# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 13:46:30 2017

@author: wutongshu
"""
import pandas as pd
import numpy as np



#匹配行程时间函数
#原始数据第1列车牌，第2列过车时刻，第3列车道，第4列为进口道方向，第5列为车型；

#行程时间匹配函数，以下为参数说明
#up_data上游数据，down_data下游数据，down_direction下游进口道的方向，
#maxtime最大匹配行程时间，mintime最小匹配行程时间
#匹配函数
def match_traveltime(up_data,down_data,maxtime,mintime,down_direction):
    down_data=down_data[down_data.ix[:,3]==down_direction]
    down_data.index=range(len(down_data))
#筛选正常数据，异常数据主要为未识别和无牌，因此数据位数都不为9,中文字符占2个
    down_data=down_data.assign(car_length=down_data.iloc[:,0].apply(lambda x:len(x)))
#    down_data['car_length']=down_data.iloc[:,0].apply(lambda x:len(x))
    down_true=down_data[(down_data.iloc[:,5]==7 )| (down_data.iloc[:,5]==9)]
    down_true.index=range(len(down_true))
#计算下游识别率
#    if len(up_data)>0:
#        plate_identify_rate1=float(len(down_true))/len(down_data)
#同理筛选上游正常数据，异常数据主要为未识别和无牌，因此数据位数都不为9
    up_data=up_data.assign(car_length=up_data.iloc[:,0].apply(lambda x:len(x)))
#    up_data['car_length']=up_data.iloc[:,0].apply(lambda x:len(x))
    up_true=up_data[(up_data.iloc[:,5]==7)|(up_data.iloc[:,5]==9)]
    up_true.index=range(len(up_true))
#计算上游识别率
#    if len(up_data)>0:
#        plate_identify_rate2=float(len(up_true))/len(up_data)
#初始化最终的大矩阵match_du，上游的车牌先进行排序
    down_true1=np.array(down_true)
    down_true=down_true.assign(up_t=np.nan)
    down_true=down_true.assign(up_clane=np.nan)
    down_true=down_true.assign(up_direct=np.nan)
    down_true=down_true.assign(tt=0)
    match_du=np.array(down_true)
    up_true=up_true.sort_values(by=up_true.columns[1])
    up_true1=np.array(up_true)
#    搜索上游在合理时间范围内的车牌数据
    for i in range(len(down_true)):
        t_min=down_true1[i,1]-maxtime
        t_max=down_true1[i,1]-mintime
        up_medium=up_true1[(up_true1[:,1]>t_min)&(up_true1[:,1]<t_max)]
        m=len(up_medium)
#       如果存在，则匹配车牌信息，并计算行程时间，一旦匹配上则跳出循环
        if m>0:
            for j in range(m):
                if (cmp(match_du[i,0],up_medium[j,0])==0):
                    match_du[i,6]=up_medium[j,1]
                    match_du[i,7]=up_medium[j,2]
                    match_du[i,8]=up_medium[j,3]
                    match_du[i,9]=match_du[i,1]-up_medium[j,1]
                    break
#    将匹配好的大矩阵按车牌，和下游过程时刻排序，去掉重复匹配的车牌
    match_time=pd.DataFrame(match_du)
    match_time=match_time.sort_values(by=[0,1])
    match_time.index=range(len(match_time))
    match_time1=np.array(match_time)
    indice=[]
#阈值设置为100s
    for h in range(1,len(match_time1)):
        if (cmp(match_time1[h,0],match_time1[h-1,0])==0)& (match_time1[h,1]-match_time1[h-1,1]<100):
            indice.append(h-1)
#给行程时间付上-1来标示行程时间
    for i in indice:
        match_time1[i,9]=-1
#筛选出正常的数据
    match_time2=match_time1[match_time1[:,9]>-1]
    match_tt=pd.DataFrame(match_time2)
#重新按下游过车时刻来排序
    match_tt=match_tt.sort_values(by=[1,0])
#修改索引
    match_tt.index=range(len(match_tt))
#    计算下匹配率
    match_final=match_tt[match_tt.iloc[:,9]>0]
    match_final.columns=['car_num','d_time','d_clane','d_direction','car_type','num_length','u_time','u_clane','u_direction','tt']
#   删掉车牌长度
    if len(match_du)==0:
        match_rate=0
    else :
        match_rate=float(len(match_final))/len(match_du)
    return match_tt,match_final,match_rate




#循环匹配函数,前面为上下游数据，以及天，后面为匹配函数的主要参数
def loopMatch(downData,upData,dayNum,maxtime1=900,mintime1=40,down_direction1=3):
    match_total_tt=[]
    match_total_final=[]
    match_total_rate=[]
    #匹配车牌行程时间，按天分别匹配
    for i in dayNum:
        down_data2=downData[downData.iloc[:,-1]==i]
        up_data2=upData[upData.iloc[:,-1]==i]
        if (len(down_data2)==0)|(len(up_data2)==0):
            match_total_tt.append(0)
            match_total_final.append(0)
            match_total_rate.append(0)
            continue
        down_data3=down_data2.iloc[:,[0,5,2,3,4]]
        up_data3=up_data2.iloc[:,[0,5,2,3,4]]
        match_tt,match_final,match_rate=match_traveltime(up_data3,down_data3,maxtime=maxtime1,mintime=mintime1,down_direction=down_direction1)
        match_total_tt.append(match_tt)
        match_total_final.append(match_final)
        match_total_rate.append(match_rate)
    return match_total_tt,match_total_final,match_total_rate