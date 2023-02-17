import streamlit as st
import pandas as pd
import numpy as np
from src.__address import Input
from src.__map import Map
from src.__frost import Frost
from src.__profet import Profet

#----------------------------------------------------------------------
# Settings
#----------------------------------------------------------------------
st.set_page_config(
    page_title="Bergvarmekalkulatoren",
    page_icon="src/bilder/icons8-dry-32.png",
    layout="centered",
    initial_sidebar_state="collapsed")

with open("styles/main.css") as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)
#----------------------------------------------------------------------
# Start App
#----------------------------------------------------------------------
st.button("Refresh")
st.title("Bergvarmekalkulatoren 2.0")
#----------------------------------------------------------------------
# GIS - ta inn flere WMS, analyser osv. 
#----------------------------------------------------------------------
st.header("Hvor befinner vi oss?")
# Adresse
input_obj = Input()
input_obj.process()
# Utetemperatur
frost_obj = Frost()
frost_obj.lat = input_obj.lat
frost_obj.long = input_obj.long
frost_obj.get_temperatures()
frost_obj.get_temperature_extremes()
# Kart 
map_obj = Map()
map_obj.address_lat = input_obj.lat
map_obj.address_long = input_obj.long
map_obj.address_postcode = input_obj.postcode
map_obj.address_name = input_obj.name
map_obj.weather_station_lat = frost_obj.weather_station_lat
map_obj.weather_station_long = frost_obj.weather_station_long
map_obj.weather_station_distance = frost_obj.weather_station_distance
map_obj.weather_station_name = frost_obj.weather_station_name
map_obj.weather_station_id = frost_obj.weather_station_id
map_obj.create_map()
#----------------------------------------------------------------------
# Temperatur
#----------------------------------------------------------------------
st.markdown("---")
st.header("Lufttemperatur")
st.line_chart(frost_obj.chart_data)
frost_obj.show_computed_temperatures()
#----------------------------------------------------------------------
# PROFet
#----------------------------------------------------------------------
st.markdown("---")
st.header("PROFet")
profet_obj = Profet()
profet_obj.air_temperature = frost_obj.median_series
profet_obj.area = st.number_input("Areal", value=200)
profet_obj.start_calculation()
chart_data = pd.DataFrame({
    "Romoppvarming" : profet_obj.space_heating_h,
    "Tappevann" : profet_obj.dhw_h,
    })
st.area_chart(chart_data)
st.write(f"Romoppvarmingsbehov: {int(np.sum(profet_obj.space_heating_h))} kWh")
st.write(f"Tappevannsbehov: {int(np.sum(profet_obj.dhw_h))} kWh")






     

    