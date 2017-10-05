import pandas as pd
import numpy as np



def loadData(path0):
    path1=unicode(path0,'utf-8')
    data=pd.read_csv(path1)
    return data



