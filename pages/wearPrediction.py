import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import datetime

from streamlit_lottie import st_lottie
import requests

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


COMMENT_TEMPLATE_MD = """{} - {}
> {}"""



#@st.cache
def try_read_df(f):
    try:
        return pd.read_csv(f, sep=',')
    except:
        return pd.read_csv(f)

def calcKeyMetrics(df, dFrom, dTo):
    #dfParse = dateutil.parser.parse(df['TIME'])
    dFrom = datetime.datetime.strptime(dFrom, '%Y-%m-%d')
    dTo = datetime.datetime.strptime(dTo, '%Y-%m-%d')
    df['TIME'] =  pd.to_datetime(df['TIME'])
    df=df.replace(to_replace="Null",value=0)
    mask = df['FEED_TPH'] > 100
    filterDF = df.loc[mask]
    reliability = filterDF.shape[0]/df.shape[0]
    meanFeed = np.mean(filterDF['FEED_TPH'])
    total_tons = sum(filterDF['FEED_TPH'])
    total_E = sum(filterDF['POWER_KW'])
    SE = total_E/total_tons
    totalBallAddition = sum(filterDF['BALL_ADDITION_KG'])
    additionRate = totalBallAddition/total_tons
    meanSpd = np.mean(abs(filterDF['SPEED']))
    #cW = np.mean(filterDF['FEED_TPH'])/(np.mean(filterDF['FEED_TPH'])+np.mean(filterDF['WATER_M3PH']))

    return reliability, meanFeed, SE, additionRate, meanSpd, total_tons


def HISTORICAL_DATA_PLOT(X, Y1, Y2, XX, YY1, YY2):
    # Add histogram data
    #config = {'displayModeBar': False}
    #                    mode='lines',
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=X, y=Y1,
                    mode='markers',
                    name='Scan Results Lifter')
                    )

    fig.add_trace(go.Scatter(x=X, y=Y2,
                    mode='markers',
                    name='Scan Results Plate',
                    yaxis="y2")
                    )

    fig.add_trace(go.Scatter(x=XX, y=YY1,
                    mode='markers',
                    name='Fit Results Lifter')
                    )

    fig.add_trace(go.Scatter(x=XX, y=YY2,
                    mode='markers',
                    name='Fit Results Plate',
                    yaxis="y2")
                    )

    fig.update_layout(
        autosize=True,
        width=800,
        height=360,
        margin=dict(l=1, r=1, t=1, b=1)
    )

    fig.update_layout(
        xaxis_title="Process Tons - MT",
        yaxis=dict(
            title="<b>Lifter Height - mm</b>",
            titlefont=dict(
                color="#1f77b4"
            ),
            tickfont=dict(
                color="#1f77b4"
            ),
            range=[100,400]
        ),
        yaxis2=dict(
            title="<b>Plate Thickness - mm</b>",
            titlefont=dict(
                color="#ff7f0e"
            ),
            tickfont=dict(
                color="#ff7f0e"
            ),
            range=[20,100],
            anchor="x",
            overlaying="y",
            side="right"
            #position=0.15
        ),
        showlegend=True,
        font=dict(
            family="Ubuntu, regular",
            size=12,
            color="Black"
        )
        #plot_bgcolor='rgb(255,255,255)'
    )


    fig.update_layout(legend=dict(
    yanchor="top",
    y=0.4,
    xanchor="left",
    x=0.03
    ))

    return fig


def app():
    titleContainer = st.container()
    with titleContainer:
        titleColmns1, titleColmns2, titleColmns3 = st.columns(3)
        with titleColmns1:
            st.title("Shell Liner Wear Prediction")
            st.markdown("Plant Operating Metrics and Wear Predictions")
        with titleColmns2:
            lottie_coding = load_lottieurl("https://assets7.lottiefiles.com/packages/lf20_9ti102vm.json")
            st_lottie(lottie_coding, height=150, key="hello")

    st.markdown("-------------------")

    opsDetails = '<p style="color:Black; font-size: 16px; font-weight: regular;">🏭 PLANT DATA SUMMARY [Dated 24-Aug-2022]</p>'
    st.markdown(opsDetails,unsafe_allow_html=True)

    pdContainer = st.container()
    with pdContainer:
        col1, col2 = st.columns([1,2])
        with col2:
            df = try_read_df('wearPrediction/runData.csv')
            #df = replaceTIMESTAMPE(df)
            #st.table(df)
            st.markdown("Operating Data")
            #st.table(df)
            st.dataframe(df, 5000, 400)
            #dfTable=plotDF(df)
            #st.plotly_chart(df, use_container_width=True)
        with col1:
            # add a function to calc key metrics
            dFrom = "2022-04-20"
            dTo = "2022-09-19"
            reliability, meanFeed, SE, additionRate, meanSpd, total_tons = calcKeyMetrics(df, dFrom, dTo)
            st.metric(label="Mill Reliability", value=round(reliability, 2), delta=np.round(reliability-0.92, 2))
            st.metric(label="Mean Fresh Feed - TPH", value=round(meanFeed, 1), delta=np.round(meanFeed-1500, 1))
            st.metric(label="Mill Specific Energy - kWh/t", value=round(SE, 1), delta=np.round(SE-10.0, 1))
            st.metric(label="Mean Ball Addition Rate - kg/ton", value=round(additionRate, 2), delta=np.round(additionRate-0.75, 2))
            st.metric(label="Mean Mill Speed - RPM", value=round(meanSpd, 2), delta=np.round(meanSpd-9.5, 2))
            #print(total_tons)
            
    
    st.markdown("-------------------")
    wearp = '<p style="color:Black; font-size: 16px; font-weight: regular;">🏭 WEAR PREDICTION</p>'
    st.markdown(wearp,unsafe_allow_html=True)
    st.markdown("###")
    wPContainer = st.container()
    with wPContainer:
        col1, col2 = st.columns([1,2])
        with col1:
            st.markdown("Historical wear trend is shown on the right graph!")
            st.info("🚩 Please input additional processed tons to predict the wear rate!")
            #tonsOpt1=np.around(np.linspace(start = 0, stop = total_tons/1000, num = 125, endpoint = True), decimals=1)
            #millTons1 = st.select_slider('Please Select Historical Culumative Processed Tons - kTons', options=tonsOpt1, value=100)
            # additional tons
            st.markdown("###")
            tonsOpt2=st.text_input('Additional Tons - kTons', '0')
            st.warning("🚩 Please double check the input tonnage unit!")
            calcPressed = st.button("Predict Wear")
            #millTons2 = st.select_slider('Please Select Additional Culumative Processed Tons - kT', options=tonsOpt1, value=100)

        with col2:
            st.markdown("###")
            X = np.array([0, 0.798812, 3.098864, 3.8506, 4.8465])
            Y1 = np.array([394, 369.48, 288.93, 238, 178])
            Y2 = np.array([94, 89, 73.98, 66.73, 54.9])

            lifter_coeff = np.polyfit(X, Y1, 2)
            plate_coeff = np.polyfit(X, Y2, 2)

            # prediction wear
            if calcPressed:
                if float(tonsOpt2):
                    tons = float(tonsOpt2)/1000 + X[-1]
                    #lifter_prediction = reg_lifter.predict(np.array([tons]).reshape((-1, 1)))
                    #plate_prediction = reg_plate.predict(np.array([tons]).reshape((-1, 1)))
                    xFitLine = np.linspace(0,tons,100)
                    yFitLineLifter = np.poly1d(lifter_coeff)
                    yFitLinePlate = np.poly1d(plate_coeff)
                    prediction_lifter = yFitLineLifter(xFitLine)
                    prediction_plate = yFitLinePlate(xFitLine)
                    fig2 = HISTORICAL_DATA_PLOT(X, Y1, Y2, xFitLine, prediction_lifter, prediction_plate)
                    st.plotly_chart(fig2, use_container_width=True)


                    additionalDays = float(tonsOpt2)*1000/meanFeed/24/reliability

                    st.info("🚩 Predicted lifter height is: " + str(np.round(prediction_lifter[-1], 1)) + ' mm')
                    st.info("🚩 Predicted plate thickness is: " + str(np.round(prediction_plate[-1], 1))+ ' mm')
                    st.info("🚩 Estimated service life to process the inputted additional ores is " + str(np.round(additionalDays, 1)) + ' Days')

            else:
                # construct fitting line
                xFitLine = np.linspace(0, 4.8465,100)
                yFitLineLifter = np.poly1d(lifter_coeff)
                yFitLinePlate = np.poly1d(plate_coeff)
                fig1 = HISTORICAL_DATA_PLOT(X, Y1, Y2, xFitLine, yFitLineLifter(xFitLine), yFitLinePlate(xFitLine))

                st.plotly_chart(fig1, use_container_width=True)





    st.markdown("###")
    st.markdown("###")
    st.markdown("###")
    st.markdown("-------------------")
    with st.container():
        st.subheader("Warranties and Liability")
        st.warning("""
            1. Bradken makes no other warranties of any kind in connection with Grindmaster, whether express or implied, and specifically disclaims any and all implied warranties for suitability, completeness, accuracy, or fitness for any particular purpose, to the maximum extent permitted by law. \n
            2. Bradken shall in no event be liable for any loss or liability incurred by User arising in connection with the use of Grindmaster.
            3. Bradken shall in no event be liable to User for any Consequential Loss in connection with this Agreement.
            4. User warrants and represents that it shall its use of Grindmaster shall be for lawful purposes, and that Grindmaster shall not be used to support any business activity contrary to any applicable laws including but not limited to laws related to:
                (i)	    sanctions and export control,
                (ii)	bribery and corruption, and
                (iii)	anti-competitive behaviour.

            """
        )

    hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
