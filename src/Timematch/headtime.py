# -*- coding: utf-8 -*-
from src.Timematch.travelTime import *
import seaborn as sns




# 原始数据共5列，t.ccarnumber,t.dcollectiondate,t.clicensetype,t.nderictrion,t.clanenumber
def carSort(path0):
    path1 = unicode(path0, "utf8")
    data = pd.read_csv(path1)
    data = data.iloc[:, [0, 1, 4, 3, 2]]
    data.iloc[:, 1] = pd.to_datetime(data.iloc[:, 1])
    data['day'] = data.iloc[:, 1].apply(lambda x: 100 * x.month + x.day)
    data['sj'] = data.iloc[:, 1].apply(lambda x: 3600 * x.hour + 60 * x.minute + x.second)
    data = data.sort_values(by=[data.columns[3],data.columns[2],data.columns[-2],data.columns[-1]])
    return data

def getHeadTime(data,start,end,direction,clane):
    start = datetime.datetime.strptime(start, "%Y-%m-%d")
    end = datetime.datetime.strptime(end, "%Y-%m-%d")
    date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end - start).days, 7)]
    dataMedium = []
    for i in date_generated:
        # print str(i)+' '+'begin'
        dataDay = data[data.iloc[:, -2] == (i.month * 100 + i.day)]
        dataDayDirect=dataDay[dataDay.iloc[:,3]==direction]
        for j in clane:
            dataDayClane=dataDayDirect[dataDayDirect.iloc[:,2]==j]
            dataDayClane= dataDayClane.assign(headTime=dataDayClane.iloc[:,-1].diff())
            dataMedium.append(dataDayClane)
    dataFinal=pd.concat(dataMedium,ignore_index=True)
    return dataFinal




def makePicDist(data,filterK,path0):
    dayNum = data.iloc[:,-3].unique()
    for i in dayNum:
        dataMedium=data[data.iloc[:,-3]==i]
        dataMediumFilter=dataMedium[dataMedium.iloc[:,-1]<filterK]
        # print i
        # print dataMediumFilter.iloc[:,-1].describe()
        fig, ax = plt.subplots(figsize=(15, 10))
        plt.title(str(i)+''+'head time distribution')
        sns.distplot(dataMediumFilter.iloc[:,-1],bins=50)
        plt.ylim(0,0.2)
        plt.xlim(0,10)
        plt.show()
        path1=path0+'\\'+str(i)+'.png'
        paht2=unicode(path1,'utf-8')
        plt.savefig(paht2,dpi=200)

def staDesc(path0,data,filterK):
    path1=unicode(path0,'utf-8')
    dayNum = data.iloc[:,-3].unique()
    for i in dayNum:
        dataMedium=data[data.iloc[:,-3]==i]
        dataMediumFilter=dataMedium[dataMedium.iloc[:,-1]<filterK]
        with open(path1,'a+') as f:
            f.write(str(i)+'\n'+str(dataMediumFilter.iloc[:,-1].describe())+'\n')









if __name__=="__main__":
    dataSorted=carSort(path0=r'C:\Users\wutongshu\Desktop\贵阳数据\10-05rj_zy.csv')
    dataHeadTime=getHeadTime(data=dataSorted,start='2017-06-02',end='2017-07-15',direction=2,clane=[3,4,5])
    makePicDist(dataHeadTime,filterK=50,path0=r'C:\Users\wutongshu\Desktop\雨天数据\0602headTime')
    # staDesc(path0=r'C:\Users\wutongshu\Desktop\雨天数据\0602headTime.txt',data=dataHeadTime,filterK=50)