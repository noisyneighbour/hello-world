#!/home/mmurko/anaconda2/bin/python

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import sys
import time

#Podatki o treh senzorjih vodostaja na mareografu Koper:
"""
360	vodostaj	vodostaj povrsinske vode iz tlacne sonde (podatkovni zapisovalnik)	10	podatki_ott	0	4	cm	A	Vodostaj	cm		vrednost		95		D	1		D	1	7	0	D			360				D			23.10.2009 09:22 	ISMM				N	8	3
	361	vodostaj	vodostaj povrsinske vode z radarskega senzorja (podatkovni zapisovalnik)	10	podatki_ott	0	4	cm	A	Vodostaj	m		vrednost		95		D	1		D	1	9	0	D			361				D			23.10.2009 09:22 	ISMM				N	8	3
	362	vodostaj	vodostaj povrsinske vode iz limnigrafa (podatkovni zapisovalnik)	10	podatki_ott	0	4	cm	A	vodostaj povrsinske vode iz limnigrafa(podatkovni zapisovalnik)	m3/s
"""
#V podatkih visina 360 je 23.5.2017 od 5:00 do 8:00 luknja v podatkih. Da preprecimo zamik podatkov od takrat naprej sem zapolnil luknjo s podatki iz 361
#Po pregledu podatkov je 362 imel eno anomalijo pri maksimumu decembra, pri 361 pa manjkajo podatki za en cas v koncu decembra. Najbolj primeren set podatkov je 360.

#['visina360','visina361','visina362']


def sestavi_tabelo_podatkov():      #V funkcijo se bo vstavilo ime fajla s podatki iz mareografa koper za posamezen senzor
    homedir = 'C:\ARSO\python_delo\'
    global data
    
    #Ta del sestavi tabelo podatkov, ce se ni sestavljena
    """    
    print 'berem 360'
    fname360 = homedir+'mareografKP_vodostaj2006_2018_360.txt'
    data360 = pd.read_table(fname360,index_col='cas',parse_dates=True,infer_datetime_format=True,dayfirst=True)
    
    print 'berem 361'
    fname361 = homedir+'mareografKP_vodostaj2006_2018_361.txt'
    data361 = pd.read_table(fname361,index_col='cas',parse_dates=True,dayfirst=True,infer_datetime_format=True)

    print 'berem 362'
    fname362 = homedir+'mareografKP_vodostaj2006_2018_362.txt'
    data362 = pd.read_table(fname362,index_col='cas',parse_dates=True,dayfirst=True,infer_datetime_format=True)

    print 'kombiniram v 1 tabelo'
    data=pd.concat([data360,data361,data362],axis=1)
    data['avg']=data.mean(axis=1)
    #data.columns=['Vodostaj povrsinske vode iz tlacne sonde','Vodostaj povrsinske vode iz radarskega senzorja','Vodostaj povrsinske vode iz limnigrafa','Povprecje senzorjev']
    """
    fname = homedir+'data2006-2018.txt'
    print 'berem podatke',fname

    data = pd.read_table(fname,index_col='cas',parse_dates=True,dayfirst=True,infer_datetime_format=True)
    data.columns=['s1','s2','s3','avg']
    """
    print anomalije
    anomalije=anomalije.append([1,2,3,4], ignore_index=True)
    print anomalije"""
    
    return data
    #print 'izvazam podatke v data2006-2018.txt'
    #data.to_csv('data2006-2018.txt', sep='\t')   
    
    
def najdi_anomalije(data):      #Funkcija namenjena iskanju anomalij, to je meritev ko ena meritev zelo odstopa od ostalih
    anomalije=pd.DataFrame(columns=['s1','s2','s3','avg'])
    
    for index, values in data.iterrows():
        if data.at[index,'s1']-data.at[index,'avg']>10:
            print 'anomalija1'
            print data.loc[index]
            anomalije=anomalije.append(data.loc[index])   
    anomalije.to_csv('anomalija1.txt', sep='\t')   
    anomalije=pd.DataFrame(columns=['s1','s2','s3','avg'])

    for index, values in data.iterrows():
        if data.at[index,'s2']-data.at[index,'avg']>10:
            print 'anomalija2'
            print data.loc[index]
            anomalije=anomalije.append(data.loc[index])    
            
    anomalije.to_csv('anomalija2.txt', sep='\t')   
    anomalije=pd.DataFrame(columns=['s1','s2','s3','avg'])

    for index, values in data.iterrows():
        if data.at[index,'s3']-data.at[index,'avg']>10:
            print 'anomalija3'
            print data.loc[index]
            anomalije=anomalije.append(data.loc[index])
    
    anomalije.to_csv('anomalija3.txt', sep='\t')   
    
    
def prikaz(data):
    global avgyear, avgmonth,monthdata,yeardata
    #data360.plot(kind='line')
    #plt.figure(2)
    #plt.plot(data360['cas'],data360['visina'],'r')
    #plt.grid()
    #print data360
    #print data360['visina']
    yeardata= data.resample('Y').mean()
    avgyear=pd.DataFrame(yeardata['s1'][(yeardata.index < datetime(2018,11,1)) & (yeardata.index > datetime(2006,1,30))])
    
    monthdata= data.resample('M').mean()
    avgmonth=pd.DataFrame(monthdata['s1'][(monthdata.index < datetime(2018,11,1)) & (monthdata.index > datetime(2006,1,30))])
    avgmonth.columns =['monthly average s1']
    print avgyear
    print avgmonth
    #data[(data.index < datetime(2006,2,1)) & (data.index > datetime(2006,1,1))].plot()
    #monthdata[(monthdata.index < datetime(2007,1,1)) & (monthdata.index > datetime(2006,1,1))].plot()    
    
    plt.show()
    return avgyear, avgmonth
#def najdi_maksimume_minimume(data):
    
    #    for index, values in data.iterrows():
    #plt.figure(2)
    #plt.plot(data360['cas'],data360['visina'],'r')
    #plt.grid()
    #plt.show()
    #return avgmonth

def preverjeni_podatki(data):           #s to funkcijo lahko primerjamo kako dobro so 'preverjeni' podatki iz aplikacije hidrolog.
    homedir2 = 'C:\ARSO\python_delo\'
    global data2
    #urne vrednosti
    fname2 = homedir2+'sep2014-jun2015.txt'
    #print 'berem podatke',fname2
    urnevrednosti = pd.read_table(fname2,index_col='cas',parse_dates=True,dayfirst=True,infer_datetime_format=True)
    urnevrednosti.columns=['urni_vodostaj']
    #ekstremi
    #print urnevrednosti
    fname3 = homedir2+'sep2014-jun2015ext.txt'
    print 'berem podatke',fname3
    urnevrednostiext = pd.read_table(fname3,index_col='cas',parse_dates=True,dayfirst=True,infer_datetime_format=True)
    urnevrednostiext.columns=['vodostaj_maxmin','tip_ekstrema']

    print urnevrednostiext
    
    print 'kombiniram v 1 tabelo'
    data2=pd.concat([urnevrednosti,urnevrednostiext],axis=1)
    #data['avg']=data.mean(axis=1)
    #data.columns=['Vodostaj povrsinske vode iz tlacne sonde','Vodostaj povrsinske vode iz radarskega senzorja','Vodostaj povrsinske vode iz limnigrafa','Povprecje senzorjev']
    #print data2
    daterange=(data2.index < datetime(2015,7,1)) & (data2.index > datetime(2014,9,1))
    
    plt.figure(1)
    #data2[daterange]['urni_vodostaj'].plot()    
    #data2[daterange]['vodostaj_maxmin'].plot(marker='.')    
    #data[(data.index < datetime(2014,10,1)) & (data.index > datetime(2014,9,1))].plot()
    #monthdata[(monthdata.index < datetime(2007,1,1)) & (monthdata.index > datetime(2006,1,1))].plot()   
    
    # Primerjava meritev vodostaja iz mareografaKP \ns preverjenimi podatki iz hidrologa
    daterange=(data2.index < datetime(2015,7,1)) & (data2.index > datetime(2014,9,1))
    plt.plot(data2[daterange]['vodostaj_maxmin'],marker='.',markersize=11)
    plt.plot(data[(data.index < datetime(2015,7,1)) & (data.index > datetime(2014,9,1))])
    plt.title('Primerjava meritev vodostaja iz mareografaKP \ns preverjenimi podatki iz hidrologa')
    plt.legend(['preverjeni podatki','260','261','262','avg'])
    plt.show()

def main():
   
    sestavi_tabelo_podatkov()
    #najdi_anomalije(data)
    prikaz(data)
    #najdi_maksimume_minimume(data)
    preverjeni_podatki(data)
    
    #print data

    #data=data.sort_values(by=['visina360'],ascending = False).dropna()
    #print data[(data.index < datetime(2017,07,02)) & (data.index > datetime(2017,07,01))]
    #print '20 najvisjih vodostajev\n', data.head(20)
    #print '20 najnizjih vodostajev\n', data.tail(20)
    
    
        
if __name__=="__main__":
    main()
