#importing various libraries used
import pandas as pd
import numpy as np
import requests
import json
import plotly.express as px
import datetime
import chart_studio.plotly as py
import plotly.graph_objs as go 
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, plot

df1 = pd.read_csv("http://api.covid19india.org/csv/latest/vaccine_doses_statewise_v2.csv")

#Date and Time Management Stuff
todayfinal = datetime.datetime.strptime("Oct 31 2021","%b %d %Y")
td = todayfinal.strftime("%d/%m/%Y")
use_date = todayfinal.strftime("%d %B %Y")
mainframe=df1[df1['Vaccinated As of'] == td]

mainframe.set_index('State',inplace=True)


mainframe.drop('Dadra and Nagar Haveli and Daman and Diu',axis=0,inplace = True)
mainframe.drop('Miscellaneous',axis=0,inplace = True)
mainframe.drop('Total',axis=0,inplace = True)
mainframe.drop('Ladakh',axis=0,inplace = True)
mainframe.reset_index(inplace = True)
#mainframe.info()


india_states = json.load(open('states_india.geojson','r'))
state_id_map = {}
for feature in india_states["features"]:
    feature["id"] = feature["properties"]["state_code"]
    state_id_map[feature["properties"]["st_nm"]] = feature["id"]
    
    

state_id_map['Delhi'] = state_id_map.pop('NCT of Delhi')
state_id_map['Andaman and Nicobar Islands'] = state_id_map.pop('Andaman & Nicobar Island')
state_id_map['Jammu and Kashmir'] = state_id_map.pop('Jammu & Kashmir')
state_id_map['Arunachal Pradesh'] = state_id_map.pop('Arunanchal Pradesh')
state_id_map.pop('Dadara & Nagar Havelli')
state_id_map.pop('Daman & Diu')
mainframe['id'] = mainframe['State'].apply(lambda x:state_id_map[x])

newent = "417036 53903393 1570458 35607039 124799926 1158473 29436231 18710922 1586250 63872399 28204692 7451955 13808320 38593948 67562686 35699443 73183 85358965 123144223 3091545 3366710 1097206 2249695 46356334 1413542 30141373 81032689 690251 77841267 39362732 4169794 237882725 11250858 99276115".split()
lister = []
for x in newent:
    lister.append(int(x))
newent = []
newent = lister
#print(len(newent))
#print(newent)

mainframe["Total Population"] = newent
mainframe['Complete Vaccination vs First Dose'] = mainframe['Second Dose Administered'] / mainframe['Total Doses Administered'] * 100
mainframe['Percentage of Vaccination Completion'] = (mainframe['First Dose Administered']/mainframe['Total Population'])*100

#Maps
#1
#Tells us about the statewise population who are getting vaccinated
fig = px.choropleth(mainframe,locations='id',
                    geojson=india_states,
                    title=f'Vaccination Status India(as of {use_date})',
                    color='Percentage of Vaccination Completion',
                    scope='asia',
                    hover_name='State',
                    #color_continuous_scale='delta',
                    hover_data=['First Dose Administered'],
                   )
fig.update_geos(fitbounds='locations',visible=False)
plot(fig)

#2
#Tells us how many people are getting completely vaccinated over those getting one dose
fig1 = px.choropleth(mainframe,locations='id',
                    geojson=india_states,
                    title=f'Complete Vaccination vs First Dose Administered(as of {use_date})',
                    color='Complete Vaccination vs First Dose',
                    scope='asia',
                    hover_name='State',
                    color_continuous_scale='rainbow',
                    hover_data=['First Dose Administered'],
                   )
fig1.update_geos(fitbounds='locations',visible=False)
plot(fig1)
