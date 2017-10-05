# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 13:46:30 2017

@author: wutongshu
"""
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import seaborn as sns



def loadData(path0):
    path1=unicode(path0,'utf-8')
    data=pd.read_csv(path1)
    return data



# data第1列MONTH,第2列DAYS，第3列SJ，第4列N
def countData(data):
    dataCount=pd.pivot_table(data,index='SJ',columns=['MONTH','DAYS'],values='N')
    dataCount.columns = [col for col in dataCount.columns]
    dataCount=dataCount.reset_index()
    return dataCount

#绘制同星期日的数据总量变化情况
def makePic(data,start,end,beginIndex):
    start = datetime.datetime.strptime(start, "%Y-%m-%d")
    end = datetime.datetime.strptime(end, "%Y-%m-%d")
    date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end - start).days,7)]
    fig, ax = plt.subplots(figsize=(15, 10))
    colorbox=['b','g','r','c','m','y','k']
    for i,j in enumerate(date_generated):
        label_time=j.strftime("%Y-%m-%d")
        plt.plot(data.iloc[:, 0]*(1.0/2), data.iloc[:, i*7+beginIndex], 'o-', color=colorbox[i],label=label_time)
    plt.legend()
    plt.xlim(0,24)
    xticks = range(0, 24,2)
    ax.set_xticks(xticks)
    ax.set_xticklabels(["$%d$" % y for y in xticks], fontsize=12)
    plt.show()


if __name__=='__main__':
    data=loadData(path0=r'C:\Users\wutongshu\Desktop\雨天数据\10-03count_zhonghua.csv')
    dataCount=countData(data)
    makePic(dataCount,'2017-06-01','2017-07-15',1)


