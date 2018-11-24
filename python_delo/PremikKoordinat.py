#!/home/mmurko/anaconda2/bin/python

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import sys

#README
"""
Ta skripta kot input vzame tabelo dogodkov poplav, jih razvrsti glede na opozorilno vrednost v 4 skupine, rdeco, oranzno, rumeno in ostale. Presteje koliko je poplav v posamezni skupini in naredi osnovno statistiko.

V drugem delu imamo moznost zamakniti koordinate v 3 smeri glede na poplavno nevarnost. To je uporabno za nadaljno vizualizacijo v gis-u, saj so malo zamaknjene koordinate bolj pregledne.

Na koncu v txt file da urejeno tabelo s klasifikatorji za poplavne nevarnosti
"""

def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
            "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)
    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                            "(or 'y' or 'n').\n")

#Priprava stevcev in slovarjev za opozorilne kategorije (rdeca, oranzna, rumena, ostalo)
st_rumenih=0
st_oranznih=0
st_rdecih=0
st_ostalih=0
rdeca = {"dict_name":"rdeco","min":"350","max":"1000","klasifikator":"3","barvni_stevec":st_rdecih}
oranzna = {"dict_name":"oranzno","min":"330","max":"350","klasifikator":"2","barvni_stevec":st_oranznih}
rumena = {"dict_name":"rumeno","min":"300","max":"330","klasifikator":"1","barvni_stevec":st_rumenih}
ostalo = {"dict_name":"ostalo","min":"0","max":"300","klasifikator":"0","barvni_stevec":st_ostalih}


def pripravi_tabelo_data(lokacija_fajla,ime_datoteke):
    fname = lokacija_fajla+ime_datoteke
    global data
    data = pd.read_excel(fname)
    data[['DAILY MAXIMUM','YEAR']]=data[['DAILY MAXIMUM','YEAR']].apply(pd.to_numeric, errors='coerce')
    
    #naredi stolpce
    POPLAVNA_NEVARNOST= [0 for i in range(data.shape[0])]

    #vnesi stolpce v tabelo "data"
    data['POPLAVNA_NEVARNOST'] = POPLAVNA_NEVARNOST
    
    #Dodatek stolpca "dates" v %Y %m %d %H:%M:%S formatu
    dates=[]
    for i in range(data.shape[0]):
        y = str(data['YEAR'][i])
        m = str(data['MONTH'][i])
        d = str(data['DAY'][i])
        t = str(data['TIME'][i])
        
        #tstr = datetime.strftime(t,'%H:%M:%S')
        datetime_string = y+' '+m+' '+d+' '+t
        
        dates.append(datetime.strptime(datetime_string,'%Y %m %d %H:%M:%S'))
    
    data['dates'] = dates
    data = data.set_index(['dates'])
    return data


def klasificiraj_poplave(data,barva):
    if barva==ostalo:
        print '\nOstale poplave: \n'
    else: print '\nPoplave z',barva['dict_name'],'opozorilno vrednostjo (' + str(barva['min']),'-',barva['max'],'cm): \n'
    
    print '[Visina gladine, leto, mesec, dan, lokacija]'
    for i in range(data.shape[0]):
        if int(barva['min'])<=data['DAILY MAXIMUM'][i]<int(barva['max']):
            print [data['DAILY MAXIMUM'][i],data['YEAR'][i],data['MONTH'][i],data['DAY'][i],data['MUNICIPALITY'][i]]
            data.at[i,'POPLAVNA_NEVARNOST']=barva['klasifikator']
            barva['barvni_stevec']+=1 
            j=i+1
            #if data['YEAR'][i]==data['YEAR'][j]:
             #   print 'lol'
             #   print data['POPLAVNA_NEVARNOST'][i]

    print '\nStevilo takih dogodkov: ',barva['barvni_stevec'],'\n'
    return data
#Ta funkcija kot input vzame tabelo podatkov in zeljeno opozorilno vrednost. Output prikaze vse poplave s tako opozorilno vrednostjo in jih presteje


def zamik_koordinat(data,vrednost_zamika):
    xdisp= int(vrednost_zamika)*3/(2*np.sqrt(3))
    ydisp= int(vrednost_zamika) /2
    for i in range(data.shape[0]):
        if 300<=data['DAILY MAXIMUM'][i]<329:
            data.at[i,'GAUSSKY']=data.at[i,'GAUSSKY']-int(ydisp)
            data.at[i,'GAUSSKX']=data.at[i,'GAUSSKX']-int(xdisp)
        elif 330<=data['DAILY MAXIMUM'][i]<349:
            data.at[i,'GAUSSKY']=data.at[i,'GAUSSKY']-int(ydisp)
            data.at[i,'GAUSSKX']=data.at[i,'GAUSSKX']+int(xdisp)
        elif data['DAILY MAXIMUM'][i]>=350:
            data.at[i,'GAUSSKY']=data.at[i,'GAUSSKY']+2*int(ydisp)
            data.at[i,'GAUSSKX']=data.at[i,'GAUSSKX']

    
    global txt_name_string
    txt_name_string='zamaknjene_koordinate_'+vrednost_zamika+'.txt'
    data.to_csv(txt_name_string, sep='\t')    
    print txt_name_string
    return data
    return txt_name_string
#Ta funkcija kot input vzame tabelo podatkov, in stevilo metrov zamika koordinat. Kot output naredi tabelo zamaknjenih koordinat glede na opozorilno vrednost in jo izvozi v "zamaknjene_koordinate_STEVILOMETROV.txt"


def statistika(data):
    global data_brez_ostalih,groupby_year
    data_brez_ostalih=data[data['DAILY MAXIMUM']>=300]
    #.reset_index(drop=True)
    
   # data_brez_ostalih=data_brez_ostalih.reset_index(drop=True)
    #Stevec poplav po kategorijah v posameznem letu. Output je tabela s stolpci 'stevilo_rumenih', 'stevilo_oranznih' in 'stevilo_rdecih' za vsako leto
    rum=ora=rde=0
    RUM=[]
    ORA=[]
    RDE=[] 
    #Pripravimo tabelo statistike. Stolpci: STEVILO_POPLAV, POVPRECNA_VISINA_POPLAVE, STEVILO_RUMENIH, STEVILO_ORANZNIH, STEVILO_RDECIH
    groupby_year = data_brez_ostalih.groupby('YEAR')
    groupby_year= groupby_year.mean().drop(['MONTH','DAY','GAUSSKX','GAUSSKY','POPLAVNA_NEVARNOST'],axis=1).rename(columns={'DAILY MAXIMUM':'POVPRECNA_VISINA_POPLAVE'})    #Izoliraj in preimenuj stolpec povprecne visine gladine v posameznem letu
    groupby_year.insert(0,column='STEVILO_POPLAV',value=data_brez_ostalih.groupby('YEAR')['YEAR'].count()) 
    
    
    for j in range(data_brez_ostalih['YEAR'].unique().tolist()[0],data_brez_ostalih['YEAR'].unique().tolist()[-1]+1):
        asd=data_brez_ostalih[data_brez_ostalih['YEAR']==j]

        if asd.empty:   #Ce ni podatka za to leto
            print '\n\nZa leto',j,'ni podatkov o poplavah'
            rum=ora=rde=0
            RUM.append(rum)
            ORA.append(ora)
            RDE.append(rde) 
            groupby_year.loc[j]=0   #Na mestu kjer ni podatka dodaj vrsto 0. Zelimo barplot 'brez lukenj' na x osi
            groupby_year.sort_index(inplace=True)
        else:   #Ce imamo podatek za to leto
            print '\n\nPoplave v letu',j,'\n',asd[['DAILY MAXIMUM','YEAR']]
            for i in range(asd.shape[0]):
                if 300<=asd['DAILY MAXIMUM'].iloc[i]<330:
                    rum+=1
                elif 330<=asd['DAILY MAXIMUM'].iloc[i]<350:
                    ora+=1
                elif asd['DAILY MAXIMUM'].iloc[i]>=350:
                    rde+=1
            RUM.append(rum)
            ORA.append(ora)
            RDE.append(rde)
        rum=ora=rde=0
    
    groupby_year['STEVILO_RUMENIH']=RUM
    groupby_year['STEVILO_ORANZNIH']=ORA
    groupby_year['STEVILO_RDECIH']=RDE
    groupby_year.insert(2,column='MAX_POPLAVA',value=data_brez_ostalih.groupby('YEAR')['DAILY MAXIMUM'].max()) 

    
    print '\n\nTabela statistike:\n\n',groupby_year

    return data_brez_ostalih, groupby_year
#Naredi statistiko podatkov, output je tabela s stolpci: leto, stevilo poplav, povprecna visina, max visina. 
#Koda v tabeli groupby_year doda vrednosti 0 za leta v katerih ni podatkov. To naredi zato da v barplot-u 'ni lukenj' na x osi.


    
def main():
    pripravi_tabelo_data('/home/mmurko/Downloads/','SPIN_ARSO_2006-2018_EN.xlsx') #Funkcija prebere podatke iz poljubnega fajla v poljubni mapi in uredi datetime index
    
    #Klasifikacija poplav glede na opozorilno vrednost (rumena, oranzna, rdeca)
    """klasificiraj_poplave(data,rumena)    
    klasificiraj_poplave(data,oranzna) 
    klasificiraj_poplave(data,rdeca) 
    klasificiraj_poplave(data,ostalo)"""

    statistika(data)
        
    #Narisi stacked barplot
    
    #fig, ax = plt.subplots()
    ax=groupby_year[['STEVILO_ORANZNIH','STEVILO_RDECIH','STEVILO_RUMENIH']].plot.bar(color={'r','yellow','darkorange'},stacked=True)
    ax.set_ylabel('Stevilo poplav')
    ax.set_xlabel('Leto')
    plt.title('Poplave na slovenski obali razvrscene po poplavni nevarnosti')   
    ax.legend(('Stevilo oranznih','Stevilo rdecih','Stevilo rumenih'))
    plt.show()
    
    #poskus dodajanja sekundarne y osi za prikaz povprecne visine poplave
    
    """x_os=range(data_brez_ostalih['YEAR'].unique().tolist()[0],data_brez_ostalih['YEAR'].unique().tolist()[-1]+1)
    y_os=groupby_year['STEVILO_ORANZNIH'].tolist()
    #fig, ax = plt.subplots()
    ax=plot.bar(x_os, y_os)
    ax.set_ylabel('Stevilo poplav')
    ax.set_xlabel('Leto')
    plt.title('Poplave na slovenski obali razvrscene po poplavni nevarnosti')   
    ax.legend(('Stevilo oranznih','Stevilo rdecih','Stevilo rumenih'))
    ax2 = ax.twinx()
    ax2.plot(y=groupby_year[['MAX_POPLAVA']])
    plt.show()"""
    """
    fig, ax = plt.subplots()
    ax.set_ylabel('Stevilo poplav')
    ax.set_xlabel('Leto')
    plt.title('Poplave na slovenski obali razvrscene po poplavni nevarnosti')  
    
    groupby_year.plot.line(y='MAX_POPLAVA',ax=ax,color='r')

    ax2 = ax.twinx()   
    ax2.set_ylabel('STEVILO_RUMENIH')

    groupby_year.plot.bar(y='STEVILO_RUMENIH',ax=ax2)
    fig.tight_layout()
    plt.show()
"""
    
    """
    np.random.seed(2016)

    N = 150
    pandoc = pd.DataFrame({'date_time':pd.date_range('2000-1-1', periods=N, freq='M'),
                    'total_goals':np.random.randint(10, size=N)})
    fig, tg = plt.subplots(1)
    print pandoc
    pandoc.plot(x='date_time', y='total_goals', kind="bar", ax=tg)

    labels, skip = ['']*N, 10
    labels[skip//2::skip] = pandoc['date_time'].dt.strftime('%Y-%m-%d')[skip//2::skip]
    tg.set_xticklabels(labels)

    fig.autofmt_xdate()
    plt.show()
    
    
    
    fig, ax1 = plt.subplots()
    t = np.arange(0.01, 10.0, 0.01)
    s1 = np.exp(t)
    ax1.plot(t, s1, 'b-')
    ax1.set_xlabel('time (s)')
    # Make the y-axis label, ticks and tick labels match the line color.
    ax1.set_ylabel('exp', color='b')
    ax1.tick_params('y', colors='b')

    ax2 = ax1.twinx()
    s2 = np.sin(2 * np.pi * t)
    ax2.plot(t, s2, 'r.')
    ax2.set_ylabel('sin', color='r')
    ax2.tick_params('y', colors='r')

    fig.tight_layout()
    plt.show()"""
    
    #Zamik koordinat za boljso preglednost v gis-u. Koordinate se zamaknejo v treh smereh okoli prvotne koordinate za poljubno stevilo metrov. Koordinate z rumeno opozorilno vrednostjo se zamaknejo v spodnji levi kot trikotnika, oranzne v spodnjega desnega, rdece pa na vrh trikotnika
    """
    ali_zamaknem = query_yes_no('Zamik koordinat glede na poplavno nevarnost:')
    if ali_zamaknem == True:
        vrednost_zamika=raw_input('Za koliko metrov zamaknem tocke v trikotniku okoli koordinate? ')
        zamik_koordinat(data,vrednost_zamika)
        print 'Urejena tabela je izvozena v '+ txt_name_string
    else:
        print 'Pa drugic!'
    """
        
if __name__=="__main__":
    main()
