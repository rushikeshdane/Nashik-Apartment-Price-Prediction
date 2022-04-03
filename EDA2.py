import streamlit as st

import plotly.express as px

import folium
from folium.plugins import HeatMap
from folium.plugins import FastMarkerCluster

from warnings import filterwarnings
import  get_data

filterwarnings('ignore')
def app():
    try:
        st.sidebar.markdown('(note : hover your mouse on the map '
                        'to get extra detail about particular house)')
        st.subheader('How our dataset looks on nashik map 🗺️ ?')
        df = get_data.get_data(path='feature_enginerring/data_after_removing_null')

        fig = px.scatter_mapbox(df,
                                lat=df.latitude,
                                lon=df.longitude, hover_name='address'  # ,color ='housetype'
                                , color_discrete_sequence=['grey'],
                                # size = 'house_condition',
                                hover_data=['owners', 'house_condition', 'BHK', 'price', 'per_month_emi', 'total_sqft'],
                                zoom=10, height=450, width=1000)
        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        st.plotly_chart(fig, use_container_width=True)


        def generateBaseMap(default_location=[19.9975, 73.7898], default_zoom_start=12):
            base_map = folium.Map(location=default_location, zoom_start=default_zoom_start)
            return base_map


        basemap = generateBaseMap()
        FastMarkerCluster(data=df[['latitude', 'longitude']].values.tolist()).add_to(basemap)
        HeatMap(df[['latitude', 'longitude']], zoom=18, radius=15).add_to(basemap)
        # with st.echo():

        from streamlit_folium import folium_static

        folium_static(basemap)

        with st.expander('see observation'):
            st.text('''
             1) if you look  heatmap  nashik city can be divided into  4-5 measure cluster
             no.1 is central nashik area around dwarka ,with measure markets in nashik located in this area ,
             with maximum number of educational facility and corparate offices ,where lot's of construction is
             going on towords south of this cluster
             no.2 is nashik road area it is very developed area with nashik railway station 
             no.3 is gangapur road or college road it is also developed area with well established educational facilty 
             no.4 is ambad area ,it is nashik's industrial area 
             no.5 is panchavati area ,with measure markets this cluster has some most important religious places
        
             2) Their is no houses near gandhinagar airport region because this is area is surrounded by 
             military ,you can see many empty spaces right next to really dense clusters because most of them are
             either corparate area or goverment's land
        
             3) you can divide nashik city into two equal part's if you follow godavari river as boundary
            ''')

        st.subheader('Where are the new and old houses situated ?')
        with st.expander('see plot'):
            fig = px.scatter_mapbox(df,
                                    lat=df.latitude,
                                    lon=df.longitude, hover_name='address', color='house_condition'
                                    , color_discrete_sequence=['indigo', 'green'],
                                    # size = 'price',
                                    hover_data=['owners', 'house_condition', 'BHK', 'price', 'per_month_emi', 'total_sqft'],
                                    zoom=10, height=350, width=1000)
            fig.update_layout(mapbox_style="open-street-map")
            fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

            st.plotly_chart(fig, use_container_width=True)

        st.subheader('Where are the Apartments and independent houses  ?')
        with st.expander('see plot'):
            fig = px.scatter_mapbox(df,
                                    lat=df.latitude,
                                    lon=df.longitude, hover_name='address', color='housetype'
                                    , color_discrete_sequence=['brown', 'yellow'],
                                    # size = 'price',
                                    hover_data=['owners', 'house_condition', 'BHK', 'price', 'per_month_emi', 'total_sqft'],
                                    zoom=10, height=350, width=1000)
            fig.update_layout(mapbox_style="open-street-map")
            fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
            st.plotly_chart(fig, use_container_width=True)

        st.subheader('Where are the expensive properties in nashik ?')
        with st.expander('see plot'):
            expensive = df[df['price'] > 50.00]
            basemap1 = generateBaseMap()
            FastMarkerCluster(data=expensive[['latitude', 'longitude']].values.tolist()).add_to(basemap1)
            HeatMap(expensive[['latitude', 'longitude']], zoom=18, radius=15).add_to(basemap1)
            folium_static(basemap1)

            fig = px.scatter_mapbox(expensive,
                                    lat=expensive.latitude,
                                    lon=expensive.longitude, hover_name='address'
                                    , color_discrete_sequence=['red'],
                                    # size = 'price',
                                    hover_data=['owners', 'house_condition', 'BHK', 'price', 'per_month_emi', 'total_sqft'],
                                    zoom=9, height=350, width=1000)
            fig.update_layout(mapbox_style="open-street-map")
            fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
            fig.update_geos(center_lat=20.00745)
            fig.update_geos(center_lon=73.80875)
            st.plotly_chart(fig, use_container_width=True)

        st.subheader('Where are the cheapest properties in nashik ?')
        with st.expander('see plot'):
            cheapest = df[df['price'] < 15.00]
            basemap1 = generateBaseMap()
            FastMarkerCluster(data=cheapest[['latitude', 'longitude']].values.tolist()).add_to(basemap1)
            HeatMap(cheapest[['latitude', 'longitude']], zoom=20, radius=15).add_to(basemap1)
            folium_static(basemap1)

            fig = px.scatter_mapbox(cheapest,
                                    lat=cheapest.latitude,
                                    lon=cheapest.longitude, hover_name='address'
                                    , color_discrete_sequence=['green'],
                                    # size = 'price',
                                    hover_data=['owners', 'house_condition', 'BHK', 'price', 'per_month_emi', 'total_sqft'],
                                    zoom=10, height=350, width=1000)
            fig.update_layout(mapbox_style="open-street-map")
            fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
            st.plotly_chart(fig, use_container_width=True)

    except  Exception as e:
        st.write(e)
        pass