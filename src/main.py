# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 13:46:30 2017

@author: wutongshu
"""
from src.Funcs.allFuns import *
from src.Timematch.travelTime import *

def main():
    # data=loadData(path0=r'C:\Users\wutongshu\Desktop\雨天数据\10-03count_zhonghua.csv')
    # dataCount=countData(data)
    # makePic(dataCount,'2017-06-01','2017-07-15',1)
    travelTimeFilter=loadObject(path0=r'C:\Users\wutongshu\Desktop\雨天数据\0602travelTimeDeal.txt')
    distTime(travelTimeFilter)






if __name__=='__main__':
    travelTimeFilter = loadObject(path0=r'C:\Users\wutongshu\Desktop\雨天数据\0602travelTimeDeal.txt')
    # distTime(travelTimeFilter)
    ttDesci(path0=r'C:\Users\wutongshu\Desktop\雨天数据\0602TravelTimeSta.txt',data=travelTimeFilter)
    # scatterTime(travelTimeFilter)
