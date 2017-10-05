# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 13:46:30 2017

@author: wutongshu
"""
from src.Funcs.allFuns import *


def main():
    data=loadData(path0=r'C:\Users\wutongshu\Desktop\雨天数据\10-03count_zhonghua.csv')
    dataCount=countData(data)
    makePic(dataCount,'2017-06-01','2017-07-15',1)




if __name__=='__main__':
    main()
