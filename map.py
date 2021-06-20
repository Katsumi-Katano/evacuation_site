import json
import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import requests

@st.cache(allow_output_mutation=True)
def get_eva(url):
    df = pd.read_csv(url, encoding='utf-8')
    return df
url ='https://www.opendata.metro.tokyo.lg.jp/soumu/130001_evacuation_center.csv'
df_eva = get_eva(url)

"""
# "東京都避難場所'
## 東京都の災害時緊急避難場所
"""

st.title('東京都災害時避難場所一覧')
st.write(df_eva)

from streamlit_folium import folium_static
import folium
from folium.plugins import MarkerCluster
import pandas as pd


def visualize_locations(df, zoom=5):
     """日本を拡大した地図に、pandasデータフレームのlatitudeおよびlongitudeカラムをプロットする。
     """
    #図の大きさを指定する。
     f = folium.Figure(width=1000, height=500)

    #初期表示の中心の座標を指定して地図を作成する。
     center_lat=35.41222
     center_lon=139.41300
     m = folium.Map(location=[center_lat, center_lon], zoom_start=zoom).add_to(f)

    #縮尺によって、マーカーがまとめられるように設定する。
     marker_cluster = MarkerCluster().add_to(m)

    #データフレームの全ての行のマーカーを作成する。
     for i in range(0, len(df)):
        folium.Marker(location=[df["緯度"][i], df["経度"][i]]).add_to(marker_cluster)

     return m


st.subheader("避難施設マップ")     
g = visualize_locations(df_eva)
folium_static(g)



WARD_COLORS = {
'千代田区': [255,0,0],
'中央区' : [139,0,0],
'港区' : [255,20,147],
'新宿区' : [219,112,147],
'文京区' : [255,69,0],
'台東区' : [255,215,0],
'墨田区' : [127,255,212],
'江東区' : [0,0,255],
'品川区' : [255,255,0],
'目黒区' : [255,250,205],
'大田区' : [255,218,185],
'世田谷区': [221,160,221],
'渋谷区' : [186,85,211],
'中野区' : [139,0,139],
'杉並区' : [128,0,128],
'豊島区' : [72,61,139],
'北区' : [173,255,47],
'荒川区' : [128,128,0],
'板橋区' : [224,255,255],
'練馬区' : [255,248,220],
'足立区' : [244,164,96],
'葛飾区' : [210,105,30],
'江戸川区' : [165,42,42],
'八王子市' : [255, 32, 32, 160],
'立川市' : [255, 32, 32, 160],
'武蔵野市' : [255, 32, 32, 160],
'三鷹市' : [255, 32, 32, 160],
'青梅市' : [255, 32, 32, 160],
'府中市' : [255, 32, 32, 160],
'昭島市' : [255, 32, 32, 160],
'調布市' : [255, 32, 32, 160],
'町田市' : [255, 32, 32, 160],
'小金井市' : [255, 32, 32, 160],
'小平市' : [255, 32, 32, 160],
'日野市' : [255, 32, 32, 160],
'東村山市' : [255, 32, 32, 160],
'国分寺市' : [255, 32, 32, 160],
'国立市' : [255, 32, 32, 160],
'福生市' : [255, 32, 32, 160],
'狛江市' : [255, 32, 32, 160],
'東大和市' : [255, 32, 32, 160],
'清瀬市' : [255, 32, 32, 160],
'東久留米市' : [255, 32, 32, 160],
'武蔵村山市' : [255, 32, 32, 160],
'多摩市' : [255, 32, 32, 160],
'稲城市' : [255, 32, 32, 160],
'羽村市' : [255, 32, 32, 160],
'あきる野市' : [255, 32, 32, 160],
'西東京市' : [255, 32, 32, 160],
'瑞穂町' : [255, 32, 32, 160],
'日の出町' : [255, 32, 32, 160],
'檜原村' : [255, 32, 32, 160],
'奥多摩町' : [255, 32, 32, 160],
'大島町' : [255, 32, 32, 160],
'利島村' : [255, 32, 32, 160],
'新島村' : [255, 32, 32, 160],
'神津島村' : [255, 32, 32, 160],
'三宅村' : [255, 32, 32, 160],
'御蔵島村' : [255, 32, 32, 160],
'八丈町' : [255, 32, 32, 160],
'青ヶ島村' : [255, 32, 32, 160],
'小笠原村' : [255, 32, 32, 160],
}
df_eva["ward_color"] = df_eva["指定区市町村名"].apply(lambda x: WARD_COLORS[x])


st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/streets-v11',
    initial_view_state=pdk.ViewState(
        latitude=35.41222,
        longitude=139.41300,
        zoom=10.5,
        pitch=50,
    ),
    layers=[
        pdk.Layer(
            'ScatterplotLayer',
            data=df_eva,
            get_position='[経度, 緯度]',
            get_fill_color="ward_color",
            get_radius=50,
        ),
    ],
))

