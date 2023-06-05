import streamlit as st 
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import os.path
from csv import writer

def calChargeOpt(wearValue, shellid, selectedCampaign, selectedScan):
    filenameDir = 'HUSAB/' + 'CAMPAIGN_' + selectedCampaign + '/SCAN-' + selectedScan.replace('-', '') + '/chargeOptions.csv'
    with open(filenameDir, 'r') as f:
        lines = f.readlines()
    chargeOptionList = []
    for line in lines:
        tmp = []
        for a in line.strip('\n').split(','):
            tmp.append(round(float(a), 1))
        chargeOptionList.append(tmp)
    f.close()
    #chargeOptDF = pd.read_csv(filenameDir)
    wearmatrix = chargeOptionList
    # add rowid as an input
    rowid=shellid
    chargeOpt = wearmatrix[rowid]
    return chargeOpt

def calTrajImageName(shellid, chargeLevid, speed, selectedCampaign, selectedScan):
    shellid=shellid+1
    #chargeLevid=0 #replace this when receive full images
    filenameDir = 'HUSAB/' + 'CAMPAIGN_' + selectedCampaign + '/SCAN-' + selectedScan.replace('-', '')
    massid = int(50*chargeLevid+300)
    rpmid = speed.replace(".", "p")
    wear_image_name = filenameDir +'/shell'+ str(shellid)+'_mass'+str(massid)+'_'+rpmid+'.png'
    return wear_image_name

def calMaxRMP(wearValue, chargeLevid, selectedCampaign, selectedScan):
    shellid=wearValue
    filenameDir = 'HUSAB/' + 'CAMPAIGN_' + selectedCampaign + '/SCAN-' + selectedScan.replace('-', '') + '/maxRPM.csv'
    with open(filenameDir, 'r') as f:
        lines = f.readlines()
    RPMmatrix = []
    for line in lines:
        tmp = []
        for a in line.strip('\n').split(','):
            tmp.append(float(a))
        RPMmatrix.append(tmp)
    f.close()
    #print(RPMmatrix)

    maxrpmVal=RPMmatrix[shellid][chargeLevid]
    imageName=calTrajImageName(wearValue, chargeLevid, str(maxrpmVal), selectedCampaign, selectedScan)

    return maxrpmVal, imageName

def calMinChargeLev(wearValue, speed, speedid, selectedCampaign, selectedScan):
    shellid=wearValue
    filenameDir = 'HUSAB/' + 'CAMPAIGN_' + selectedCampaign + '/SCAN-' + selectedScan.replace('-', '') + '/minCharge.csv'
    with open(filenameDir, 'r') as f:
        lines = f.readlines()
    Chargematrix = []
    for line in lines:
        tmp = []
        for a in line.strip('\n').split(','):
            tmp.append(int(a))
        Chargematrix.append(tmp)
    f.close()

    minChargeVal=Chargematrix[shellid][speedid]

    if minChargeVal == 0:
        for i in range(0,len(Chargematrix[0])):
            if Chargematrix[shellid][i] != 0:
                ChargeVal = Chargematrix[shellid][i]
                safeRPMid=i
                break
    elif minChargeVal == -1:
        for i in range(-1,-1*(len(Chargematrix[0])+1),-1):
            if Chargematrix[shellid][i] != -1:
                ChargeVal = Chargematrix[shellid][i]
                safeRPMid = i+len(Chargematrix[0])
                break
    else:
        ChargeVal = minChargeVal
        safeRPMid = speedid

    chargeLevid=int((ChargeVal-300)/50)
    ChargeOpt = calChargeOpt(wearValue, shellid, selectedCampaign, selectedScan)
    ChargeLev = ChargeOpt[chargeLevid]
    #print("image input=",wearValue, ChargeVal, chargeLevid, speed)
    chargeimageName=calTrajImageName(shellid, chargeLevid, str(speed), selectedCampaign, selectedScan)      

    return minChargeVal, ChargeLev, safeRPMid, chargeimageName


def local_pvModel(file_name):
    st.markdown(
            f'<iframe src=' + file_name + ' height = "500" width = "100%"></iframe>',
            unsafe_allow_html=True,
    )

def GET_SCAN_DATES(campaign):
    scanDatesFile = 'HUSAB/' + "CAMPAIGN_" + campaign + '/scanDates.csv'
    scanDatesDF = pd.read_csv(scanDatesFile)
    relineDate = scanDatesDF["SCAN_DATES"].iloc[-1]
    scanDates = scanDatesDF["SCAN_DATES"].values
    campaignDir = 'HUSAB/' + "CAMPAIGN_" + campaign
    return relineDate, scanDates, campaignDir

####################################### MAIN ################################
def app():
    # add sidebar elements
    st.sidebar.markdown("---")
    #st.sidebar.markdown("Please Select Shell Liner Campaign")
    st.session_state.selectCampaign = st.sidebar.radio(
        "Please Select Shell Liner Campaigns",
        ["OCT22-APR23", "APR22-OCT22"],
    )
    #st.session_state.selectCampaign
    st.header("Shell Wear Evolution")
    st.markdown("---")

    #wearEvo = '<p style="color:Black; font-size: 18px; font-weight: bold;">🎢 SHELL GEOMETRY EVOLUTION</p>'
    #st.markdown(wearEvo,unsafe_allow_html=True)
    shellEvlv = st.container()
    with shellEvlv:
        shellslider, shellprof = shellEvlv.columns([1,2])
        #st.session_state.wearInput=None
        #st.session_state.updateProfclicked =False
        #st.session_state.selectedWear = None
        relineDate, scanDates, campaignDir = GET_SCAN_DATES(st.session_state.selectCampaign)
        with shellslider:
            #st.markdown(relineDate)
            #st.markdown(scanDates)
            #st.markdown(scanDates[0])
            st.info("🚩  Shell liners from the current campaign was installed on " + relineDate)
            st.session_state.wearvalue=0
            st.markdown("###")
            st.session_state.modeSelect = st.radio(
                    "Please Select Shell Liner Profile:",
                    (scanDates))
            st.markdown("###")

            # 2D
            st.session_state.selectWear_clicked = st.button("🚀  Select This Profile")
            #try:
            if st.session_state.selectWear_clicked:                          
                st.session_state.selectedWear = st.session_state.wearvalue
                st.success(f'✅ ' + st.session_state.modeSelect + ' Shell profile is Sellected.')
            #except:
            #    if selectWear_clicked:
            #        st.session_state.selectWear_clicked=True
            #        st.session_state.selectedWear = st.session_state.wearvalue
            #        st.success(f'✅ Latest Shell profile is Sellected. Now you can move below for trajectory predictions.') 


        with shellprof:
            #st.plotly_chart(wearProfPlot, use_container_width=False)
            #st.bokeh_chart(p, use_container_width=True)
            imName = campaignDir + '/shell2d.jpg'
            ##wearfilename = 'shellProfile2D/' + imName
            image = Image.open(imName)
            st.image(image, caption='Selected Shell Liner Profile')
            #else:
            #    pvLINK = "https://kycg.s3.ap-east-1.amazonaws.com/husab/SHELL-10OCT22.html"
            #    with st.spinner('Loading 3D Worn Shell ...'):
            #        local_pvModel(pvLINK)

    #perfmPredic = '<p style="color:Black; font-size: 18px; font-weight: bold;">📈 SHELL PERFORMANCE PREDICTION</p>'
    #st.markdown(perfmPredic, unsafe_allow_html=True)
    st.header("Shell Trajectory Prediction")
    st.markdown("---")
    shellPerf = st.container()
    with shellPerf:
        shellOper, spacer, shellTraj = shellPerf.columns([2,1,2])
        with shellOper:
            direction = st.radio(
                        '1. Please Select Mill Rotational Direction?',
                        ('FE -> DE Counter-Clock-Wise', 
                        'FE -> DE Clock-Wise'))
            st.markdown("###")
            option = st.radio(
                        '2. Please Select Which Performance to Predict?',
                        ('Total Charge + Mill Speed -> Trajectory', 
                        'Total Charge -> Maximum Mill Speed', 
                        'Mill Speed -> Safe Total Charge level'))
            st.session_state.option = option
            st.session_state.direction = direction
            # define shell id
            if st.session_state.direction == 'FE -> DE Counter-Clock-Wise':
                st.session_state.shellid = 0  # worn as second row
                st.markdown("###")
                st.success("✅ The latest shell profile scanned on " + st.session_state.modeSelect + " was utilised, please confirm the mill rotational direction!")
                direction1 = Image.open("millDirection/FEDE_LH.png")
                st.image(direction1)
            elif st.session_state.direction == 'FE -> DE Clock-Wise':
                st.session_state.shellid = 1  # new as first row
                st.markdown("###")
                st.success("✅ The latest shell profile scanned on " + st.session_state.modeSelect + " was utilised, please confirm the mill rotational direction!")
                direction2 = Image.open("millDirection/FEDE_RH.png")
                st.image(direction2)
            st.markdown("###")
            st.success('✅ You have selected: ' + direction + ' ' + option)
            st.markdown("-------------------------------------------")
            #st.write(' ')
            
            if option == 'Total Charge + Mill Speed -> Trajectory':
                st.session_state.computeTraj_clicked= False
                st.session_state.trajImageName = None  
                #st.markdown(st.session_state.selectedWear)             
                try:
                    if st.session_state.selectedWear is not None:
                        # Total Charge Level input
                        chargeOpt=calChargeOpt(st.session_state.selectedWear, st.session_state.shellid, st.session_state.selectCampaign, st.session_state.modeSelect)  # add a row ID input
                        #st.dataframe(chargeOpt)
                        chargelevel = st.select_slider('Please Select Total Charge Level - %', 
                                        options=chargeOpt, value=chargeOpt[int(len(chargeOpt)/2-1)])
                        st.session_state.chargelevel = chargelevel
                        st.session_state.chargeid = chargeOpt.index(chargelevel)
                        # define ball charge level
                        #ballOpt=np.around(np.linspace(start = 12.0, stop = 16.0, num = 5, endpoint = True), decimals=1)
                        #balllevel = st.select_slider('Please Select Ball Charge Level - %', options=ballOpt, value=14.0)
                        #st.session_state.balllevel = balllevel

                        # Speed input
                        speedOpt=np.around(np.linspace(start = 8.4, stop = 10.2, num = 19, endpoint = True), decimals=1)
                        millSpeed = st.select_slider('Please Select Mill Speed - RPM', options=speedOpt, value=9.4)
                        st.session_state.millSpeed = millSpeed
                        # call associated results image
                        trajImageName=calTrajImageName(st.session_state.shellid, st.session_state.chargeid, str(st.session_state.millSpeed), st.session_state.selectCampaign, st.session_state.modeSelect)
                        #st.markdown(trajImageName)
                        st.session_state.trajImageName=trajImageName


                        st.markdown("-------------------------------------------")
                        computeTraj_clicked = st.button("🚀  Compute Trajectory")
                        if computeTraj_clicked:
                            st.session_state.computeTraj_clicked= True               
                except:
                    #if st.session_state.computeTraj_clicked:
                    #    st.warning('Wear profile hasn\'t selected!')
                    pass

            elif option == 'Total Charge -> Maximum Mill Speed':   
                st.session_state.computeMaxRPM_clicked = False
                st.session_state.rpmimagename = " " 
                try:
                    if st.session_state.selectedWear is not None:            
                        chargeOpt1=calChargeOpt(st.session_state.selectedWear, st.session_state.shellid, st.session_state.selectCampaign, st.session_state.modeSelect)  # add a row ID input
                        chargelevel1 = st.select_slider('Please Select Total Charge Level - %', options=chargeOpt1, value=chargeOpt1[int(len(chargeOpt1)/2-1)])
                        st.session_state.chargelevel1 = chargelevel1
                        st.session_state.chargeid1 = chargeOpt1.index(chargelevel1)
                        # define ball charge level
                        #ballOpt1=np.around(np.linspace(start = 12.0, stop = 16.0, num = 5, endpoint = True), decimals=1)
                        #balllevel1 = st.select_slider('Please Select Ball Charge Level - %', options=ballOpt1, value=14.0)
                        #st.session_state.balllevel1 = balllevel1

                        # Speed input
                        computeMaxRPM_clicked = st.button("🚀 Compute Maximum RPM")
                        if computeMaxRPM_clicked:
                            st.session_state.computeMaxRPM_clicked = True
                            #st.markdown("Reached 0")
                            maxRPM, rpmimagename = calMaxRMP(st.session_state.shellid, st.session_state.chargeid1, st.session_state.selectCampaign, st.session_state.modeSelect)
                            #st.markdown(maxRPM)
                            #st.markdown(rpmimagename)
                            
                            st.session_state.maxRPM=maxRPM
                            st.session_state.rpmimagename = rpmimagename
                            st.metric("Maximum RPM = ", value= maxRPM)                            
                except:
                    pass
                
            elif option == 'Mill Speed -> Safe Total Charge level': 
                st.session_state.computeMinCharge_clicked = False
                st.session_state.chargeimageName = " " 
                try:
                    if st.session_state.selectedWear is not None:
                        speedOpt1=np.around(np.linspace(start = 8.4, stop = 10.2, num = 19, endpoint = True), decimals=1)
                        millSpeed1 = st.select_slider('Please Select Mill Speed - RPM', options=speedOpt1, value=9.4)
                        #st.metric('millSpeed1', millSpeed1)
                        st.session_state.millSpeed1 = millSpeed1
                        st.session_state.millSpeedid1 = speedOpt1.tolist().index(millSpeed1)

                        computeMinCharge_clicked = st.button("🚀 Compute Min Charge Level")
                        if computeMinCharge_clicked:
                            st.session_state.computeMinCharge_clicked = True
                            #st.metric('reached here', 100)
                            minChargeVal, ChargeLev, safeRPMid, chargeimageName =calMinChargeLev(st.session_state.shellid, st.session_state.millSpeed1, st.session_state.millSpeedid1, st.session_state.selectCampaign, st.session_state.modeSelect)
                            st.session_state.minChargeVal = minChargeVal
                            st.session_state.ChargeLev = ChargeLev
                            st.session_state.chargeimageName = chargeimageName
                            safeRPM = speedOpt1[safeRPMid]
                            
                            st.session_state.safeRPM = safeRPM 
                            if st.session_state.minChargeVal == 0:
                                st.warning(f'Warning: At current shell profile, mill speed cannot be below {st.session_state.safeRPM :.2f} RPM, and the min charge level is {st.session_state.ChargeLev :.2f} %.')
                            elif st.session_state.minChargeVal == -1:
                                st.warning(f'Warning: At current shell profile, mill speed cannot be above {st.session_state.safeRPM :.2f} RPM, and the min charge level is {st.session_state.ChargeLev :.2f} %.')
                            else:
                                st.metric("Minimum Charge Level (%) = ", value= st.session_state.ChargeLev) 
                except:
                    pass
        with shellTraj:
            if st.session_state.option == 'Total Charge + Mill Speed -> Trajectory': 
                if st.session_state.computeTraj_clicked:        
                    #print("show trajectory image",st.session_state.trajImageName)                              
                    if os.path.exists(st.session_state.trajImageName):
                        trajImage = Image.open(st.session_state.trajImageName)
                        st.image(trajImage, caption='Shell Trajectory', use_column_width=True)
                    #else:
                    #    st.image("HUSAB/blank.png", caption='Shell trajectory image doesn\'t exist', use_column_width=True)

            elif st.session_state.option == 'Total Charge -> Maximum Mill Speed':
                if st.session_state.computeMaxRPM_clicked:                       
                    if os.path.exists(st.session_state.rpmimagename):
                            trajImage = Image.open(st.session_state.rpmimagename)
                            st.image(trajImage, caption=f'Shell Trajectory at Maximum RPM = {st.session_state.maxRPM :.2f}', use_column_width=True)
                    #else:
                    #        st.image("HUSAB/blank.png", caption='Shell trajectory image at Maximum RPM doesn\'t exist', use_column_width=True)
            elif st.session_state.option == 'Mill Speed -> Safe Total Charge level':
                if st.session_state.computeMinCharge_clicked:   
                    if os.path.exists(st.session_state.chargeimageName):
                        trajImage = Image.open(st.session_state.chargeimageName)
                        st.image(trajImage, caption=f'Shell Trajectory at Mininum Charge Level = {st.session_state.ChargeLev :.2f}', use_column_width=True)
                    else:
                        st.image("HUSAB/blank.png", caption='Shell trajectory image at Mininum Charge Level doesn\'t exist', use_column_width=True)
    
    
    st.markdown("-------------------------------------------")
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