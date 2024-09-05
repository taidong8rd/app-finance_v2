import streamlit as st
import pandas as pd
from io import BytesIO

import gspread
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession

@st.cache_data()
def load_csv(path):
    df = pd.read_csv(path, sep=",", decimal=".")
    return df


@st.cache_data()
def create_excel_file(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    
    output.seek(0)  
    return output.read()

@st.cache_data()
def connection_gsheet(sheet):
    scope = [
        #'https://spreadsheets.google.com/feeds',
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    credentials = service_account.Credentials.from_service_account_info(
            st.secrets["gcp_service_account"],
            scopes=scope,
        )
    
    # json_file = r".streamlit/app-finance-hec-v2-87b9e52036ee.json"
    # credentials = ServiceAccountCredentials.from_json_keyfile_name(json_file, scope)

    gc = gspread.authorize(credentials)    
    sh = gc.open('App-finance-HEC-students-results')
    
    if sheet == "lab1":
        return sh.sheet1
    
    else:
        return sh.get_worksheet(1)
    
    
    
    # Function to submit answers for Page 1
def submit_answers_page1(list_answers_):
    
    scope = [
        #'https://spreadsheets.google.com/feeds',
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=scope,
    )

    # Authorize with gspread
    gc = gspread.authorize(credentials)
    sh = gc.open('App-finance-HEC-students-results')
    
    # Access the first worksheet (lab1)
    lab1_sheet = sh.get_worksheet(0)
    dashboard_sheet = sh.get_worksheet(2)
    
    # Append the row to the worksheet
    lab1_sheet.append_row(list_answers_)
    dashboard_sheet.append_row(list_answers_[:8])
    
    # Mark submission as complete in session state
    st.session_state['submitted_page1'] = True


# Function to submit answers for Page 2
def submit_answers_page2(list_answers_):
    
    scope = [
        #'https://spreadsheets.google.com/feeds',
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"],
        scopes=scope,
    )

    # Authorize with gspread
    gc = gspread.authorize(credentials)
    sh = gc.open('App-finance-HEC-students-results')
    
    # Access the second worksheet (lab2)
    lab2_sheet = sh.get_worksheet(1)
    dashboard_sheet = sh.get_worksheet(2)

    
    # Append the row to the worksheet
    lab2_sheet.append_row(list_answers_)
    dashboard_sheet.append_row(list_answers_[:8])
    
    # Mark submission as complete in session state
    st.session_state['submitted_page2'] = True