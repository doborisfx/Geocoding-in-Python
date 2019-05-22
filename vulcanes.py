import folium
import pandas as pd
import os
import json



US_Unemployment_Oct2012 = os.path.join('.', 'us_unemployment.csv')
unemployment = pd.read_csv(US_Unemployment_Oct2012)
#unemployment.head(5)

us_states = os.path.join('.', 'us-states.json')
geo_json_data = json.load(open(us_states))

vdata = pd.read_csv('volcanoes.txt')
def colorProducer(elevation):
    if elevation < 1000:
        return "green"
    elif 1000 <= elevation < 3000:
        return "orange"
    else:
        return "red"

lat = list(vdata['LAT'])
lon = list(vdata['LON'])

m = folium.Map(location=[30.281140, -97.734285],zoom_start=4,tiles="Mapbox Bright")
folium.Choropleth(
    name='choropleth',
    #geo_data=open("world.json",'r',encoding="utf-8-sig").read(),
    geo_data=geo_json_data,  #geopandas.read_file(us_states),
    data=unemployment,
    columns=['State', 'Unemployment'],
    key_on='feature.id',
    fill_color='YlGn',
    fill_opacity=0.3,
    line_opacity=0.2,
    line_weight=2,
    legend_name='Unemployment Rate %'
).add_to(m)

#feature group to grup together the group of points
fg=folium.FeatureGroup(name="Volcanoes")
#for the population or pop2005 we also can build other feature grop and added to the maps
# or just as i did.... fgp=folium.FeatureGroup(name="population") and ....
#look here to customize or see how is done....
#http://geojson.io/#map=2/20.0/0.0
m.add_child(folium.GeoJson(name="Population",data=open("world.json",'r',encoding="utf-8-sig").read(),
    style_function=lambda x: {'fillColor':
         'Limw'   if x['properties']['POP2005'] < 1000000
    else 'DarkCyan'  if 1000000 <= x['properties']['POP2005'] < 5000000
    else 'green'  if 5000000 <= x['properties']['POP2005'] < 10000000
    else 'forest'  if 10000000 <= x['properties']['POP2005'] < 20000000
    else 'orange'  if 20000000 <= x['properties']['POP2005'] < 30000000
    else 'tomato'     if 30000000 <= x['properties']['POP2005'] < 60000000
    else 'red'
    }
    ))

irow=0
# for lt,ln,el in zip(lat,lon)):
disp="!"
while disp != "c" and  disp !="m":
    disp=input("Enter Markers type (Circle='C' or Marker='m')?")
for lt,ln,el in zip(lat,lon,list(vdata['ELEV'])):
    html=f"""<h4>Volcano information:</h4>
        Name {vdata.NAME[irow]} Volcano
        <a href="https://www.google.com/search?q=({lt},{ln})" target="_blank"> ({lt},{ln}) </a>
        </BR>in {vdata.LOCATION[irow]}</BR>Elevation {el} m"""
    if disp=="c":
        fg.add_child(
            # ------------------------------------------------------
            folium.CircleMarker(
                    location=[lt, ln],
                    radius=10,
                    popup=html,
                    fill="true",
                    fill_color=colorProducer(el),
                    color=colorProducer(el),
                    fill_opacity=0.7
                    ,tooltip=f"Name {vdata.NAME[irow]} Volcano</Br>Press Click for more Info.")
                    # ------------------------------------------------------
        )
    else:
        fg.add_child(
                        folium.Marker(location=[lt, ln],
                        popup=html,
                        icon=folium.Icon(color=colorProducer(el)),
                        tooltip=f"Name {vdata.NAME[irow]} Volcano</Br>Press Click for more Info."
                        )
        )
                        ##------------------------------------------------------
        # fg.add_child(
                        # folium.Marker(
                        #                 location=[lt,ln],
                        #                 # popup=f"Hi I am the ({lt},{ln})<br/>Name {vdata.iloc[irow,2]} in {vdata.iloc[irow,3]} ",
                        #                 # popup=f"Hi I am {vdata.NAME[irow]} Volcano <BR/><a url='https://www.google.com/maps/search?q='''({lt},{ln})''''> ({lt},{ln}) </a><br/> in {data.LOCATION[irow]}<BR/>Elevation {data.ELEV[irow]} m ",
                        #                 popup=html,
                        #                 icon=folium.Icon(color='blue')
                        #               )
        # )
                        # ------------------------------------------------------
    irow += 1
m.add_child(fg)


m.add_child(folium.LayerControl())
m.save("vulcanos.html")
