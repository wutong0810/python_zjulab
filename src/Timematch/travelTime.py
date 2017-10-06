# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 13:46:30 2017

@author: wutongshu
"""
import pandas as pd
import numpy as np
import datetime
import cPickle as pickle

# 匹配行程时间函数
# 原始数据第1列车牌，第2列过车时刻，第3列车道，第4列为进口道方向，第5列为车型；

# 行程时间匹配函数，以下为参数说明
# up_data上游数据，down_data下游数据，down_direction下游进口道的方向，
# maxtime最大匹配行程时间，mintime最小匹配行程时间
# 匹配函数
def match_traveltime(upData, downData, maxtime, mintime, down_direction):
    downData = downData[downData.ix[:, 3] == down_direction]
    downData.index = range(len(downData))
    # 筛选正常数据，异常数据主要为未识别和无牌，因此数据位数都不为9,中文字符占2个
    downData = downData.assign(car_length=downData.iloc[:, 0].apply(lambda x: len(x)))
    #    down_data['car_length']=down_data.iloc[:,0].apply(lambda x:len(x))
    down_true = downData[(downData.iloc[:, 5] == 7) | (downData.iloc[:, 5] == 9)]
    down_true.index = range(len(down_true))
    # 计算下游识别率
    #    if len(up_data)>0:
    #        plate_identify_rate1=float(len(down_true))/len(down_data)
    # 同理筛选上游正常数据，异常数据主要为未识别和无牌，因此数据位数都不为9
    upData = upData.assign(car_length=upData.iloc[:, 0].apply(lambda x: len(x)))
    #    up_data['car_length']=up_data.iloc[:,0].apply(lambda x:len(x))
    up_true = upData[(upData.iloc[:, 5] == 7) | (upData.iloc[:, 5] == 9)]
    up_true.index = range(len(up_true))
    # 计算上游识别率
    #    if len(up_data)>0:
    #        plate_identify_rate2=float(len(up_true))/len(up_data)
    # 初始化最终的大矩阵match_du，上游的车牌先进行排序
    down_true1 = np.array(down_true)
    down_true = down_true.assign(up_t=np.nan)
    down_true = down_true.assign(up_clane=np.nan)
    down_true = down_true.assign(up_direct=np.nan)
    down_true = down_true.assign(tt=0)
    match_du = np.array(down_true)
    up_true = up_true.sort_values(by=up_true.columns[1])
    up_true1 = np.array(up_true)
    #    搜索上游在合理时间范围内的车牌数据
    for i in range(len(down_true)):
        t_min = down_true1[i, 1] - maxtime
        t_max = down_true1[i, 1] - mintime
        up_medium = up_true1[(up_true1[:, 1] > t_min) & (up_true1[:, 1] < t_max)]
        m = len(up_medium)
        #       如果存在，则匹配车牌信息，并计算行程时间，一旦匹配上则跳出循环
        if m > 0:
            for j in range(m):
                if (cmp(match_du[i, 0], up_medium[j, 0]) == 0):
                    match_du[i, 6] = up_medium[j, 1]
                    match_du[i, 7] = up_medium[j, 2]
                    match_du[i, 8] = up_medium[j, 3]
                    match_du[i, 9] = match_du[i, 1] - up_medium[j, 1]
                    break
                #    将匹配好的大矩阵按车牌，和下游过程时刻排序，去掉重复匹配的车牌
    match_time = pd.DataFrame(match_du)
    match_time = match_time.sort_values(by=[0, 1])
    match_time.index = range(len(match_time))
    match_time1 = np.array(match_time)
    indice = []
    # 阈值设置为100s
    for h in range(1, len(match_time1)):
        if (cmp(match_time1[h, 0], match_time1[h - 1, 0]) == 0) & (match_time1[h, 1] - match_time1[h - 1, 1] < 100):
            indice.append(h - 1)
        # 给行程时间付上-1来标示行程时间
    for i in indice:
        match_time1[i, 9] = -1
    # 筛选出正常的数据
    match_time2 = match_time1[match_time1[:, 9] > -1]
    match_tt = pd.DataFrame(match_time2)
    # 重新按下游过车时刻来排序
    match_tt = match_tt.sort_values(by=[1, 0])
    # 修改索引
    match_tt.index = range(len(match_tt))
    #    计算下匹配率
    match_final = match_tt[match_tt.iloc[:, 9] > 0]
    match_final.columns = ['car_num', 'd_time', 'd_clane', 'd_direction', 'car_type', 'num_length', 'u_time', 'u_clane',
                           'u_direction', 'tt']
    #   删掉车牌长度
    if len(match_du) == 0:
        match_rate = 0
    else:
        match_rate = float(len(match_final)) / len(match_du)
    return match_tt, match_final, match_rate




def loopMatch(start, end, downData, upData, maxtime1=900, mintime1=40, down_direction1=3):
    match_total_tt = []
    match_total_final = []
    match_total_rate = []
    # 匹配车牌行程时间，按天分别匹配
    start = datetime.datetime.strptime(start, "%Y-%m-%d")
    end = datetime.datetime.strptime(end, "%Y-%m-%d")
    date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end - start).days, 7)]
    for i in date_generated:
        print i+'begin'
        down_data2 = downData[downData.iloc[:, -2] == (i.month*100+i.day)]
        up_data2 = upData[upData.iloc[:, -2] == (i.month*100+i.day)]
        if (len(down_data2) == 0) | (len(up_data2) == 0):
            match_total_tt.append(0)
            match_total_final.append(0)
            match_total_rate.append(0)
            continue
        down_data3 = down_data2.iloc[:, [0, -1, 2, 3, 4]]
        up_data3 = up_data2.iloc[:, [0, -1, 2, 3, 4]]
        match_tt, match_final, match_rate = match_traveltime(up_data3, down_data3, maxtime=maxtime1, mintime=mintime1,
                                                             down_direction=down_direction1)
        match_total_tt.append(match_tt)
        match_total_final.append(match_final)
        match_total_rate.append(match_rate)
    return match_total_tt, match_total_final, match_total_rate


# 原始数据第1列车牌，第2列过车时刻，第3列车道，第4列为进口道方向，第5列为车型；
def openfile(inpath1=r"C:\Users\wutongshu\Desktop\贵阳数据\zh_zy1201-1215.csv",
             inpath2=r"C:\Users\wutongshu\Desktop\贵阳数据\rj_zy1201-1215.csv"):
    uipath1 = unicode(inpath1, "utf8")
    uipath2 = unicode(inpath2, "utf8")
    downData = pd.read_csv(uipath1)
    upData = pd.read_csv(uipath2)
    downData = downData.iloc[:, [0, 1, 4, 3, 2]]
    upData = upData.iloc[:, [0, 1, 4, 3, 2]]
    downData.iloc[:, 1] = pd.to_datetime(downData.iloc[:, 1])
    upData.iloc[:, 1] = pd.to_datetime(upData.iloc[:, 1])
    downData['day'] = downData.iloc[:, 1].apply(lambda x: 100 * x.month + x.day)
    upData['day'] = upData.iloc[:, 1].apply(lambda x: 100 * x.month + x.day)
    downData['sj'] = downData.iloc[:, 1].apply(lambda x: 3600 * x.hour + 60 * x.minute + x.second)
    upData['sj'] = upData.iloc[:, 1].apply(lambda x: 3600 * x.hour + 60 * x.minute + x.second)
    dayNum = downData.day.unique()
    return downData, upData, dayNum

def writeObject(path0,data):
    path1 = unicode(path0, "utf8")
    fileOpen=open(path1,'wb')
    pickle.dump(data,fileOpen)
    fileOpen.close()


def loadObject(path0):
    path1 = unicode(path0, "utf8")
    fileOpen=open(path1,'rb')
    data=pickle.load(fileOpen)
    fileOpen.close()
    return data



#行程时间预处理函数
#根据箱型图原理处理原始数据,滚动时间窗。
#match是车牌匹配后的行程时间矩阵（array），含9列，1列车牌信息，2列为下游过车时刻，3列下游车道编号，4列下游行驶方向，5列车型，6列上游过车时刻，7列上游车道编号，8列上游进口方向，9列行程时间
#cd为周期划分方案
#tet,处理间隔
#tet1,低峰期每tet处理一次，每次提取tet1时长的时距tet1
#tet2,非低峰期每tet处理一次，每次提取tet2时长的时距tet1
#num，样本数阈值
#cs,时间窗中IQR的系数，默认1.5
#td,替代分位值，采用上一时间窗的td 100-td分位值进行替代
#lc，采用标准差变化率时，本时间窗标准差与上一时间窗标准差的正常变化范围参数，默认1.8
#match_pre,预处理后的行程时间矩阵，含7列，1列上游过车时刻，2列上游车道编号，3列上游进口方向，4列下游过车时刻，5列下游车道编号，6列下游进口方向，7列行程时间
#ap_et，预处理评价矩阵，1、2为时间窗，3列上边界，4列下边界，5列一次处理后的标准差
#    tet为处理步长，tet默认为60s，即每60s来一个数据，
def data_deal(match_du,tet=60,tet1=1800,tet2=300,num=10,td=90,lc=1.8):
    cd=np.array([[0,25200,77,23],[25200,32400,100,24],[32400,59400,110,25],[59400,72000,100,24],[72000,86400,77,23]])
    match_final_1=[]
    match_twp_time=[]
#    处理步数
    step=(24*3600/tet)
    ap_et=np.zeros(((24*3600/tet),6))
    for i in range(step):
        if (i*tet<3600*7)|(i*tet>=3600*19.5):
            ap_et[i,0]=i*tet-tet1
            ap_et[i,1]=i*tet
        else:
            ap_et[i,0]=i*tet-tet2
            ap_et[i,1]=i*tet
        if ap_et[i,0]<0:
            ap_et[i,0]=0
        gc1=cd[(ap_et[i,0]>=cd[:,0])&(ap_et[i,0]<cd[:,1])][:,3]
        gc2=cd[(ap_et[i,1]>=cd[:,0])&(ap_et[i,1]<cd[:,1])][:,3]
        gc=max(gc1,gc2)
        cc1=cd[(ap_et[i,0]>=cd[:,0])&(ap_et[i,0]<cd[:,1])][:,2]
        cc2=cd[(ap_et[i,1]>=cd[:,0])&(ap_et[i,1]<cd[:,1])][:,2]
        cc=max(cc1,cc2)
        match_tw_time=match_du[(match_du[:,1]>=ap_et[i,0])&(match_du[:,1]<ap_et[i,1])]
        if (len(match_tw_time)==0):
            continue
        else:
            if (len(match_tw_time)<=num):
                if len(match_twp_time)>0:
                    match_tw_time1=match_tw_time[(match_tw_time[:,8]<(np.percentile(match_twp_time[:,8],td)+cc))&(match_tw_time[:,8]>=(np.percentile(match_twp_time[:,8],100-td)-cc))]
                else:
#                    上限
                    ap_et[i,2]=1.5*(np.percentile(match_tw_time[:,8],75)-np.percentile(match_tw_time[:,8],25))+np.percentile(match_tw_time[:,8],75)
#                    下限
                    ap_et[i,3]=-1.5*(np.percentile(match_tw_time[:,8],75)-np.percentile(match_tw_time[:,8],25))+np.percentile(match_tw_time[:,8],25)
                    match_tw_time1=match_tw_time[(match_tw_time[:,8]>=ap_et[i,3])&(match_tw_time[:,8]<=ap_et[i,2])]
            else:
#                上限
                ap_et[i,2]=1.5*(np.percentile(match_tw_time[:,8],75)-np.percentile(match_tw_time[:,8],25))+np.percentile(match_tw_time[:,8],75)
#                下限
                ap_et[i,3]=-1.5*(np.percentile(match_tw_time[:,8],75)-np.percentile(match_tw_time[:,8],25))+np.percentile(match_tw_time[:,8],25)
                match_tw_time1=match_tw_time[(match_tw_time[:,8]>=ap_et[i,3])&(match_tw_time[:,8]<=ap_et[i,2])]
                ap_et[i,4]=np.std(match_tw_time1[:,8])
                if ap_et[i,4]<(gc/2.+10):
    #                上限
                    ap_et[i,2]=(np.percentile(match_tw_time[:,8],25))+cc
    #                下限
                    ap_et[i,3]=(np.percentile(match_tw_time[:,8],25))-cc
                    match_tw_time1=match_tw_time[(match_tw_time[:,8]>=ap_et[i,3])&(match_tw_time[:,8]<=ap_et[i,2])]
                else:
                    if len(match_twp_time)>0:
                        if ap_et[i-1,5]<=gc/2.+10:
                            bzgu=gc/2.+10
                        else:
                            bzgu=ap_et[i-1,5]
                        if ap_et[i,4]>lc*bzgu:
                            match_tw_time1=match_tw_time[(match_tw_time[:,8]<(np.percentile(match_twp_time[:,8],td)+cc))&(match_tw_time[:,8]>=(np.percentile(match_twp_time[:,8],100-td)-cc))]
            match_twp_time=match_tw_time1
            ap_et[i,5]=np.std(match_tw_time1[:,8])
        if len(match_tw_time1)>0:
            match_tw_time1=match_tw_time1[(match_tw_time1[:,1]>=((i-1)*tet)) & (match_tw_time1[:,1]<(i*tet))]
#            一分钟时间窗内有数据，就保存这一分钟数据
            if len(match_tw_time1)>0:
                match_tw_time1=pd.DataFrame(match_tw_time1)
                match_final_1.append(match_tw_time1)
    match_final1 = pd.concat(match_final_1, ignore_index=True)
    return match_final1


def loopDeal(match_total_final, claneNum):
    tt_deal = []
    for i in range(len(match_total_final)):
        test = match_total_final[i].iloc[:, [0, 1, 2, 3, 4, 6, 7, 8, 9]]
        if len(test) > 0:
            medData = []
            for j in claneNum:
                straightData = test[(test.iloc[:, 2] == j)]
                medData.append(straightData)
            medFinal = pd.concat(medData, ignore_index=True)
            med_data = np.array(medFinal)
            med_deal = data_deal(med_data, tet=60, tet1=1800, tet2=300, num=10, td=90, lc=1.1)
        else:
            med_deal = 0
        tt_deal.append(med_deal)
    return tt_deal


if __name__ == "__main__":
    downData, upData, dayNum = openfile(inpath1=r'C:\Users\wutongshu\Desktop\贵阳数据\10-05zh_zy.csv',
                                           inpath2=r'C:\Users\wutongshu\Desktop\贵阳数据\10-05rj_zy.csv')
    match_total_tt, match_total_final, match_total_rate=loopMatch(start='2017-06-02', end='2017-07-15', downData=downData, upData=upData,
                                                                  maxtime1=900, mintime1=40, down_direction1=3)
    # matchData=loadObject(path0=r'C:\Users\wutongshu\Desktop\雨天数据\travelTimeFinal.txt')
    matchDataDeal=loopDeal(match_total_final=match_total_final, claneNum=[1,2,3,4])
    writeObject(path0=r'C:\Users\wutongshu\Desktop\雨天数据\0602travelTimeDeal.txt', data=matchDataDeal)



