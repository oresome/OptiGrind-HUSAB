import streamlit as st 
import numpy as np 
import datetime



def app():
    st.title("""
            Mill Simulation Studies
            """)

    st.markdown("---------------------")

    st.subheader("Effect of Feed Chute Designs on Mill Trajectories")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("Old Chute @ 9.0 RPM")
        video_file1 = open('millSimulation/old9rpm.mp4', 'rb')
        video_bytes1 = video_file1.read()
        st.video(video_bytes1)
    with col2:
        st.markdown("Current Chute @ 9.0 RPM")
        video_file2 = open('millSimulation/new9rpm.mp4', 'rb')
        video_bytes2 = video_file2.read()
        st.video(video_bytes2)



    st.markdown("-------------------------------------------")
    with st.container():
        st.markdown("Visit us @ <https://bradken.com>")
        st.markdown("""
                All company names, logos, product names, and identifying marks used throughout this website are the property of their respective trademark owners. They are used for descriptive purposes only and are protected by the relevant laws of the countries in which the trademarks are registered.
        """
        )
        st.markdown("©️ 2022 Copyright Bradken")


    hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True) 