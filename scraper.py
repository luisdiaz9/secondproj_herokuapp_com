#!/usr/bin/env python
# coding: utf-8

# In[1]:



from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import pandas as pd
import numpy as np
import time
import re
from ast import literal_eval
from datetime import timedelta, date, datetime

DataToHTML = {}

# In[2]:
def init_browser(): 
        executable_path = {'executable_path': 'chromedriver.exe'}
        return Browser('chrome', **executable_path, headless=False)

def scrape_last(fecha):
    token = '183d3cd0c2c6b81223aa6a1d99b7384c9ad21db4086ca76d388602fed844bc2b';
    start_date = date.today()
    date_before = start_date- timedelta(days=1)
    query1 = 'https://www.banxico.org.mx/SieAPIRest/service/v1/series/'+'SF43787'+'/datos/'+str(date_before)+'/'+str(date_before)+'?token='+token;
    country_info = requests.get(query1).json()
    
    
    
    print(fecha)
    date_object = datetime.strptime(fecha, '%Y-%m-%d')
    print(date_object)
    print(date_object.ctime())
    print(date_object.year)
    print(date_object.month)
    print(date_object.day)
    print('{:02d}'.format(date_object.day))
    date_object1 = datetime.strftime(date_object,'%b').upper()
    print(date_object1)
    try: 
        browser = init_browser()
        browser.driver.set_window_size(100, 100)
        # In[3]:
        aeropuertos = ["CUN","HAV","ORD","JFK","LAX","BCN","MAD","YYZ","MCO","SFO","LAS","MUC","YUL","MIA","DEN"] 
        urls = []
        for x in aeropuertos:
            amx_url = f"https://aeromexico.com/es-mx/reserva/opciones?itinerary=MEX_{x}_{date_object.year}-{date_object.month}-{'{:02d}'.format(date_object.day)}&leg=1&travelers=A1_C0_I0_PH0_PC0"
            urls.append(amx_url)
            print(amx_url)


        # In[4]:


        amx_data = []

        for x in urls:
            browser.visit(x)
            time.sleep(8)
            try:
                browser.find_by_xpath("/html/body/div[2]/div/div/div[1]/div/div[1]/div/div/button").click()
            except:
                print("ok")
            amx_site = browser.html
            amx_soup = bs(amx_site, 'html.parser')
            options = amx_soup.find_all('div', class_="FlightOptionsListItem")
            print("appending")
            amx_data.append(options)


        # In[5]:


        precios = []
        origenes = []
        destinos = []
        salidas = []
        llegadas = []

        for x in amx_data:
            for y in x:
                precio = y.find('div', class_='FlightOptionsFare-price')
                origen = y.find_all('div', class_='FlightOptionsTimeline-city')
                horario = y.find_all('div', class_='FlightOptionsTimeline-time')
                try:
                    precios.append(precio.span.text.replace("$","").replace(",",""))
                    origenes.append(origen[0].text)
                    destinos.append(origen[1].text)
                    salidas.append(horario[0])
                    llegadas.append(horario[1])
                except:
                    continue


        # In[6]:


        salidas2 = []

        for x in salidas:
            try:
                salidas2.append(x.text)
            except:
                continue


        # In[7]:


        llegadas2 = []

        for x in llegadas:
            try:
                llegadas2.append(x.text)
            except:
                continue


        # In[8]:


        df = pd.DataFrame({
        "Origen": origenes,
        "Destino": destinos,
        "Hora_Salida": salidas2,
        "Hora_Llegada": llegadas2,
        "Desde": precios,
        "Dmxn": datetime.strftime(start_date,'%Y/%m/%d'),
        "Mxn": 1,
        "No": datetime.strftime(date_object,'%Y-%m-%d')
        })


        # In[9]:


        df["Desde"] = pd.to_numeric(df["Desde"])


        # In[10]:


        grouped_df = df.groupby(["Hora_Salida","Destino"])
        amx_grouped = grouped_df.min()


        # In[11]:


        amx_grouped.reset_index(inplace=True)


        # In[12]:



        for x in aeropuertos:
            amx_url = f"https://sales.avianca.com/B2C/InicioAmadeus.aspx?cco=MEX&Pais=MX&lan=ES&tv=false&fi={'{:02d}'.format(date_object.day)}{date_object1}&FFL=false&ccd={x}&fr={'{:02d}'.format(date_object.day)}{date_object1}&Cabina=0&na=1&nn=0&ni=0&VInt=si&tt=4&ccorp=0&hvi=0&hvr=0&tarifa=0&SistemaOrigen=AH&FriendlyID=&FriendlyIDNegoF=&WS=&MPD=0&IvaMPD=0&descq=0&Device=web"
            urls.append(amx_url)
            print(amx_url)


        # In[13]:


        avi_prices = []
        avi_horarios = []

        for x in urls:
            browser.visit(x)
            time.sleep(8)
            avi_site = browser.html
            avi_soup = bs(avi_site, 'html.parser')
            avi_prices.append(avi_soup.find_all('div', class_='availability-list-fares'))
            avi_horarios.append(avi_soup.find_all('div', class_='flight-details availability-flight-details flight-details-without-button availability-flight-details-without-button row'))
            print("appending")


        # In[14]:


        precios = []

        for x in avi_prices:
            for y in x:
                precios.append(y.find('div', class_='cell-reco-price').span.text.replace(",","").replace(".00",""))


        # In[15]:


        salidas = []
        llegadas = []
        origenes = []
        destinos = []

        for x in avi_horarios:
            for y in x:
                salidas.append(y.find('time', class_='time-from').text)
                llegadas.append(y.find('time', class_='time-to').text)
                origenes.append(y.find('abbr', class_='citycode-from').text.replace("(","").replace(")",""))
                destinos.append(y.find('abbr', class_='citycode-to').text.replace("(","").replace(")",""))


        # In[16]:


        df2 = pd.DataFrame({
        "Origen": origenes,
        "Destino": destinos,
        "Hora_Salida": salidas,
        "Hora_Llegada": llegadas,
        "Desde": precios,
        "Dmxn": datetime.strftime(start_date,'%Y/%m/%d'),
        "Mxn": 1,
        "No": datetime.strftime(date_object,'%Y-%m-%d')
        })


        # In[17]:


        df2["Desde"] = [literal_eval(x) for x in df2["Desde"]]


        # In[18]:


        df2["Desde"] = pd.to_numeric(df2["Desde"])


        # In[19]:


        grouped_df2 = df2.groupby(["Hora_Salida", "Destino"])
        avi_grouped = grouped_df2.min()


        # In[20]:


        avi_grouped.reset_index(inplace=True)


        # In[21]:



        urls = []
        for x in aeropuertos:
            ua_url = f"https://www.united.com/ual/en/MX/flight-search/book-a-flight/results/rev?f=MEX&t={x}&d={date_object.year}-{date_object.month}-{'{:02d}'.format(date_object.day)}&tt=1&sc=7&px=1&taxng=1&newHP=True&idx=1"
            urls.append(ua_url)
            print(ua_url)


        # In[22]:


        ua_data = []

        for x in urls:
            browser.visit("https://www.united.com/en/mx/")
            time.sleep(8)
            browser.visit(x)
            time.sleep(20)
            united_site = browser.html
            united_soup = bs(united_site, 'html.parser')
            print("appending")
            ua_data.append(united_soup.find_all('li', class_='flight-block flight-block-fares use-roundtrippricing flight-block-revised'))


        # In[23]:


        salidas = []
        llegadas = []
        origenes = []
        destinos = []
        precios = []

        for x in ua_data:
            for y in x:
                xx = y.find('div', class_='flight-time flight-time-depart').text
                xy = y.find('div', class_='flight-time flight-time-arrive').text
                xz = y.find_all('span')
                xw = (y.find('div', class_='price-point price-point-revised use-roundtrippricing').text)
                salidas.append(re.search(r'\d{1,2}(:\d{1,2})', xx).group())
                llegadas.append(re.search(r'\d{1,2}(:\d{1,2})', xy).group())
                origenes.append(xz[1].text)
                destinos.append(xz[3].text)
                precios.append(xw[25:-17].replace(',',''))


        # In[24]:


        precios2 = [x.strip(' ') for x in precios]

        # In[25]:


        df3 = pd.DataFrame({
        "Origen": origenes,
        "Destino": destinos,
        "Hora_Salida": salidas,
        "Hora_Llegada": llegadas,
        "Desde": precios2 ,
        "Dmxn": country_info['bmx']['series'][0]['datos'][0]['fecha'],
        "Mxn": country_info['bmx']['series'][0]['datos'][0]['dato'],
        "No": datetime.strftime(date_object,'%Y-%m-%d')
        })
    
        df3["Origen"] = df3["Origen"].str[-4:]
        df3["Destino"] = df3["Destino"].str[-4:]
        df3["Origen"] =df3["Origen"].str[:3]
        df3["Destino"] = df3["Destino"].str[:3]
        df3["Desde"] = pd.to_numeric(df3["Desde"])
        df3.dropna(inplace=True)
        df3["Desde"] = pd.to_numeric(df3["Desde"]).astype('int64')
        df3["Hora_Salida"] = df3["Hora_Salida"].apply('{0:0>5}'.format)
        df3["Hora_Llegada"] = df3["Hora_Llegada"].apply('{0:0>5}'.format)


        # In[26]:


        grouped_df3 = df3.groupby(["Hora_Salida", "Destino"])
        ual_grouped = grouped_df3.min()


        # In[27]:


        ual_grouped.reset_index(inplace=True)


        # In[32]:


        amx_grouped["Name"] = "AMX"


        # In[37]:


        avi_grouped["Name"] = "AVI"


        # In[39]:


        ual_grouped["Name"] = "UAL"


        # In[98]:


        df4 = amx_grouped.append(avi_grouped, ignore_index=True)


        # In[99]:


        df5 = df4.append(ual_grouped, ignore_index = True)


        # In[101]:


        conditions = [
            (df5["Destino"] == "CUN"),
            (df5["Destino"] == "HAV"),
            (df5["Destino"] == "ORD"),
            (df5["Destino"] == "JFK"),
            (df5["Destino"] == "LAX"),
            (df5["Destino"] == "BCN"),
            (df5["Destino"] == "MAD"),
            (df5["Destino"] == "YYZ"),
            (df5["Destino"] == "MCO"),
            (df5["Destino"] == "SFO"),
            (df5["Destino"] == "LAS"),
            (df5["Destino"] == "MUC"),
            (df5["Destino"] == "YUL"),
            (df5["Destino"] == "MIA"),
            (df5["Destino"] == "DEN"),
            (df5["Destino"] == "YJB"),
            (df5["Destino"] == "EWR"),
            (df5["Destino"] == "LGA")
        ]

        lat_choices = [21.040358,
                    22.991455,
                    41.974166,
                    40.641235,
                    33.941562,
                    41.297781,
                    40.498324,
                    43.677764,
                    28.431205,
                    37.621313,
                    36.084026,
                    48.353598,
                    45.465610,
                    25.795814,
                    39.856121,
                    41.3789,
                    40.689588,
                    40.777065]

        lon_choices = [-86.873455,
                    -82.410321,
                    -87.907300,
                    -73.778263,
                    -118.408412,
                    2.083530,
                    -3.567469,
                    -79.624959,
                    -81.308008,
                    -122.378988,
                    -115.153889,
                    11.775135,
                    -73.745299,
                    -80.287169,
                    -104.673641,
                    2.1400,
                    -74.174430,
                    -73.873987]


        # In[102]:


        df5["Lat"] = np.select(conditions, lat_choices, default="N/A")


        # In[105]:


        df5["Lon"] = np.select(conditions, lon_choices, default="N/A")




        # In[109]:


        df5.to_csv("consolidated_01102019.csv")


        # In[111]:


        df5.to_json("consolidated_json_01102019.js", orient="records")
        DataToHTML = df5.to_json()

        return DataToHTML
        # In[ ]:
    finally:
        browser.quit()


