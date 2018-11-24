#!/home/mmurko/anaconda2/bin/python

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import sys



def primerjava(data):
    data[(data.index < datetime(2009,12,2)) & (data.index > datetime(2009,12,1))].plot()
    #data360.plot(kind='line')
    #plt.figure(2)
    #plt.plot(data360['cas'],data360['visina'],'r')
    #plt.grid()
    plt.show()
    #print data360
    #print data360['visina']
    
def main():
    homedir = '/home/mmurko/Downloads/'
    
    fname = homedir+'data2006-2018.txt'
    data = pd.read_table(fname,index_col='cas',parse_dates=True)
    
    print data
    primerjava(data)

    
if __name__=="__main__":
    main()
    
