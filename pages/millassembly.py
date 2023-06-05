'''
Description: 
Author: lunyang
Github: 
Date: 2022-02-02 15:03:13
LastEditors: lunyang
LastEditTime: 2022-02-02 17:22:06
'''
import streamlit as st
import requests
from streamlit_lottie import st_lottie
import plotly.graph_objects as go
from PIL import Image
import time


def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


# Use local CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Use local CSS


#@st.cache
def local_pvModel(file_name):
    st.markdown(
            f'<iframe src=' + file_name + ' height = "600" width = "100%"></iframe>',
            unsafe_allow_html=True,
    )

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def millLocationMap():
    fig = go.Figure(go.Scattermapbox(
    fill = "toself",
    lon = [15.0172], lat = [-22.5888],
    marker = { 'size': 20, 'color': "orange" }))

    fig.update_layout(
        mapbox = {
            'style': "stamen-terrain",
            'center': {'lon': 20, 'lat': -20 },
            'zoom': 4},
        showlegend = False)
    fig.update_layout(
        autosize=False,
        width=600,
        height=600,
        margin=dict(l=10, r=3, t=3, b=3)
    )        
    return fig

def app():
    #local_css("style/style.css")
    # ---- LOAD ASSETS ----
    #st.image("bradken.png")
    st.title("Current Mill Assembly")
    #st.markdown("<br>", unsafe_allow_html=True)
    #"""
    # [![Buy me a coffee](https://img.shields.io/badge/Buy%20me%20a%20coffee--yellow.svg?logo=buy-me-a-coffee&logoColor=orange&style=social)](https://www.buymeacoffee.com/wchennewy)
    #"""
    #st.markdown("_______________________________________________________")

    colm1 = st.columns(3)
    with colm1[0]:
        opsDetails = '<p style="color:Black; font-size: 16px; font-weight: regular;">🏗️  BK58691_r1</p>'
        st.markdown(opsDetails,unsafe_allow_html=True)
        #st.header("🏗️ Current Mill Assembly - BK58691_r1")
    with colm1[1]:
        downloadGA_clicked = st.button("Download GA")
    with colm1[2]:
        downloadBoM_clicked = st.button("Download BoM")


    #my_bar.progress(percent_complete + 1)
    #lottie_spin= load_lottieurl("https://assets8.lottiefiles.com/packages/lf20_9asbexx5.json")
    pvLINK = "https://kycg.s3.ap-east-1.amazonaws.com/BK56981_r3.html"
    with st.spinner('Loading mill assembly model...'):
        time.sleep(1)
        local_pvModel(pvLINK)
    
    st.markdown("_______________________________________________________________________")
    st.title("Current Mill Datasheet")
    with st.container():
        r1col1, r1col2, r1col3 = st.columns(3)
        r1col1.text_input("Name of Mill", "MIL230")
        r1col1.text_input("Manufacturer", "NCP")
        r1col1.text_input("Mill Diameter - m/ft", "10.97/36")
        r1col1.text_input("Length of Shell - m/ft", "5.94/19.5")
        r1col1.text_input("F.E Trunnion - m/ft", "2.698/8.85")        
        r1col1.text_input("D.E Trunnion - m/ft", "2.398/7.86")#

        r1col2.text_input("Grate Discharge - Y/N", "Y")
        r1col2.text_input("Cone Angle - deg", 15)
        r1col2.text_input("No. of Rows Drilled: Shell", 60)        
        r1col2.text_input("No. of Rows Drilled: FE & DE Heads", 32)
        r1col2.text_input("Mill Speed Range - RPM", "0-10.01")
        r1col2.text_input("Typical RPM", 9.72)

        r1col3.text_input("Variable/Fixed Speed", "Variable")
        r1col3.text_input("Uni/Bi-directional", "Uni")
        r1col3.text_input("Direction of Rotation:-FE to DE", "CCW")
        r1col3.text_input("Total Mill Volume - %", "24-30")
        r1col3.text_input("Steel Ball Load - %", "12-15")
        r1col3.text_input("Top Size Steel Ball - mm", 125)
        #r1col2.text_input("Placeholder", "Placeholder")

    st.markdown("_______________________________________________________________________")
    #st.title("Current Mill Datasheet")
    with st.container():
        fig=millLocationMap()
        st.plotly_chart(fig, use_container_width=True)
    
    with st.container():
        st.markdown("Visit us @ <https://bradken.com>")
        st.markdown("""
                All company names, logos, product names, and identifying marks used throughout this website are the property of their respective trademark owners. They are used for descriptive purposes only and are protected by the relevant laws of the countries in which the trademarks are registered.
        """
        )
        st.markdown("© 2022 Copyright Bradken")

    hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True) 