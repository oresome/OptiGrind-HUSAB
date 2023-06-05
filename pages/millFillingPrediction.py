import streamlit as st 
import numpy as np 
import mrlcpower
import plotly.graph_objects as go

def pieChart(labels, values):
    # Add histogram data
    fig = go.Figure()
    #config = {'displayModeBar': False}
    fig.add_trace(go.Pie(labels=labels, values=values))

    fig.update_layout(
        autosize=False,
        margin=dict(l=1, r=1, t=1, b=1)
    )

    fig.update_layout(
        showlegend=True,
        font=dict(
            family="Ubuntu, regular",
            size=12,
            color="Black"
        )
    )

    fig.update_layout(legend=dict(
    yanchor="top",
    y=0.97,
    xanchor="left",
    x=0.03
    ))

    return fig


def checkinput(millIntDia, plateWear, bellyLen, trinionDia, coneLen, oreSG, totalFill, speed):
    if millIntDia and plateWear and bellyLen and trinionDia and coneLen and oreSG and totalFill and speed:
        return True
    else:
        return False

def app():
    st.title("""
            Mill Power Draw Prediction and Mill Filling Estimation
            """)

    st.markdown("---------------------")

    # section 1: 
    st.subheader("Mill Power Draw Prediction")
    pdContainer = st.container()
    with pdContainer:
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            millType = st.selectbox(
            'Please Select Mill Type',
            ('SAG', 'AG', 'Ball'))
            millSize = st.selectbox(
            'Please Select Mill Size',
            ('36FT', '24FT', '26FT', '28FT', '30FT', '32FT', '34FT', '38FT', '40FT'))
            millSizeNum = millSize[0:2]
            millIntDia = st.text_input('Mill Internal Diameter - m', '10.764', help="The radius should calculate from the mill centre to the top of the shell plate!")
            plateWear = st.text_input('Shell Plate Wear - mm', '0', help="The wear should be calculated compared with the new liner conditions!")
            bellyLen = st.text_input('Cylindrical Section Length - m', '5.054', help="This is the cylindrical section length inside liners!")
            centreLen = st.text_input('Mill Centre Line Length - m', '8.032', help="This is centre line length inside liners within the mill!")
            trinionDia = st.text_input('Mill Trunnion Diameter - m', '2.3', help="This is discharge trunion diameter of the mill!")
            coneLen = st.text_input('Conical Section Length - m', '0.999', help="This is estimated conical section length!")

        with col2:
            # get all flags
            ballSGDisable = False
            ballFillDisable = False
            if millType == 'AG':
                ballSGDisable = True
                ballFillDisable = True
            # inputs
            oreSG = st.text_input('Ore Density - t/m³', '2.7')
            ballSG = st.text_input('Ball Density - t/m³', '7.85', disabled = ballSGDisable)
            totalFill = st.text_input('Total Filling - %', '', help="Ball filling is Total Filling for Ball Mill Power Draw Prediction")
            ballFill = st.text_input('Ball Filling - %', '', help="Ball filling is Total Filling for Ball Mill Power Draw Prediction", disabled = ballFillDisable)
            if ballFillDisable and ballSGDisable:
                ballFill = 0
                ballSG = 0
            speed = st.text_input('Mill Speed - RPM', '')
            dischargeType = st.radio(
                "Please Select Discharge Type",
                ('Overflow', 'Grate')) 
            if dischargeType == 'Overflow':
                overflowFlag = True
            else:
                overflowFlag = False
                
            millDrive = st.radio(
                "Please Select Mill Drive Type",
                ('Gear and Pinion', 'Gearless')) 
            if millDrive == 'Gear and Pinion':
                gearedFlag = True
            else:
                gearedFlag = False
            #st.markdown("###")
            st.markdown("###")
            calcPressed = st.button("Calculate Power")
        
        with col3:
            drivePower = 0
            conicalPower = 0
            shellPower = 0
            totalPower = 0
            if calcPressed:
                calcFlag = checkinput(millIntDia, plateWear, bellyLen, trinionDia, coneLen, oreSG, totalFill, speed)
                if calcFlag:
                    actualDia = float(millIntDia)+float(plateWear)/500
                    #print(actualDia)
                    noLoadP, shellPower, conicalPower, totalPowerkW = mrlcpower.millPower(actualDia, float(bellyLen), float(centreLen), float(trinionDia), float(coneLen), float(speed), float(millSizeNum), float(oreSG), float(ballSG), float(totalFill)/100, float(ballFill)/100, overflowFlag, gearedFlag)
                    drivePower = noLoadP
                    conicalPower = conicalPower
                    shellPower = shellPower
                    totalPower = totalPowerkW
                else:
                    st.error("Input paramters are either not complete or wrong, please check again!!!")
            st.metric(label="Predicted no-load Draw - [kW]", value=round(drivePower, 1))
            st.metric(label="Predicted Power from Shell - [kW]", value=round(conicalPower, 1))
            st.metric(label="Predicted Power from Conical Section - [kW]", value=round(shellPower, 1))
            st.metric(label="Predicted Total Power Draw - [kW]", value=round(totalPower, 1))
            fig = pieChart(['No-load Power', 'Cylindrical Section Power', 'Conical Section Power'], [drivePower, shellPower, conicalPower])
            st.plotly_chart(fig, use_container_width=True)


    # section 2: 
    st.markdown("---------------------")
    st.subheader("Mill Filling Estimation")
    chargeLevels = [7.56, 
                    8.44, 
                    9.25, 
                    10.05, 
                    10.85, 
                    11.74, 
                    12.64, 
                    13.58, 
                    14.59, 
                    15.51, 
                    16.43, 
                    17.40, 
                    18.41, 
                    19.43, 
                    20.56, 
                    21.59, 
                    22.61, 
                    23.63, 
                    24.68, 
                    25.78, 
                    26.87, 
                    28.08, 
                    29.20, 
                    30.30, 
                    31.39, 
                    32.55, 
                    33.69, 
                    34.95, 
                    36.10, 
                    37.27]

    millCharge = st.container()
    with millCharge:
        col1, col2 = st.columns([1, 2])
        with col1:
            st.info("🚩  Shell liner profile has been updated with the latest profile from scan.")
            st.markdown("###")
            st.info("🚩  The total charge level is estimated based on the shell cross-sectional area.")
            st.markdown("###")
            st.info("🚩  The total charge level is superimposed to the discharge end liners.")
            st.markdown("###")
            chargeLvOpt = st.select_slider('Please Select Total Charge Level - %', 
                                        options=chargeLevels, value=chargeLevels[int(len(chargeLevels)/2-1)])
            st.markdown("###")
            st.markdown("Coming soon: Power Draw as an indicator for Mill Filling")



        with col2:
            st.session_state.chargeid = chargeLevels.index(chargeLvOpt)
            imgName = "Charge/charge_" + str(st.session_state.chargeid) + ".png"
            captionName = "Estimated charge level is:" + str(chargeLvOpt) + "%"
            st.image(imgName, caption='Shell Trajectory', use_column_width=True)


    hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True) 