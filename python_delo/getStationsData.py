#!/home/mmurko/anaconda2/bin/python
from oracleWrapper import *
import re,time
from datetime import timedelta

def main():
    
    startdate = sys.argv[1]
    enddate = sys.argv[2]
    outputdir = sys.argv[3]
    
    t_start = datetime.datetime.strptime(startdate, "%Y%m%d%H%M")
    t_end = datetime.datetime.strptime(enddate, "%Y%m%d%H%M") 

    t_start_str=datetime.datetime.strftime(t_start,"'%d. %m. %Y %H:%M'")
    t_end_str=datetime.datetime.strftime(t_end,"'%d. %m. %Y %H:%M'")    
   
    #### mareograf KP:
    ### air temperature:
    # db = oracleWrapper("hidpro")
    # oracle_data = db.select("select to_char(datum,'dd.mm.yyyy HH24:MI') as datum , vred as temp from podatki where postaja='M38'\
    # and parameter=10 and datum between to_date("+t_start_str+",'dd. mm. yyyy HH24:MI') and to_date("+t_end_str+",'dd. mm. yyyy HH24:MI')\
    # order by datum asc")
    # db.close_connection()
    # data = pd.DataFrame(oracle_data,columns=["cas","temp"]) 
    # data=data.set_index("cas")  
    # data.to_csv(outputdir +'/mareografKP_Tair_'+startdate + '-'+enddate+'.txt','\t')

    ### wind:
    # db = oracleWrapper("hidpro")
    # oracle_data = db.select("select to_char(datum,'dd.mm.yyyy HH24:MI') as datum , vred as hitrost, svred as smer from podatki_veter where postaja='M38'\
    # and parameter=100 and datum between to_date("+t_start_str+",'dd. mm. yyyy HH24:MI') and to_date("+t_end_str+",'dd. mm. yyyy HH24:MI')\
    # order by datum asc")
    # db.close_connection()
    # data = pd.DataFrame(oracle_data,columns=["cas","hitrost","smer"])   
    # data=data.set_index("cas")  
    # data.to_csv(outputdir +'/mareografKP_veter_'+startdate + '-'+enddate+'.txt','\t')

    ### sea surface temperature:
    # db = oracleWrapper("hidpro")
    # oracle_data = db.select("select to_char(datum,'dd.mm.yyyy HH24:MI') as datum , vrednost as SST from podatki_ott where postaja='H24'\
    # and parameter=330 and datum between to_date("+t_start_str+",'dd. mm. yyyy HH24:MI') and to_date("+t_end_str+",'dd. mm. yyyy HH24:MI')\
    # order by datum asc")
    # db.close_connection()
    # data = pd.DataFrame(oracle_data,columns=["cas","SST"])  
    # data=data.set_index("cas")  
    # data.to_csv(outputdir +'/mareografKP_SST_'+startdate + '-'+enddate+'.txt','\t')

    ### vodostaj:
    db = oracleWrapper("hidpro")
    oracle_data = db.select("select to_char(datum,'dd.mm.yyyy HH24:MI') as datum , vrednost as visina from podatki_ott where postaja='H24'\
    and parameter=362 and datum between to_date("+t_start_str+",'dd. mm. yyyy HH24:MI') and to_date("+t_end_str+",'dd. mm. yyyy HH24:MI')\
    order by TO_DATE(datum,'dd.mm.yyyy HH24:MI') asc")
    db.close_connection()
    data = pd.DataFrame(oracle_data,columns=["cas","visina"])  
    data=data.set_index("cas")  
    data.to_csv(outputdir +'/mareografKP_vodostaj2006-2018_362.txt','\t')
    #./getStationsData.py 201701010000 201801010000 .

    ### zracni pritisk:
    # db = oracleWrapper("hidpro")
    # oracle_data = db.select("select to_char(datum,'dd.mm.yyyy HH24:MI') as datum , vred as pritisk from podatki where postaja='M38'\
    # and parameter=47 and datum between to_date("+t_start_str+",'dd. mm. yyyy HH24:MI') and to_date("+t_end_str+",'dd. mm. yyyy HH24:MI')\
    # order by datum asc")
    # db.close_connection()
    # data = pd.DataFrame(oracle_data,columns=["cas","pritisk"])  
    # data=data.set_index("cas")  
    # data.to_csv(outputdir +'/mareografKP_pritisk_'+startdate + '-'+enddate+'.txt','\t')

    ### relativna vlaznost:
    # db = oracleWrapper("hidpro")
    # oracle_data = db.select("select to_char(datum,'dd.mm.yyyy HH24:MI') as datum , vred as vlaznost from podatki where postaja='M38'\
    # and parameter=3 and datum between to_date("+t_start_str+",'dd. mm. yyyy HH24:MI') and to_date("+t_end_str+",'dd. mm. yyyy HH24:MI')\
    # order by datum asc")
    # db.close_connection()
    # data = pd.DataFrame(oracle_data,columns=["cas","vlaznost"])  
    # data=data.set_index("cas")  
    # data.to_csv(outputdir +'/mareografKP_vlaznost_'+startdate + '-'+enddate+'.txt','\t')


    ### soncno obsevanje:
    # db = oracleWrapper("hidpro")
    # oracle_data = db.select("select to_char(datum,'dd.mm.yyyy HH24:MI') as datum , vred as sevanje from podatki where postaja='M38'\
    # and parameter=4 and datum between to_date("+t_start_str+",'dd. mm. yyyy HH24:MI') and to_date("+t_end_str+",'dd. mm. yyyy HH24:MI')\
    # order by datum asc")
    # db.close_connection()
    # data = pd.DataFrame(oracle_data,columns=["cas","sevanje"])  
    # data=data.set_index("cas")  
    # data.to_csv(outputdir +'/mareografKP_sevanje_'+startdate + '-'+enddate+'.txt','\t')

    ### padavine (pol urne):
    # db = oracleWrapper("hidpro")
    # oracle_data = db.select("select to_char(datum,'dd.mm.yyyy HH24:MI') as datum , rr as padavine from podatki where postaja='M38'\
    # and parameter=7 and datum between to_date("+t_start_str+",'dd. mm. yyyy HH24:MI') and to_date("+t_end_str+",'dd. mm. yyyy HH24:MI')\
    # order by datum asc")
    # db.close_connection()
    # data = pd.DataFrame(oracle_data,columns=["cas","padavine"])  
    # data=data.set_index("cas")  
    # data.to_csv(outputdir +'/mareografKP_padavine_'+startdate + '-'+enddate+'.txt','\t')

    #### letalisce portoroz:
    ### wind:
    #db = oracleWrapper("hidpro")
    #oracle_data = db.select("select to_char(datum,'dd.mm.yyyy HH24:MI') as datum , vred as hitrost, svred as smer from podatki_veter where postaja='M08'\
    #and parameter=100 and datum between to_date("+t_start_str+",'dd. mm. yyyy HH24:MI') and to_date("+t_end_str+",'dd. mm. yyyy HH24:MI')\
    #order by datum asc")
    #db.close_connection()
    #data = pd.DataFrame(oracle_data,columns=["cas","hitrost","smer"])   
    #data=data.set_index("cas")  
    #data.to_csv(outputdir +'/letaliscePO_veter_'+startdate + '-'+enddate+'.txt','\t')
    
    ### air temperature:
    #db = oracleWrapper("hidpro")
    #oracle_data = db.select("select to_char(datum,'dd.mm.yyyy HH24:MI') as datum , vred as temp from podatki where postaja='M08'\
    #and parameter=10 and datum between to_date("+t_start_str+",'dd. mm. yyyy HH24:MI') and to_date("+t_end_str+",'dd. mm. yyyy HH24:MI')\
    #order by datum asc")
    #db.close_connection()
    #data = pd.DataFrame(oracle_data,columns=["cas","Tair"]) 
    #data=data.set_index("cas")  
    #data.to_csv(outputdir +'/letaliscePO_Tair_'+startdate + '-'+enddate+'.txt','\t')

    ### zracni pritisk:
    #db = oracleWrapper("hidpro")
    #oracle_data = db.select("select to_char(datum,'dd.mm.yyyy HH24:MI') as datum , vred as pritisk from podatki where postaja='M08'\
    #and parameter=47 and datum between to_date("+t_start_str+",'dd. mm. yyyy HH24:MI') and to_date("+t_end_str+",'dd. mm. yyyy HH24:MI')\
    #order by datum asc")
    #db.close_connection()
    #data = pd.DataFrame(oracle_data,columns=["cas","pritisk"])  
    #data=data.set_index("cas")  
    #data.to_csv(outputdir +'/letaliscePO_pritisk_'+startdate + '-'+enddate+'.txt','\t')


    
if __name__=='__main__':
    main()
