import streamlit as st 
import numpy as np
import datetime
import time
import streamlit.components.v1 as components
#import boto3
#from boto.s3.key import Key

def local_millInspect(file_name):
    st.markdown(
            f'<iframe src=' + file_name + ' height = "800" width = "100%"></iframe>',
            unsafe_allow_html=True,
    )


def upload_file_using_client(bytes_data, scanDate, uploadedBy):
    """
    Uploads file to S3 bucket using S3 client object
    :return: None
    """
    session = boto3.Session(aws_access_key_id="AKIARQN3SPXTJ4BN5PGX", aws_secret_access_key="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")
    bucket_name = "husab"
    #prefix = 'test'
    s3 = session.resource("s3", region_name="ap-east-1")
    bucket = s3.Bucket(bucket_name)
    #print(bucket)
    #objs = bucket.objects.filter(Prefix=prefix)

    Key = str(scanDate) + "_" + uploadedBy + ".zip"
    try:
        s3.meta.client.put_object(Body=bytes_data, Bucket=bucket_name, Key=Key)
    except:
        raise

def photo360HTML_GEN(scanDateSelect, assetTypeSelect, colorModeSelect):
    # in database
    # S3 prefix
    prefix = "https://kycg.s3.ap-east-1.amazonaws.com/husab/photo360/"

    # get parameters
    #name0 = 'SAG'
    if assetTypeSelect == 'Ball Mill':
        name0 = 'BALL'
    elif assetTypeSelect == 'Ball Mill 2':
        name0 = 'BALL2'
    elif assetTypeSelect == 'SAG Mill':
        name0 = 'SAG'
    
    # date
    day = scanDateSelect.split("-")[0]
    month = scanDateSelect.split("-")[1]
    year = scanDateSelect.split("-")[2]
    name1 = day + month + year[2:4]
        
    # color
    name2 = 'RGB'
    if colorModeSelect == 'Monochrome':
        name2 = 'GRAY'

    fname = name0+'-'+name1+'-'+name2+'.jpg'
    fnamePV = name0+'-'+name1+'-'+name2+'-PV.jpg'

    with open('photo360.html', 'r') as f:
        lines = f.readlines()
    f.close()
    lines[18] = '    "panorama": ' + '"'+ prefix + fname + '"' + ',\n'
    lines[19] = '    "preview": ' + '"'+ prefix + fnamePV + '"' + ',\n'
    
    with open('photo360.html', 'w') as f:
        f.writelines(lines)
    f.close()

    return

def GET_SCAN_DATES(assetName):
    SAG = ['30-JAN-2023', '12-DEC-2022', '10-OCT-2022', '15-SEP-2022', '22-AUG-2022', '25-JUL-2022', '21-MAY-2022']
    #SAG2 = ['30-JUN-2022', '23-MAY-2022']
    BALL = ['25-Jul-2022']
    #BALL2 = ['09-JUL-2022']

    if assetName == 'SAG Mill':
        datesList = SAG
    elif assetName == 'Ball Mill':
        datesList = BALL
    #elif assetName == 'Ball Mill 1':
    #    datesList = BALL1
    #elif assetName == 'Ball Mill 2':
    #    datesList = BALL2

    return datesList



def app():
    # add sidebar elements
    st.sidebar.markdown("---")
    st.sidebar.title("Upload New Scan")
    millType = st.sidebar.radio(
            "Please select Grinding Lines",
            ('SAG Mill','Ball Mill'))
    uploadedBy = st.sidebar.text_input('Uploaded By Whom:', ' ')
    scanDate = st.sidebar.date_input(
            "Please Select Scan Date",
            datetime.date(2020, 5, 20))
    st.sidebar.text_input('Total Processed Tons - kton', '200')
    uploaded_file = st.sidebar.file_uploader("Choose a file")
    uploadClicked = st.sidebar.button("Upload and Save")
    if uploaded_file is not None and uploadClicked:
        bytes_data = uploaded_file.getvalue()
        upload_file_using_client(bytes_data, scanDate, uploadedBy)
        st.sidebar.success("Scan file uploaded to server.")
    
    
    st.title("Mill Scan Inspection 360")
    st.markdown("---------------")
    optionContainer = st.container()
    with optionContainer:
        ccolmn1, ccolmn2, ccolmn3 = st.columns(3)
        with ccolmn1:
            assetTypeSelect = st.radio(
                    "1. Please select the asset",
                    ('SAG Mill','Ball Mill'))
            st.markdown("###")
            if assetTypeSelect == 'Ball Mill':
                st.warning("Ball mill scans are not currently available, please select SAG mill!")

        with ccolmn2:
            # select the dates
            scanDatesForAssets = GET_SCAN_DATES(assetTypeSelect)
            scanDateSelect = st.selectbox(
                "2. Please select inspection date",
                (scanDatesForAssets)
            )
            
        with ccolmn3:
            colorModeSelect = st.radio(
                    "3. Please select image mode",
                    ('Monochrome', 'Full RGB Color'))
    
    st.markdown("###")
    loadScanClicked = st.button("4. Load Scan")


    st.markdown("---")
    
    with st.spinner('Loading mill assembly model...'):
        time.sleep(1)
        #local_millInspect(iframeLINK)
        photo360HTML_GEN(scanDateSelect, assetTypeSelect, colorModeSelect)
        if loadScanClicked:
            HtmlFile_tSS = open("photo360.html", 'r', encoding='utf-8').read()
            components.html(HtmlFile_tSS, height=800)
        else:
            st.info("Please select scan date, asset type and press Load Scan")


    st.markdown("_______________________________________________________")
    st.title("Inspection Notes")
    st.markdown("""
        🎏 Please review the 360 photo for each asset.
        """
    )

    st.markdown("_______________________________________________________")
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