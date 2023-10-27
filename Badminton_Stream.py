import streamlit as st
#from streamlit_modal import Modal
import pandas as pd
import numpy as np
import os, sys

# install selenium
@st.experimental_singleton
def installff():
  os.system('sbase install geckodriver')
  os.system('ln -s /home/appuser/venv/lib/python3.7/site-packages/seleniumbase/drivers/geckodriver /home/appuser/venv/bin/geckodriver')

_ = installff()
# END install selenium

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options


st.header('Disponibilités')

##########################
# parameters
##########################
hreLookFrom = 17
timeLong = 1

#############
# selenium related
#############
delay = 10
delayPay = 20

# options available
tarif_std_text = "Tarif standard"
tarif_reduit_text = "Tarif réduit"
mode_payment_code = "Utiliser un code"
mode_payment_online = "Payer en ligne"
option_pay = "TWINT"
reserv_text = "Réserver"
reserv_terrain_text = "Réserver sans préférence"



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

       
##########################
# functions
##########################

#############
# selection interface
#############
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

def formatDate(d, format):
    dmap = {0:'Lun',1:'Mar',2:'Mer',3:'Jeu',4:'Ven',5:'Sam',6:'Dim'}
    dDate = pd.to_datetime(d)
    prtDate = dDate.strftime(format) 
    return prtDate

def formatFRHre(h):
    prtHre = str(int(h))+"h"
    return prtHre

def reserv_url(url, date, duree):
    url = url.replace('MyjDate',str(date))
    url = url.replace('MyjTime',str(duree))
    return url

def reserv_bad(date, duree):
    linkBad = 'https://node.agenda.ch/api_front/pro_users/availabilities?company_id=7910&locale=fr&date=MyjDate&range=3months&bookables%5B0%5D%5Bid%5D=MyjTime&bookables%5B0%5D%5Btype%5D=Service&agenda_id=anyone&as_minutes=true&location_ids%5B0%5D=1047&simultaneous_count=1&returning_customer=true&_=1677363720387'
    return reserv_url(linkBad, date, duree)

def reserv_squash(date, duree):
    linkSquash = 'https://node.agenda.ch/api_front/pro_users/availabilities?company_id=7910&locale=fr&date=MyjDate&range=3months&bookables%5B0%5D%5Bid%5D=MyjTime&bookables%5B0%5D%5Btype%5D=Service&agenda_id=anyone&as_minutes=true&location_ids%5B0%5D=1047&simultaneous_count=1&returning_customer=true&_=1677363720387'
    return reserv_url(linkSquash, date, duree)

def display_link_reserv(date, hre):
    return "a" #"<a href='#' id='link-reserv'>"+formatFRHre(hre)+"</a>", unsafe_allow_html=True, on_click=run_reserv(date,hre)"

def run_reserv(date, hre):
    #modal = Modal(key="Demo Key",title="Réserve")
    print("date",date)
    print("hre",hre)


#############
# selenium related
#############

def by_class_delayed(browser, delay, class_name):
    elem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CLASS_NAME, class_name)))
    return elem

def get_center(key):
    centers = browser.find_elements(By.CLASS_NAME, "item-0-2-108")
    for c in centers:
        sect = c.find_element(By.CLASS_NAME, "title-0-2-104")
        if key in sect.text:
            buttons = c.find_elements(By.CLASS_NAME, "actionButton-0-2-110")
            for b in buttons:
                if b.text.strip() == "Choisir":
                    return b
    return None

def get_reserv_tarif(key):
    reservs = browser.find_elements(By.CLASS_NAME, "priceLabel-0-2-200")
    for r in reservs:
        #sect = c.find_element(By.CLASS_NAME, "title-0-2-104")
        print("get_reserv_tarif",r.text)
        if key in r.text:
            print("----")
            parent = r.find_element(By.XPATH, '..')
            print("------")
            print(parent.get_attribute("class"))
            btnSelectTarif = parent.find_element(By.CLASS_NAME,"selectButton-0-2-207")
            return btnSelectTarif
    return None

def get_reserv_terrain(key):
    reservs = browser.find_elements(By.CLASS_NAME, "anyButton-0-2-209")
    for r in reservs:
        print("get_reserv_terrain",r.text)
        if key in r.text:
            return r
    return None

def get_reserv_week(date_to_find):
    date_picker = browser.find_element(By.CLASS_NAME, "input-0-2-259")
    date_picker.click()

    # TODO : date ==> "Choose jour jj mois aaaa" (!case sensitive! user upper)
    #date_to_find = date "Choose vendredi 27 octobre 2023"
    # date_class_name = "react-datepicker__day available-0-2-256 day-0-2-253 react-datepicker__day--025"
    
    elmnts = browser.find_elements(By.CSS_SELECTOR, '*')
    for el in elmnts: 
            display_date = el.get_attribute("aria-label")
            if display_date == date_to_find:
                print("get_reserv_week",display_date)
                return el
    return None


def get_reserv_date(date, hre):
    # TODO : date ==> "JOU. jj" OU "aujourd'hui" (!case sensitive! user upper)
    date_to_find = date
    # TODO : hre ==> hreh00
    hre_to_find = hre+"00"
    print("date_to_find:"+date_to_find)
    print("hre_to_find:"+hre_to_find)

    days_header = browser.find_elements(By.CLASS_NAME, "columnHeader-0-2-265")
    id_col_day = 0
    # print(id_col_day)
    for day_head in days_header:
        if day_head.text != "":
            id_col_day = id_col_day+1
            #print(id_col_day, day_head.text)

        if day_head.text == date_to_find:
            break

    print("id_col_day:",id_col_day)

    id_col_day = id_col_day-1
    table = browser.find_elements(By.TAG_NAME, "tbody")[1]
    #print("table.text: ",table.text)
    col = table.find_elements(By.TAG_NAME, "td")[id_col_day]
    print("col.text: ",col.text)
    lines = col.find_elements(By.CSS_SELECTOR,"*")
    for l in lines:
        print("l.text: ",l.text)
        if l.text.strip() == hre_to_find.strip():
            print("Trouve:",l.text)
            return l
    return None

      
# linkBad = linkBad.replace('MyjDate',str(jDate))
# linkBad = linkBad.replace('MyjTime',str(jTimeBad))
# linkSquash = linkSquash.replace('MyjDate',str(jDate))
# linkSquash = linkSquash.replace('MyjTime',str(jTimeSquash))
linkBad = reserv_bad(str(jDate),str(jTimeBad))
#print(linkBad) #check
linkSquash = reserv_squash(str(jDate),str(jTimeBad))
#print(link) #check


# if st.button ("my-link"):
#     st.write("Link clicked!")

if __name__ == "__main__":
    #print(formatFRDate(jDate)) #check
    #print(header) #check

    #############
    #tests
    #############
    # st.write("<a href='#/date=25' id='my-link'>Réserve</a>", unsafe_allow_html=True, on_click=run_reserv(25,19))
    # st.write("Réserve: ",linkBad) #on_click=run_reserv('25.10.2023','19'))


    urlParams = st.experimental_get_query_params()
    #st.write("Params:",urlParams)
    #print(urlParams.__len__)
    if len(urlParams)>0:
        date_choosed = urlParams ['date'][0]
        hre_choosed = str(int(float(urlParams ['hre'][0])))
        sport_choosed = urlParams ['sport'][0]
        print(sport_choosed+" the "+date_choosed+" at "+hre_choosed)

        # define variables
        date_format1 = "Mar 31.10.2023"
        date_format2 = "MAR. 31"
        date_format3 = "Choose mardi 31 octobre 2023"
        hre_format = hre_choosed+"h"
        email_reserv = "test@test.com"

        print(date_format1)
        print(date_format2)
        print(date_format3)
        print(hre_format)
        print(email_reserv)

        tarif_text = tarif_reduit_text
        mode_payment_text = mode_payment_online
        
        options = Options()
        options.add_argument("--headless=new")
        browser = webdriver.Firefox(options=options)

        if sport_choosed == "bad":
            uri = linkReservBad
        elif sport_choosed == "squash":
            uri = linkReservSquash
        
        if len(uri)>0:
            browser.get(uri)

            conditions = by_class_delayed(browser, delay, "acceptButton-0-2-7")
            conditions.click()

            by_class_delayed(browser, delay, "item-0-2-108")
            center = get_center("Queue")
            center.click()

            els = browser.find_elements(By.CSS_SELECTOR, '*')
            for x in els: 
                if x.text == reserv_text:
                    print("-",reserv_text,x.text)
                    print("--",x.get_attribute("class"))
                    if x.get_attribute("class") == "actionButton-0-2-171":
                        print(reserv_text,"click")
                        x.click()
                        break

            reserv_tarif = get_reserv_tarif(tarif_text)
            reserv_tarif.click()

            reserv_terrain =  get_reserv_terrain(reserv_terrain_text)
            reserv_terrain.click()

            choose_week = get_reserv_week(date_format3)
            choose_week.click()

            choose_date = get_reserv_date(date_format2, hre_format)
            choose_date.click()

            email_field = by_class_delayed(browser, delay, "input-0-2-301")
            # email_field = browser.find_element(By.CLASS_NAME, "input-0-2-301")
            email_field.send_keys(email_reserv)

            btn_submit = browser.find_element(By.CLASS_NAME, "submitButton-0-2-304")
            btn_submit.click()

            check_boxes = browser.find_elements(By.CSS_SELECTOR,"input[type='checkbox']")
            for c in check_boxes:
                print(c.text)
                c.click()


            # pay_btns = browser.find_elements(By.CLASS_NAME, "submitButton-0-2-322")
            # for b in pay_btns:
            #     print(b.text)
            #     if b.text == mode_payment_text:
            #         b.click()

            # TODO : select payment TWINT
            # #pay_options = browser.find_elements(By.CLASS_NAME, "payment-method has-description active")
            # pay_options = by_class_delayed(browser, delayPay, "payment-method has-description active")
            # for o in pay_options:
            #     print(o.text)
            #     if o.text.strip() == option_pay:
            #         o.click()
                
            # btn_pay = browser.find_element(By.CLASS_NAME,"btn btn-rounded btn-primary btn-block payment-submit")
            # print(btn_pay.text)

    

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
        formatDay = formatDate(i, "%Y%m%d")
        dayHres = dfHres[i]    
        bDisplayedDay = False
        
        st.write(displayDay+": ")
        
        for hre in dayHres:
            if hre.is_integer :
                if hre>=hreLookFrom:
                    # if not bDisplayedDay:
                    #     displayLine = displayDay+": "+formatFRHre(hre)
                    #     bDisplayedDay = True
                    # else:
                        #displayLine = displayLine+", "+display_link_reserv(formatDay, hre)
                        st.write("<a target='#' href='?sport=bad&date="+formatDay+"&hre="+str(hre)+"' id='link-reserv'>"+formatFRHre(hre)+"</a>", unsafe_allow_html=True)
                        # , on_click=run_reserv(formatDay,hre))
                        #print(displayLine)
                        # st.write("<a href='#/date=25' id='my-link'>"+formatFRHre(hre)+"</a>", unsafe_allow_html=True, on_click=run_reserv(25,19))
        # if len(displayLine)>0:
        #     print(displayLine)
        #     st.write(displayLine)

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


