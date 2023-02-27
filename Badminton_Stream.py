import streamlit as st
import pandas as pd
import numpy as np

st.title('Badminton')

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
    jTime = 53896
else:
    jTime = 64693


link = 'https://node.agenda.ch/api_front/pro_users/availabilities?company_id=7910&locale=fr&date=MyjDate&range=3months&bookables%5B0%5D%5Bid%5D=MyjTime&bookables%5B0%5D%5Btype%5D=Service&agenda_id=anyone&as_minutes=true&location_ids%5B0%5D=1047&simultaneous_count=1&returning_customer=true&_=1677363720387'
       
link = link.replace('MyjDate',str(jDate))
link = link.replace('MyjTime',str(jTime))
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

df = pd.read_json(link,orient='index')
#print(df.head(10)) #check

dfHres = df.applymap(lambda c : showHre(c)).transpose()
#print(dfHres.head(10)) #check

header = "Disponibilités dès "+formatFRHre(hreLookFrom)+" (pour "+str(timeLong)+"h):"
#print(header) #check
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
linkReserv = 'https://book.agenda.ch/services/pick/'+str(jTime)+'?companyId=7910'
#print("Reserve : ",linkReserv) #check
st.write("Réserve : "+linkReserv)

