import streamlit as st
import pandas as pd
import numpy as np

st.header('Disponibilités')

#############
#parameters
#############
hreLookFrom = 17
timeLong = 1

hreLookFrom = st.slider('A partir de quelle heure ?', min_value=8, max_value=21, value=18, step=1)

from datetime import datetime
jDate = datetime.now().strftime("%Y-%m-%d")
#print(jDate) #check

if timeLong == 1:
    jTimeBad = 53896
else:
    jTimeBad = 64693

if timeLong == 1:
    jTimeSquash = 53899
#else:    jTimeBad = 64693

linkReservBad = 'https://book.agenda.ch/services/pick/'+str(jTimeBad)+'?companyId=7910'
linkReservSquash = 'https://book.agenda.ch/services/pick/'+str(jTimeSquash)+'?companyId=7910'

linkBad = 'https://node.agenda.ch/api_front/pro_users/availabilities?company_id=7910&locale=fr&date=MyjDate&range=3months&bookables%5B0%5D%5Bid%5D=MyjTime&bookables%5B0%5D%5Btype%5D=Service&agenda_id=anyone&as_minutes=true&location_ids%5B0%5D=1047&simultaneous_count=1&returning_customer=true&_=1677363720387'
linkSquash = 'https://node.agenda.ch/api_front/pro_users/availabilities?company_id=7910&locale=fr&date=MyjDate&range=3months&bookables%5B0%5D%5Bid%5D=MyjTime&bookables%5B0%5D%5Btype%5D=Service&agenda_id=anyone&as_minutes=true&location_ids%5B0%5D=1047&simultaneous_count=1&returning_customer=true&_=1677363720387'
       
linkBad = linkBad.replace('MyjDate',str(jDate))
linkBad = linkBad.replace('MyjTime',str(jTimeBad))
linkSquash = linkSquash.replace('MyjDate',str(jDate))
linkSquash = linkSquash.replace('MyjTime',str(jTimeSquash))
#print(link) #check

        
def showHre(cell):    
    if str(type(cell)).strip()!="<class 'NoneType'>":
        dict = cell
        hre = cell['start']
        hre = hre / 60
        return hre

def formatFRDate(d):
    dmap = {0:'Lun',1:'Mar',2:'Mer',3:'Jeu',4:'Ven',5:'Sam',6:'Dim'}
    dDate = pd.to_datetime(d)
    prtDate = dmap[dDate.dayofweek]+" "+dDate.strftime("%d.%m.%Y")
    return prtDate

def formatFRHre(h):
    prtHre = str(int(h))+"h"
    return prtHre

#print(formatFRDate(jDate)) #check
#print(header) #check

df = pd.read_json(linkBad,orient='index')
#print(df.head(10)) #check

dfHres = df.applymap(lambda c : showHre(c)).transpose()
#print(dfHres.head(10)) #check

headerBad = "**_Badminton_** dès "+formatFRHre(hreLookFrom)+" (pour "+str(timeLong)+"h):"
#print(header) #check
st.markdown(headerBad)
for i in dfHres.columns:
    displayLine = ""
    displayDay = formatFRDate(i)
    dayHres = dfHres[i]    
    bDisplayedDay = False
    
    
    for hre in dayHres:
        if hre.is_integer :
            if hre>=hreLookFrom:
                if not bDisplayedDay:
                    displayLine = displayDay+": "+formatFRHre(hre)
                    bDisplayedDay = True
                else:
                    displayLine = displayLine+", "+formatFRHre(hre)
    if len(displayLine)>0:
        #print(displayLine)
        st.text(displayLine)

st.write("Réserve Badminton: "+linkReservBad)	


df = pd.read_json(linkSquash,orient='index')
#print(df.head(10)) #check

dfHres = df.applymap(lambda c : showHre(c)).transpose()
#print(dfHres.head(10)) #check
headerSquash = "**_Squash_** dès "+formatFRHre(hreLookFrom)+" (pour "+str(timeLong)+"h):"		
#print(headerSquash) #check
st.write(headerSquash)
for i in dfHres.columns:
    displayLine = ""
    displayDay = formatFRDate(i)
    dayHres = dfHres[i]    
    bDisplayedDay = False
    
    
    for hre in dayHres:
        if hre.is_integer :
            if hre>=hreLookFrom:
                if not bDisplayedDay:
                    displayLine = displayDay+": "+formatFRHre(hre)
                    bDisplayedDay = True
                else:
                    displayLine = displayLine+", "+formatFRHre(hre)
    if len(displayLine)>0:
        #print(displayLine)
        st.text(displayLine)
		
#print("Reserve : ",linkReserv) #check
st.write("Réserve Squash: "+linkReservSquash)

