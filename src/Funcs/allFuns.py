# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 13:46:30 2017

@author: wutongshu
"""
import pandas as pd
import numpy as np



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



if __name__=='__main__':
    data=loadData(path0=r'C:\Users\wutongshu\Desktop\雨天数据\10-03count_zhonghua.csv')
    dataCount=countData(data)

