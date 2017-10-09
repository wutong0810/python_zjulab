# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 13:46:30 2017

@author: wutongshu
"""
from src.Funcs.allFuns import *
from src.Timematch.travelTime import *




def traveltime():
    travelTimeFilter = loadObject(path0=r'C:\Users\wutongshu\Desktop\雨天数据\0602travelTimeDeal.txt')
    scatterTime(travelTimeFilter)
    distTime(travelTimeFilter)
    ttDesci(path0=r'C:\Users\wutongshu\Desktop\雨天数据\0602TravelTimeSta.txt',data=travelTimeFilter)


def headtime():
    dataHeadtime=loadObject(path0=r'C:\Users\wutongshu\Desktop\雨天数据\0602headTimeDeal.txt')
    makePicDist(dataHeadtime,filterK=50,path0=r'C:\Users\wutongshu\Desktop\雨天数据\0602headTime')
    staDesc(path0=r'C:\Users\wutongshu\Desktop\雨天数据\0602headTime.txt',data=dataHeadtime,filterK=50)


def countArea():
    data=loadData(path0=r'C:\Users\wutongshu\Desktop\雨天数据\10-03count_zhonghua.csv')
    dataCount=countData(data)
    makePic(dataCount,'2017-06-01','2017-07-15',1)

def main():
    traveltime()
    headtime()
    countArea()






if __name__=='__main__':
    main()
