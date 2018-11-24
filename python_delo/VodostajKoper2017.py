#!/home/mmurko/anaconda2/bin/python

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import sys

#Podatki o treh senzorjih:
"""
360	vodostaj	vodostaj povrsinske vode iz tlacne sonde (podatkovni zapisovalnik)	10	podatki_ott	0	4	cm	A	Vodostaj	cm		vrednost		95		D	1		D	1	7	0	D			360				D			23.10.2009 09:22 	ISMM				N	8	3
	361	vodostaj	vodostaj povrsinske vode z radarskega senzorja (podatkovni zapisovalnik)	10	podatki_ott	0	4	cm	A	Vodostaj	m		vrednost		95		D	1		D	1	9	0	D			361				D			23.10.2009 09:22 	ISMM				N	8	3
	362	vodostaj	vodostaj povrsinske vode iz limnigrafa (podatkovni zapisovalnik)	10	podatki_ott	0	4	cm	A	vodostaj povrsinske vode iz limnigrafa(podatkovni zapisovalnik)	m3/s
"""
#V podatkih visina 360 je 23.5.2017 od 5:00 do 8:00 luknja v podatkih. Da preprecimo zamik podatkov od takrat naprej sem zapolnil luknjo s podatki iz 361
#Po pregledu podatkov je 362 imel eno anomalijo pri maksimumu decembra, pri 361 pa manjkajo podatki za en cas v koncu decembra. Najbolj primeren set podatkov je 360.

#['visina360','visina361','visina362']

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
    
    fname360 = homedir+'mareografKP_vodostaj2006-2018_360.txt'
    data360 = pd.read_table(fname360)
    
    fname361 = homedir+'mareografKP_vodostaj2006-2018_361.txt'
    data361 = pd.read_table(fname361)
    
    fname362 = homedir+'mareografKP_vodostaj2006-2018_362.txt'
    data362 = pd.read_table(fname362)

    """
    data=data360
    data['visina360']=data360['visina']
    data['visina361']=data361['visina']
    data['visina362']=data362['visina']
    data=data.drop(['visina'],axis=1)"""
    print 'indexiram 360'
    for i in range(data360.shape[0]):
        data360.at[i,'cas']=datetime.strptime(data360['cas'][i], "%d.%m.%Y %H:%M")
    #data360['cas'] = pd.to_datetime(data360['cas'])
    data360 = data360.set_index(['cas'])
    
    print 'indexiram 361'
    for i in range(data361.shape[0]):
        data361.at[i,'cas']=datetime.strptime(data361['cas'][i], "%d.%m.%Y %H:%M")
    data361 = data361.set_index(['cas'])
    
    print 'indexiram 362'
    for i in range(data362.shape[0]):
        data362.at[i,'cas']=datetime.strptime(data362['cas'][i], "%d.%m.%Y %H:%M")
    data362 = data362.set_index(['cas'])
    
    #print data360
    #print data361
    #print data362
    print 'kombiniram v 1 tabelo'
    data=pd.concat([data360,data361,data362],axis=1)
    data['sensor_average']=data.mean(axis=1)
    data.columns=['Vodostaj povrsinske vode iz tlacne sonde','Vodostaj povrsinske vode iz radarskega senzorja','Vodostaj povrsinske vode iz limnigrafa','Povprecje senzorjev']
    print data
    
    #data=data.sort_values(by=['visina360'],ascending = False).dropna()
    primerjava(data)
    #print data[(data.index < datetime(2017,07,02)) & (data.index > datetime(2017,07,01))]
    #print '20 najvisjih vodostajev\n', data.head(20)
    #print '20 najnizjih vodostajev\n', data.tail(20)
    data.to_csv('data2006-2018.txt', sep='\t')    

    
if __name__=="__main__":
    main()
