import pandas as pd
from PIL import Image 
from PIL import Image
import streamlit as st

from labs.lab1 import lab1_code
from labs.lab2 import lab2_code



st.set_page_config(
    page_title="Finance", layout="wide", page_icon="./images/flask.png"
)


# Image HEC
image_hec = Image.open('images/hec.png')

# Image Hi Paris
image_hiparis = Image.open('images/hi-paris.png')




##################################################################################
############################# DASHBOARD PART #####################################
##################################################################################



st.sidebar.header("**Dashboard**") # .sidebar => add widget to sidebar
st.sidebar.markdown("  ")


############# SELECT TEACHER  ###############
select_teacher = "Daniel Schmidt"


############# SELECT SECTION CODE ###############
list_section_code = ["2", "5", "11", "13"]
select_code = st.sidebar.selectbox('Select your section code ➡️', list_section_code)


############# SELECT STUDENT IDS OF GROUP ###############
student_ids = st.sidebar.text_input("Write each members' student id ➡️", "(Example: 76307 82090 76322)")


############# SELECT A LAB/EXERCICE NUMBER ###############

lab_numbers = st.sidebar.selectbox('Select the exercise ➡️', [
'01 - One risky and one risk-free asset',
'02 - Two risky assets'
])




# ########### TITLE #############


st.image(image_hec, width=300)
st.title("HEC Paris - Finance Labs")
st.subheader("Portfolio theory 📈")
st.markdown("##### **Course provided by Daniel Schmidt**")


url = "https://www.hi-paris.fr/"
st.markdown("Made with the help of the **[Hi! PARIS Engineering Team](%s)**" % url)
st.image(image_hiparis, width=150)

st.markdown("  ")
st.markdown("---")




if lab_numbers == "01 - One risky and one risk-free asset": # premiere page
    lab1_code(select_teacher, select_code, student_ids)
    
else:
    lab2_code(select_teacher, select_code, student_ids)
    