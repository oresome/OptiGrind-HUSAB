'''
Description: 
Author: lunyang
Github: 
Date: 2022-02-02 16:00:26
LastEditors: lunyang
LastEditTime: 2022-02-02 17:34:55
'''
import streamlit as st 
import numpy as np 
import datetime



def app():
    st.title("""
            Vibration Sensor Dashboard
            """)

    st.markdown("---------------------")


    d = st.sidebar.date_input(
        "Please Select Operating Date",
        datetime.date(2022, 4, 22))

    freq = st.sidebar.slider('Please Select Data Smoothing Levels?', 0, 99, 7)

    st.markdown("Coming soon!")




    hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True) 