import streamlit as st
import streamlit.components.v1 as components
#import base64

# Use local CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def app():

    local_css("style/style.css")
    # ---- LOAD ASSETS ----
    #st.image("bradken.png")
    st.title("Bradken OptiGrind Cloud Application")
    with st.container():
        components.html(
            """
            <div class="flourish-embed flourish-cards" data-src="visualisation/10431727"><script src="https://public.flourish.studio/resources/embed.js"></script></div>
            """,
            height = 500,
            scrolling = True,
        )

    #st.markdown("<br>", unsafe_allow_html=True)
    #"""
    # [![Buy me a coffee](https://img.shields.io/badge/Buy%20me%20a%20coffee--yellow.svg?logo=buy-me-a-coffee&logoColor=orange&style=social)](https://www.buymeacoffee.com/wchennewy)
    #"""
    st.markdown("_______________________________________________________")
    components.html(
        """
            <head>
                <title> Blinking feature using JavaScript </title>
                <style>
                    #blink {
                        font-size: 20px;
                        font-weight: bold;
                        color: #c9510c;
                        transition: 0.05s;
                    }
                </style>
            </head>

            <body>
                <p id="blink"> 21-December-2022 App Updates </p>
                <script type="text/javascript">
                    var blink = document.getElementById('blink');
                    setInterval(function() {
                        blink.style.opacity = (blink.style.opacity == 0 ? 1 : 0);
                    }, 1000);
                </script>
            </body>
        """,
        height = 50
    )

    st.markdown("""
        1. Updated Inspection360 and Shell Grind Master with new scan
        """)

    st.markdown("_______________________________________________________")
    st.subheader("Development Roadmap")
    intro = '<p style="color:Black; font-size: 14px; font-weight: regular;">26-Apr-2022</p>'
    st.markdown(intro, unsafe_allow_html=True)
    st.markdown("""
        1. App in previous dev has been sub-divided into sub-modules for easier access.
        """)
    st.markdown("""
        2. Updated Mill Assembly to latest revisions
        """)
    st.markdown("""
        3. Updated Grind Master with latest Shell install.
        """)

    intro = '<p style="color:Black; font-size: 14px; font-weight: regular;">May-2022</p>'
    st.markdown(intro, unsafe_allow_html=True)
    st.markdown("""
        1. Include vibration sensor dashboard sample results
        """)
    st.markdown("""
        2. Including charge level estimation from mill power draw
        """)
    st.markdown("""
        3. Bug fixes and performance improvements
        """)
    st.markdown("_______________________________________________________")




    with st.container():
        st.markdown("Visit us @ <https://bradken.com>")
        st.markdown("""
                All company names, logos, product names, and identifying marks used throughout this website are the property of their respective trademark owners. They are used for descriptive purposes only and are protected by the relevant laws of the countries in which the trademarks are registered.
        """
        )
        st.markdown("© 2022 Copyright Bradken")