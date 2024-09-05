import pandas as pd
from pandas import to_datetime
from pandas.plotting import register_matplotlib_converters
import numpy as np
from pathlib import Path
import base64
import io
import os
from datetime import date, datetime
#import yfinance as yf
from PIL import Image # display an image
from io import StringIO # upload file
from google.oauth2 import service_account
import gspread


from utils import load_csv, create_excel_file
from io import BytesIO
import altair as alt
from PIL import Image
from vega_datasets import data
import pandas_datareader as pdr
import streamlit as st



from htbuilder import HtmlElement, div, hr, a, p, img, styles
from htbuilder.units import percent, px
import seaborn as sns
import matplotlib.pyplot as plt
import re
register_matplotlib_converters()

from labs.lab1 import Q1_compute_holdingperiod_returns




sns.set(style="whitegrid")
pd.set_option('display.max_rows', 15)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
st.set_option('deprecation.showPyplotGlobalUse', False)






# Configuration de l'app (html, java script like venv\)

# Deploy the app localy in terminal: streamlit run model.py

st.set_page_config(
    page_title="Finance", layout="wide", page_icon="./images/flask.png"
)



scope = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]




############################# LOAD STOCK DATA ####################################

# data = load_csv(r"data/CourseData_clean.csv")


# Image HEC
image_hec = Image.open('images/hec.png')

# Image Hi Paris
image_hiparis = Image.open('images/hi-paris.png')













##################################################################################
############################# DASHBOARD PART #####################################
##################################################################################

# st.sidebar.image(image_hiparis, width=200)
# url = "https://www.hi-paris.fr/"
# st.sidebar.markdown("Made in collaboration with the [Hi! PARIS Engineering Team](%s)" % url)

#st.sidebar.markdown("  ")



st.sidebar.header("**Dashboard**") # .sidebar => add widget to sidebar
st.sidebar.markdown("  ")


############# SELECT TEACHER  ###############
list_teachers = ["François Derien","Irina Zviadadze","Mian Liu","Teodor Duevski","Quirin Fleckenstein"]
select_teacher = st.sidebar.selectbox('Select your teacher ➡️', list_teachers)


############# SELECT SECTION CODE ###############
list_section_code = [f"B1-{i}" for i in range(1,15)] + ["B4-1", "B4-2"]
select_code = st.sidebar.selectbox('Select your section code ➡️', list_section_code)


############# SELECT STUDENT IDS OF GROUP ###############
student_ids = st.sidebar.text_input("Write each members' student id", "(Here is an example: 76307 82090 76322)")


############# SELECT A LAB/EXERCICE NUMBER ###############

lab_numbers = st.sidebar.selectbox('Select the exercise ➡️', [
'01 - One risky and one risk-free asset',
'02 - Two risky assets',
])




# ########### TITLE #############

st.image(image_hec, width=300)
st.title("HEC Paris - Finance Labs 🧪")
st.subheader("Portfolio theory 📈")
st.markdown("Course provided by: **François Derrien**, **Irina Zviadadze**, **Mian Liu**, **Teodor Duevski**, **Quirin Fleckenstein**")

st.markdown("  ")
st.markdown("---")

# default text for st.text_area()
default_text = ""

list_risky_assets = ["ACMTA", "ACU", "AIR", "ASA", "BKTI", "CECO", "PRG"]






#####################################################################################
#                   EXERCICE 1 - One risky asset, one risk-free asset
#####################################################################################


if lab_numbers == "01 - One risky and one risk-free asset": # premiere page
    
    startdate = datetime.now()


    #################################### SIDEBAR ##################################
    risky_asset = st.sidebar.selectbox("Select a risky asset ➡️", list_risky_assets, key="select_risky")
    


    ################################### DATAFRAMES ###############################

    # Risky asset dataframe (df_risky)
    # df_risky = data.loc[data["Stock"]==risky_asset]
    df_risky = load_csv(f"data/stocks/{risky_asset}.csv")


    @st.cache_data()
    def compute_riskfree(df_risky):
        returns = np.array([0.02 for i in range(df_risky.shape[0]-1)])
        exp_returns = np.mean(returns)
        std = np.std(returns, ddof=1)
        
        return returns, exp_returns, std
    
    riskfree_returns, riskfree_exp_returns, riskfree_std = compute_riskfree(df_risky)
    




    ##################################### TITLE ####################################
    st.markdown("## 01 - One risky and one risk-free asset")
    st.info(""" In this exercise, assume that you can invest in a risk-free asset (a T-bill) with an annual rate of return of 2%. 
            In addition, you have information on annual prices and dividends of individual risky stocks. Please choose one stock and compute its expected return and the standard deviation of its return. 
            Then, describe feasible portfolios that you can obtain by investing in the risk-free asset and chosen stock. 
            Please represent the set of feasible portfolios in a graph that has the standard deviation of the portfolio’s return on the x-axis and the expected return on the y-axis.
    """)
    st.markdown("    ")
    st.markdown("    ")





    #################################### QUESTION 1 ###################################

    st.subheader("Question 1 📝")

    #################### Part 1

    ## Title of PART 1
    st.markdown('''<p style="font-size: 22px;"> Please select one stock and <b>compute its realized (holding-period) returns.</b> 
                Assume that holding, is one year. <br> Next, please <b>compute the expected return</b> and <b>standard deviation</b> of the holding-period returns</b></p>''',
                unsafe_allow_html=True)

    st.markdown("   ")

    # ## View risky dataset
    st.markdown(f"**View the {risky_asset} data** with Date, Dividend and Price.")
    st.dataframe(df_risky.drop(columns=["Stock"]))


    ## Download dataset as xlsx

    # Set the headers to force the browser to download the file
    headers = {
                'Content-Disposition': 'attachment; filename=dataset.xlsx',
                'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            }

    # Create a Pandas Excel writer object
    excel_writer = pd.ExcelWriter(f"{risky_asset}.xlsx", engine='xlsxwriter')
    df_risky.drop(columns=["Stock"]).to_excel(excel_writer, index=False, sheet_name='Sheet1')
    excel_writer.close()

    # Download the file
    with open(f"{risky_asset}.xlsx", "rb") as f:
            st.download_button(
                    label=f"📥 **Download the {risky_asset} dataset**",
                    data=f,
                    file_name=f"{risky_asset}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )



    st.markdown("   ")
    st.markdown("   ")        
    
    
    ####### Holding-period returns
    st.write(f"**Compute the holding-period returns**")

    upload_expected_return = st.file_uploader("Drop your results in an excel file (.xlsx)", key="Q1", type=['xlsx'])
    answer_1_Q1_1 = ""

    if upload_expected_return is not None:
        answer_1_Q1_1 = "Received"
        returns_portfolios = pd.read_excel(upload_expected_return)

        
    st.markdown("  ")
    st.markdown("  ")


    
    ###### Expected returns
    st.write(f"**Compute the expected returns**")
    answer_1_Q1_2 = st.text_input("Enter your results","", key="AQ1.2a")

    # solution = st.checkbox('**Solution** ✅',key="SQ1.2a")
    # if solution:
    #     answer_text = f'The expected return of {risky_asset} is **{np.round(asset_expected_return,4)}**.'
    #     st.success(answer_text)

    st.markdown("  ")
    st.markdown("  ")


    # Standard deviation
    st.write(f"**Compute the standard deviation**")
    answer_1_Q1_3 = st.text_input("Enter your results ","", key="AUQ1.2b")

    # solution = st.checkbox('**Solution** ✅',key="SQ1.2b")

    # if solution:
    #     answer_text = f'The standard deviation of {risky_asset} is **{np.round(asset_std_dev,4)}**.'
    #     st.success(answer_text)
        
        
    st.markdown("   ")  
    
    
    # Compute holding-period returns, expected returns, std 
    @st.cache_data()
    def Q1_compute_holdingperiod_returns(df_risky):
        asset1_returns = (df_risky["Price"][1:].to_numpy() - df_risky["Price"][:-1].to_numpy() + df_risky["Dividends"].to_numpy()[1:])/df_risky["Price"][:-1].to_numpy()    
        return asset1_returns
    
    #asset1_returns = Q1_compute_holdingperiod_returns(df_risky)
    
    
    if st.checkbox('**Solutions - Question 1** ✅'):
        asset1_returns = Q1_compute_holdingperiod_returns(df_risky)
        returns_result = pd.DataFrame({"Year":df_risky["Year"].iloc[1:], 
                                       "Return":asset1_returns})
        st.markdown(f"""**Instruction**: Please select one stock and compute its realized (holding-period) returns. Assume that holding, is one year. <br>
                    """, unsafe_allow_html=True)
        st.dataframe(returns_result)
        
        st.markdown(" ")
        st.markdown(" ")
        
        asset_expected_return = np.round(np.mean(asset1_returns),4)
        asset_std_dev = np.round(np.std(asset1_returns, ddof=1), 4)
        
        st.markdown(f"""**Instruction**: Compute the expected return and standard deviation of the holding-period returns <br>
                    - <u>Expected return</u>: {asset_expected_return} <br>
                    - <u>Standard deviation</u>: {asset_std_dev}
                    """, unsafe_allow_html=True)



    st.markdown("   ")
    st.markdown("   ") 
    st.markdown("   ")     
    st.markdown("   ")





    ###################################### QUESTION 2 ##########################################
    

    st.subheader("Question 2 📝")
    
    ### Part 1
    st.markdown('''<p style="font-size: 22px;">Assume that you have a capital of 1000 EUR that you fully invest in a portfolio. <b>Combine two assets</b> (one risky and one risk-free asset) into a <b>portfolio</b>. Next, <b>compute the expected returns</b> and <b>standard deviation</b> of the portfolio.</p>''',
                unsafe_allow_html=True)
    
    st.info("In this question, assume that **short-sale constraints** are in place (that is, the weight of each asset in your portfolio must be between 0 and 1). ")


    st.markdown("   ")
    st.markdown("   ")

    
    # Create a portfolio by selecting amount (EUR) in risky asset
    st.write(f"**Select the amount you want to put in {risky_asset}**")

    risky_amount = st.slider(f"**Select the amount you want to put in {risky_asset}**", min_value=0, max_value=1000, step=50, value=500, label_visibility="collapsed")
    riskfree_amount = 1000 - risky_amount
    
    st.write(f"You've invested **{risky_amount}** EUR in {risky_asset} and **{riskfree_amount}** EUR in the risky-free asset.")

    st.markdown("  ")
    st.markdown("  ")



    # Weight of assets in the portfolio
    st.write("**Compute the weight of each asset in your portfolio**")

    risky_weight = risky_amount/1000
    riskfree_weight = riskfree_amount/1000

    answer_1_Q2_1 = st.text_input(f'Enter the weight of the {risky_asset} asset',"", key="AUQ2.1w1")

    # solution = st.checkbox('**Solution** ✅', key="SQ2.1w1")
    # if solution:
    #     answer_text1 = f'The weight of the {risky_asset} asset is **{np.round(risky_weight,2)}**.'
    #     st.success(answer_text1)


    st.markdown("  ")
    
    answer_1_Q2_2 = st.text_input(f'Enter the weight of the risk-free asset',"", key="AUQ2.1w2")
    st.markdown("   ")
    st.markdown("   ") 



    # Enter portfolio expected returns
    st.write("**Compute the expected return of the portfolio**")
    answer_1_Q2_3 = st.text_input("Enter your results","", key="AQ2.21")
    st.markdown("    ")
    st.markdown("    ")


    # Enter portfolio standard deviation
    st.write("**Compute the standard deviation of the portfolio**")
    answer_1_Q2_4 = st.text_input("Enter your results","", key="AQ2.22")    
    st.markdown("   ")

        

    if st.checkbox('**Solutions - Question 2** ✅'):
        asset1_returns = Q1_compute_holdingperiod_returns(df_risky)
        
        risky_weight = risky_amount/1000
        riskfree_weight = riskfree_amount/1000
        
        st.markdown(f"""**Instruction**: *Compute the weight of each asset in your portfolio* <br>
                    - <u>{risky_asset}</u>: {risky_weight} <br>
                    - <u>Risk-free asset</u>: {riskfree_weight}
                    """, unsafe_allow_html=True)
        
        # Compute portfolio returns, expected ret, std
        portfolio_returns = (risky_weight*asset1_returns) + (riskfree_weight*riskfree_returns)
        
        st.markdown(f"""**Instruction**: *Compute the expected return and standard deviation of the portfolio* <br>
                    - <u>Expected return</u>: {np.round(np.mean(portfolio_returns), 4)} <br>
                    - <u>Standard deviation</u>: {np.round(np.std(portfolio_returns, ddof=1), 4)}
                    """, unsafe_allow_html=True)
        
        
        
    st.markdown("   ")
    st.markdown("   ") 
    st.markdown("   ")     
    st.markdown("   ")


################## QUESTION 3

    st.subheader("Question 3 📝")
    
    #### PART 1
    st.markdown('''<p style="font-size: 22px;"> Using Excel, <b> construct portfolios </b> that contain x% of the risky asset and (1-x)% of the risk-free asset, with x varying between 0 and 100% with 1% increments.
                For each portfolio, calculate its <b>standard deviation</b> of return and its <b>expected return</b>. 
                Represent these combinations in a graph, that is <b>draw the set of feasible portfolios</b>.''',
                unsafe_allow_html=True)
    
            
    
    st.markdown("   ")
    st.write("**Compute the expected return and standard deviation for each portfolio**")


    upload_file = st.file_uploader("Drop your results in an excel file (.xlsx)", key="Q3.21",type=['xlsx'])
    answer_1_Q3_1 = ""

    if upload_file is not None:
        answer_1_Q3_1 = "Received"
        returns_portfolios = pd.read_excel(upload_file)
        

    st.markdown("   ")
    st.markdown("   ")

    
    
    st.write("**Draw the set of feasible portfolios**")

    upload_graph = st.file_uploader("Drop the graph as an image (jpg, jpeg, png)", key="Q3.23", type=['jpg','jpeg','png'])
    answer_1_Q3_2 = ""

    if upload_graph is not None:
        answer_1_Q3_2 = "Received"
        image = Image.open(upload_graph)

      
        
    @st.cache_data()
    def Q3_return_std_portfolios(asset1_returns, weight_risky_portfolios):
        # Expected returns/std of risky asset
        asset_expected_return = np.round(np.mean(asset1_returns),4)
        asset_std_dev = np.round(np.std(asset1_returns, ddof=1), 4)

        # Weights of risky/riskfree in portfolios 
        # weight_risky_portfolios = np.arange(0,1.01,0.01)
        weight_riskfree_portfolios = 1 - weight_risky_portfolios
        
        # Expected returns/std of portfolios
        expected_returns_portfolios = np.array([w*asset_expected_return + (1-w)*riskfree_exp_returns for w in weight_risky_portfolios])
        std_portfolios = np.array([(w*asset_std_dev)**2 + ((1-w)*riskfree_std)**2 for w in weight_risky_portfolios])
        std_portfolios = np.sqrt(std_portfolios)
        
         # Portfolio dataframe to plot
        df_portfolios = pd.DataFrame({f"{risky_asset}":np.round(weight_risky_portfolios,2),
                                    "Risk-free":np.round(weight_riskfree_portfolios,2),
                                    "Expected return":np.round(expected_returns_portfolios,4), 
                                    "Standard deviation":np.round(std_portfolios,4)})
        
        return df_portfolios     
        
    
    st.markdown("   ")

    if st.checkbox('**Solutions - Question 3** ✅'):
        asset1_returns = Q1_compute_holdingperiod_returns(df_risky)
        weight_risky_portfolios = np.arange(0,1.01,0.01)
        df_portfolios = Q3_return_std_portfolios(asset1_returns, weight_risky_portfolios)            
        
        st.markdown(f"""**Instruction**: *Compute the expected return and standard deviation for each portfolio* <br>
                    """, unsafe_allow_html=True)
        st.dataframe(df_portfolios)
        
        st.markdown(" ")
        st.markdown(" ")
        
        asset_expected_return = np.round(np.mean(asset1_returns),4)
        asset_std_dev = np.round(np.std(asset1_returns, ddof=1), 4)
        
        st.markdown(f"""**Instruction**: *Draw the set of feasible portfolios* <br>
                    """, unsafe_allow_html=True)
        chart_portfolios = alt.Chart(df_portfolios).mark_circle(size=40).encode(y="Expected return",x="Standard deviation")
        st.altair_chart(chart_portfolios.interactive(), use_container_width=True)
    


    st.markdown("   ")
    st.markdown("   ") 
    st.markdown("   ")     
    st.markdown("   ")
    st.markdown("   ") 




################## QUESTION 4

    st.subheader("Question 4 📝")

    st.markdown('''<p style="font-size: 22px;"> Consider the feasible portfolios from Question 3 and <b> answer the following questions. </b> </p>''',
                unsafe_allow_html=True)
    st.info("Provide specific answers, that is, **characterize the portfolios in terms of the weights on both assets**")
    st.markdown("   ")
    
    
    ###### MAX expected return   
    answer_1_Q4_1 = st.text_area("**Can you find which portfolio has the highest expected return ?**", default_text)
    st.markdown("   ")
    st.markdown("   ")


    ###### MIN expected return   
    answer_1_Q4_2 = st.text_area("**Can you find which portfolio has the lowest expected return ?**", default_text)
    st.markdown("   ")
    st.markdown("   ")



    ###### MAX standard deviation 
    answer_1_Q4_3 = st.text_area("**Can you find which portfolio has the highest standard deviation ?**", default_text)
    st.markdown("   ")
    st.markdown("   ")
    
    
    ###### MIN standard deviation   
    answer_1_Q4_4 = st.text_area("**Can you find which portfolio has the lowest standard deviation ?**", default_text)
    st.markdown(" ")
    
    
    @st.cache_data()
    def Q4_feasible_portfolios_exp(df_portfolios):
    
        # EXPECTED RETURN 
        max_exp_row = df_portfolios.iloc[df_portfolios["Expected return"].idxmax(),:]
        max_exp_risky = max_exp_row[f"{risky_asset}"]
        max_exp_riskfree = max_exp_row["Risk-free"]
        max_exp_value = max_exp_row["Expected return"]

        min_exp_row = df_portfolios.iloc[df_portfolios["Expected return"].idxmin(),:]
        min_exp_risky = min_exp_row[f"{risky_asset}"]
        min_exp_riskfree = min_exp_row["Risk-free"]
        min_exp_value = min_exp_row["Expected return"]
        
        return max_exp_risky, max_exp_riskfree, max_exp_value, min_exp_risky, min_exp_riskfree, min_exp_value
    
    
    @st.cache_data()
    def Q4_feasible_portfolios_std(df_portfolios):
        
        # STANDARD DEVIATION
        max_std_row = df_portfolios.iloc[df_portfolios["Standard deviation"].idxmax(),:]
        max_std_risky = max_std_row[f"{risky_asset}"]
        max_std_riskfree = max_std_row["Risk-free"]
        max_std_value = max_std_row["Standard deviation"]

        min_std_row = df_portfolios.iloc[df_portfolios["Standard deviation"].idxmin(),:]
        min_std_risky = min_std_row[f"{risky_asset}"]
        min_std_riskfree = min_std_row["Risk-free"]
        min_std_value = min_std_row["Standard deviation"]
        
        return max_std_risky, max_std_riskfree, max_std_value, min_std_risky, min_std_riskfree, min_std_value 
    
    
    
    if st.checkbox('**Solutions - Question 4** ✅'):
        asset1_returns = Q1_compute_holdingperiod_returns(df_risky)
        weight_risky_portfolios = np.arange(0,1.01,0.01)
        df_portfolios = Q3_return_std_portfolios(asset1_returns, weight_risky_portfolios)
        
        max_exp_risky, max_exp_riskfree, max_exp_value, min_exp_risky, min_exp_riskfree, min_exp_value = Q4_feasible_portfolios_exp(df_portfolios)
        max_std_risky, max_std_riskfree, max_std_value, min_std_risky, min_std_riskfree, min_std_value = Q4_feasible_portfolios_std(df_portfolios)        
        
        st.markdown(f"""**Instruction**: *Can you find which portfolio has the highest expected return ?* <br>
                    - The portfolio with **{max_exp_risky}** in the risky asset ({risky_asset}) and **{max_exp_riskfree}** in the risk free asset. <br>
                    - The portfolio's expected return is **{np.round(max_exp_value,4)}**
                    """, unsafe_allow_html=True)
        
        st.markdown(" ")
        
        st.markdown(f"""**Instruction**: *Can you find which portfolio has the lowest expected return ?* <br>
                    - The portfolio with **{min_exp_risky}** in the risky asset ({risky_asset}) and **{min_exp_riskfree}** in the risk free asset. <br>
                    - The portfolio's expected return is **{np.round(min_exp_value,4)}**
                    """, unsafe_allow_html=True)
        
        st.markdown(" ")
        
        st.markdown(f"""**Instruction**: *Can you find which portfolio has the highest standard deviation ?* <br>
                    - The portfolio with **{max_std_risky}** in the risky asset ({risky_asset}) and **{max_std_riskfree}** in the risk free asset. <br>
                    - The portfolio's standard deviation is **{np.round(max_std_value,4)}**

                    """, unsafe_allow_html=True)
        
        st.markdown(" ")
        
        st.markdown(f"""**Instruction**: *Can you find which portfolio has the lowest standard deviation ?* <br>
                    - The portfolio with **{min_std_risky}** in the risky asset ({risky_asset}) and **{min_std_riskfree}** in the risk free asset. <br>
                    - The portfolio's standard deviation is **{np.round(min_std_value,4)}**
                    """, unsafe_allow_html=True)
        
        st.markdown(" ")



    st.markdown("   ")
    st.markdown("   ") 
    st.markdown("   ")     
    st.markdown("   ")
    st.markdown("   ")





    ######################################################################################
    ##################################### QUESTION 5 #####################################
    ######################################################################################


    st.subheader("Question 5 📝")
    
    st.markdown('''<p style="font-size: 22px;"> <b>Repeat the exercise of Question 3</b>, but with the possibility of selling short one of the two assets. That is, vary x, for example, from -100% to 100%.''',
                unsafe_allow_html=True)
   
    
    st.markdown("   ")

    st.write("**Compute the expected return and standard deviation for each portfolio**")
    upload_expected_return = st.file_uploader("Drop results in an excel file (.xlsx)", key="UQ5.1", type=['xlsx'])
    answer_1_Q5_1 = ""
    
    if upload_expected_return is not None:
        answer_1_Q5_1 = "Received"
        expected_return_portfolios = pd.read_excel(upload_expected_return)

    
    st.markdown("   ")
    st.markdown("  ")


    st.write("**Draw the set of feasible portfolios**")

    upload_graph = st.file_uploader("Drop graph as an image (jpg, jpeg, png)", key="UQ5.2", type=['jpg','jpeg','png'])
    answer_1_Q5_2 = ""

    if upload_graph is not None:
        answer_1_Q5_2 = "Received"
        image = Image.open(upload_graph)
        
    
    st.markdown(" ")

    if st.checkbox('**Solutions - Question 5** ✅'):
        asset1_returns = Q1_compute_holdingperiod_returns(df_risky)
        
        weight_risky_portfolios = np.arange(-1,2.01,0.01)
        df_portfolios = Q3_return_std_portfolios(asset1_returns, weight_risky_portfolios)             
        
        st.markdown(f"""**Instruction**: *Compute the expected return and standard deviation for each portfolio.* <br>
                    """, unsafe_allow_html=True)
        st.dataframe(df_portfolios)
        
        st.markdown(" ")
        st.markdown(" ")
        
        asset_expected_return = np.round(np.mean(asset1_returns),4)
        asset_std_dev = np.round(np.std(asset1_returns, ddof=1), 4)
        
        st.markdown(f"""**Instruction**: *Draw the set of feasible portfolios* <br>
                    """, unsafe_allow_html=True)
        chart_portfolios = alt.Chart(df_portfolios).mark_circle(size=20).encode(y="Expected return",x="Standard deviation")
        st.altair_chart(chart_portfolios.interactive(), use_container_width=True)



    st.markdown("   ")
    st.markdown("   ") 
    st.markdown("   ")     
    st.markdown("   ")
    st.markdown("   ")
    



################## QUESTION 6

    st.subheader("Question 6 📝")
    
    st.markdown('''<p style="font-size: 22px;"> <b>Repeat the exercise of Question 4</b>, but with the possibility of <b>selling short</b> one of the two assets. That is, analyze feasible portfolios from Question 5.''',
                unsafe_allow_html=True)
    
    st.markdown("  ")
    
   
    


    ###### PART 1 
    #answer_1_Q4_2 = user_input_2
    answer_1_Q6_1 = st.text_area("**Can you find which portfolio has the highest expected return?**", default_text, key="Q6.1")
    st.markdown("   ")


    ###### PART 2
    answer_1_Q6_2 = st.text_area("**Can you find which portfolio has the lowest expected return?**", default_text, key="Q6.2")
    st.markdown("   ")


    ###### PART 3
    answer_1_Q6_3 = st.text_area("**Can you find which portfolio has the highest standard deviation?**", default_text, key="Q6.3")
    st.markdown("   ")
    
    
    ###### PART 4
    answer_1_Q6_4 = st.text_area("**Can you find which portfolio has the lowest standard deviation?**", default_text, key="Q6.4")
    st.markdown(" ")

    
    if st.checkbox('**Solutions - Question 6** ✅'):
        asset1_returns = Q1_compute_holdingperiod_returns(df_risky)
        weight_risky_portfolios = np.arange(-1,2.01,0.01)
        df_portfolios = Q3_return_std_portfolios(asset1_returns, weight_risky_portfolios)
        
        max_exp_risky, max_exp_riskfree, max_exp_value, min_exp_risky, min_exp_riskfree, min_exp_value = Q4_feasible_portfolios_exp(df_portfolios)
        max_std_risky, max_std_riskfree, max_std_value, min_std_risky, min_std_riskfree, min_std_value = Q4_feasible_portfolios_std(df_portfolios)        
        
        st.markdown(f"""**Instruction**: *Can you find which portfolio has the highest expected return ?* <br>
                    - The portfolio with **{max_exp_risky}** in the risky asset ({risky_asset}) and **{max_exp_riskfree}** in the risk free asset. <br>
                    - The portfolio's expected return is **{np.round(max_exp_value,4)}**
                    """, unsafe_allow_html=True)
        
        st.markdown(" ")
        
        st.markdown(f"""**Instruction**: *Can you find which portfolio has the lowest expected return ?* <br>
                    - The portfolio with **{min_exp_risky}** in the risky asset ({risky_asset}) and **{min_exp_riskfree}** in the risk free asset. <br>
                    - The portfolio's expected return is **{np.round(min_exp_value,4)}**
                    """, unsafe_allow_html=True)
        
        st.markdown(" ")
        
        st.markdown(f"""**Instruction**: *Can you find which portfolio has the highest standard deviation ?* <br>
                    - The portfolio with **{max_std_risky}** in the risky asset ({risky_asset}) and **{max_std_riskfree}** in the risk free asset. <br>
                    - The portfolio's standard deviation is **{np.round(max_std_value,4)}**

                    """, unsafe_allow_html=True)
        
        st.markdown(" ")
        
        st.markdown(f"""**Instruction**: *Can you find which portfolio has the lowest standard deviation ?* <br>
                    - The portfolio with **{min_std_risky}** in the risky asset ({risky_asset}) and **{min_std_riskfree}** in the risk free asset. <br>
                    - The portfolio's standard deviation is **{np.round(min_std_value,4)}**
                    """, unsafe_allow_html=True)
        
        st.markdown(" ")
        
    st.markdown(" ")
    st.markdown("#### Congratulations you finished Exercise 1 🎉")



    list_answer = [answer_1_Q1_1,
answer_1_Q1_2,
answer_1_Q1_3,
answer_1_Q2_1,
answer_1_Q2_2,
answer_1_Q2_3,
answer_1_Q2_4,
answer_1_Q3_1,
answer_1_Q3_2,
answer_1_Q4_1,
answer_1_Q4_2,
answer_1_Q4_3,
answer_1_Q4_4,
answer_1_Q5_1,
answer_1_Q5_2,
answer_1_Q6_1,
answer_1_Q6_2,
answer_1_Q6_3,
answer_1_Q6_4,]


    ## SUBMISSION EXERCICE 1
    if st.sidebar.button('**Submit answers Ex1**'):
        ######### CONNEXION WITH GOOGLE SHEET API ##########

        scope = [
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive"
            ]

        ## Connect to google sheet
        credentials = service_account.Credentials.from_service_account_info(
            st.secrets["gcp_service_account"],
            scopes=scope,
        )

        gc = gspread.authorize(credentials)
        answers = [x for x in list_answer if x not in [np.nan,"", None]]
        count = len(answers)

        # List with answers 
        list_answers_ = [select_teacher,
        select_code,
        student_ids,
        1,
        risky_asset,
        str(startdate),
        str(datetime.now()),
        count,
        f"{round((count/len(list_answer))*100,1)}%",
        answer_1_Q1_1,
        answer_1_Q1_2,
        answer_1_Q1_3,
        answer_1_Q2_1,
        answer_1_Q2_2,
        answer_1_Q2_3,
        answer_1_Q2_4,
        answer_1_Q3_1,
        answer_1_Q3_2,
        answer_1_Q4_1,
        answer_1_Q4_2,
        answer_1_Q4_3,
        answer_1_Q4_4,
        answer_1_Q5_1,
        answer_1_Q5_2,
        answer_1_Q6_1,
        answer_1_Q6_2,
        answer_1_Q6_3,
        answer_1_Q6_4,
        ]
        

        ## Append new row to the google sheet
        sh = gc.open('App-finance-HEC-students-results').sheet1
        insertRow = list_answers_
        sh.append_row(insertRow)

        sh_looker = gc.open('App-finance-HEC-students-results').get_worksheet(2)
        insertRow2 = list_answers_[:9]
        sh_looker.append_row(insertRow2)

        st.sidebar.info('**Your answers have been submitted !**')
 


    ## Hi! PARIS logo
    st.sidebar.divider()
    st.sidebar.image(image_hiparis, width=150)
    url = "https://www.hi-paris.fr/"
    st.sidebar.markdown("**Made in collaboration with: [Hi! PARIS Engineering Team](%s)**" % url)
    
    










#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


@st.cache_data()
def two_stocks_charts(df_asset_ex2_merge, risky_asset1_ex2, risky_asset2_ex2):
    df_asset_ex2_graph1 = df_asset_ex2_merge.drop(columns=[f"Dividends ({risky_asset1_ex2})",
                                                            f"Dividends ({risky_asset2_ex2})"]).melt(id_vars=["Year"])
    
    chart1 = alt.Chart(df_asset_ex2_graph1).mark_line(point=True).encode(
        x=alt.X('Year:O'), 
        y="value", 
        color="variable"
        ).properties(title=f'View the stock price evolution of {risky_asset1_ex2} and {risky_asset2_ex2}')

    return chart1 


    
@st.cache_data()
def Q2_return_std_portfolios_risky(asset1_returns, asset2_returns, weight_portfolios):
    # returns_portfolios = np.array([w*asset1_returns + (1-w)*asset2_returns for w in weight_portfolios])
    
    asset1_expected_return = np.mean(asset1_returns)
    asset1_std_dev = np.std(asset1_returns, ddof=1)
    asset2_expected_return = np.mean(asset2_returns)
    asset2_std_dev = np.std(asset2_returns, ddof=1)
    
    asset12_corr = np.corrcoef(asset1_returns, asset2_returns)[0,1]
    
    # Compute expected return and std of each portfolio 
    expected_returns_portfolios = np.array([w*asset1_expected_return + (1-w)*asset2_expected_return for w in weight_portfolios])
    std_portfolios = np.array([(w*asset1_std_dev)**2 + ((1-w)*asset2_std_dev)**2 + 2*w*(1-w)*asset12_corr*asset1_std_dev*asset2_std_dev for w in weight_portfolios])
    std_portfolios = np.sqrt(std_portfolios)

    df_exp_std_return_portfolios = pd.DataFrame({risky_asset1_ex2:np.round(weight_portfolios,2),
                                                risky_asset2_ex2:np.round(1-weight_portfolios,2),
                                                "Expected return":np.round(expected_returns_portfolios,4), 
                                                "Standard deviation":np.round(std_portfolios,4)})
    
    return df_exp_std_return_portfolios


@st.cache_data()
def Q3_efficient_portfolios(df):
    df_ex2_q3_efficient = df.sort_values(by=["Expected return"]).reset_index(drop=True)
    min_std_q3 = df_ex2_q3_efficient["Standard deviation"].min()
    min_std_q3_exp = df_ex2_q3_efficient.loc[df_ex2_q3_efficient["Standard deviation"] == min_std_q3,"Expected return"].idxmax()
    efficient_portfolio = df_ex2_q3_efficient.iloc[min_std_q3_exp:].reset_index(drop=True)
    
    return efficient_portfolio


@st.cache_data()
def Q5_tangency_portfolio(df):
    riskfree_rate = 0.02
    df["Sharpe Ratio"] = np.round(((df["Expected return"] - riskfree_rate)/df["Standard deviation"]),4)
    
    max_sharpe_ratio = df_exp_std_return_portfolios["Sharpe Ratio"].idxmax()
    max_sharpe_ratio_row = df_exp_std_return_portfolios.iloc[max_sharpe_ratio,:]
    
    # Portfolio with max sharpe ratio
    max_sharpe_weight1, max_sharpe_weight2 = max_sharpe_ratio_row[risky_asset1_ex2], max_sharpe_ratio_row[risky_asset2_ex2]
    max_sharpe, max_sharpe_expected, max_sharpe_std = max_sharpe_ratio_row["Sharpe Ratio"], max_sharpe_ratio_row["Expected return"], max_sharpe_ratio_row["Standard deviation"]

    return df, max_sharpe, max_sharpe_weight1, max_sharpe_weight2


@st.cache_data()
def Q6_compute_weights():
    weight_portfoliosR = np.round(np.arange(0,1.01,0.01),2)
    weight_riskfree = 1 - weight_portfoliosR

    weight_risk1_full = []
    weight_risk2_full = []
    weight_riskportfolio = []
    weight_riskfree = []

    # Weights in risky portfolio R (weight=1 for risky portfolio R)
    weight_risk1_portfolioR = []
    weight_risk2_portfolioR = []

    for wp in weight_portfoliosR:
        for w1 in weight_portfoliosR:
            weight_risk1_full.append(w1)
            weight_risk2_full.append(wp-w1)
            weight_riskportfolio.append(wp)
            weight_riskfree.append(1-wp)

            weight_risk1_portfolioR.append(w1/wp)
            weight_risk2_portfolioR.append((wp-w1)/wp)
            
    return weight_risk1_full, weight_risk2_full, weight_riskportfolio, weight_riskfree, weight_risk1_portfolioR, weight_risk2_portfolioR


@st.cache_data()
def Q6_portfolio_tworisky_riskfree(asset1_returns, asset2_returns):
    
    weight_risk1_full, weight_risk2_full, weight_riskportfolio, weight_riskfree, weight_risk1_portfolioR, weight_risk2_portfolioR = Q6_compute_weights()
    
    df_full_portfolio = pd.DataFrame({risky_asset1_ex2:np.round(weight_risk1_full,2),
                                    f"{risky_asset1_ex2} (in risky portfolio)":np.round(weight_risk1_portfolioR,2),
                                    risky_asset2_ex2:np.round(weight_risk2_full,2),
                                    f"{risky_asset2_ex2} (in risky portfolio)":np.round(weight_risk2_portfolioR,2),
                                    "risky portfolio":np.round(weight_riskportfolio,2),
                                    "risk-free":np.round(weight_riskfree,2)})


    asset1_expected_return = np.mean(asset1_returns)
    asset1_std_dev = np.std(asset1_returns, ddof=1)
    asset2_expected_return = np.mean(asset2_returns)
    asset2_std_dev = np.std(asset2_returns, ddof=1)
    asset12_corr = np.corrcoef(asset1_returns, asset2_returns)[0,1]
    
    # Compute expected return and std of each portfolio 
    expected_returns_portfolios = np.array([w1*asset1_expected_return + w2*asset2_expected_return + w3*0.02 for w1,w2,w3 in zip(weight_risk1_full,weight_risk2_full,weight_riskfree)])
    std_portfolios = np.array([(w1*asset1_std_dev)**2 + (w2*asset2_std_dev)**2 + 2*w1*w2*asset12_corr*asset1_std_dev*asset2_std_dev for w1,w2 in zip(weight_risk1_full,weight_risk2_full)])
    std_portfolios = np.sqrt(std_portfolios)

    df_full_portfolio["Expected return"] = expected_returns_portfolios
    df_full_portfolio["Standard deviation"] = std_portfolios

    # Find efficient portfolios 
    df_efficient_portfolios = df_full_portfolio.loc[(df_full_portfolio[f"{risky_asset1_ex2} (in risky portfolio)"]==max_sharpe_weight1) & (df_full_portfolio[f"{risky_asset2_ex2} (in risky portfolio)"]==max_sharpe_weight2)].drop(columns=[f"{risky_asset1_ex2} (in risky portfolio)",f"{risky_asset2_ex2} (in risky portfolio)"])
    df_efficient_portfolios.reset_index(drop=True, inplace=True)
    
    return df_efficient_portfolios





#################################################################################################################
#                                        EXERCICE 2 - Two risky assets
#################################################################################################################

if lab_numbers == "02 - Two risky assets":

    startdate = datetime.now()

    ##################################### SIDEBAR ##########################################
    
    risky_asset1_ex2 = st.sidebar.selectbox('Select the first risky stock ➡️', list_risky_assets)
    
    if risky_asset1_ex2:
        risky_asset2_ex2 = st.sidebar.selectbox('Select the second risky stock ➡️', [elem for elem in list_risky_assets if elem != risky_asset1_ex2])


    ##################################### TITLE ##########################################
    st.markdown("## 02 - Two risky assets")
    st.info("""The purpose of this exercise is to understand how to **construct efficient portfolios** if you can invest in two risky assets.""")
    st.sidebar.markdown("  ")

    
    ##################################### QUESTION 1 #####################################
    st.markdown("   ")
    st.markdown("   ")

    st.subheader("Question 1 📝")
    
    ########### Q1 PART 1
    st.markdown('''<p style="font-size: 22px;"> Download prices for two risky stocks. <b>Compute their realized returns</b>.  
                Next, estimate the <b>expected returns</b> and <b>standard deviations of returns</b> on these two stocks. 
                Finally, compute the <b>correlation of the returns</b> on these two stocks.''',
                unsafe_allow_html=True)

    st.markdown("  ")


    ######################## LOAD DATASETS ############################
    
    ## Dataframe for each stock
    df_asset1_ex2 = load_csv(f"data/stocks/{risky_asset1_ex2}.csv")
    df_asset2_ex2 = load_csv(f"data/stocks/{risky_asset2_ex2}.csv")


    ## Dataframe with both stocks 
    two_assets = [risky_asset1_ex2, risky_asset2_ex2]
    two_assets.sort()
    df_asset_ex2_merge = load_csv(f"data/two_stocks/{two_assets[0]}_{two_assets[1]}.csv")
    
    
    
    ############################### VIEW PLOTS #############################   
    
    chart1 = two_stocks_charts(df_asset_ex2_merge, risky_asset1_ex2, risky_asset2_ex2)
    st.altair_chart(chart1, use_container_width=True)
    
    
    
    ####################### SHOW DOUBLE DATASET + DOWNLOAD BUTTON ############################

    st.markdown(f"**View Price and Dividends for {risky_asset1_ex2} and {risky_asset2_ex2}**")
    st.dataframe(df_asset_ex2_merge, use_container_width=True)
    
    # Convert the DataFrame to Excel bytes
    excel_data = create_excel_file(df_asset_ex2_merge)

    # Use the download button to allow users to download the Excel file
    download_button_stocks = st.download_button(
        label=f"📥 **Download the {risky_asset1_ex2} and {risky_asset2_ex2} stock data**",
        data=excel_data,
        file_name=f"{risky_asset1_ex2}_{risky_asset2_ex2}_Ex2.xlsx",
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    
    st.markdown(" ")
    st.markdown(" ")
    
    
    
    
    
    ############################## RISKY STOCK 1 ##################################


    st.subheader(f"Risky stock 1: **{risky_asset1_ex2}** 📋")
    st.markdown("  ")


    ## Compute holding-period returns, expected returns, std 
    asset1_returns = Q1_compute_holdingperiod_returns(df_asset1_ex2)    


    ## Holding-period returns
    st.write(f"**Compute the holding-period returns**")

    # Upload answer
    upload_file = st.file_uploader("Drop your results in an excel file (.xlsx)", key="Ex2.Q1.11",type=['xlsx'])
    answer_2_Q1_1a = ""
    
    if upload_file is not None:
        answer_2_Q1_1a = "Received"

    st.markdown("  ")
    st.markdown("  ")


    ## Expected returns
    st.write(f"**Compute the expected return**")
    answer_2_Q1_1b = st.text_input("Enter your results","", key="Ex2.Q1.12")
    st.markdown("  ")


    ## Standard deviation of returns
    st.write(f"**Compute the standard deviation**")
    answer_2_Q1_1c = st.text_input(f"Enter your results","", key="Ex2.Q2.13")
    st.markdown("  ")


    if st.checkbox(f'**Solutions - Question 1 ({risky_asset1_ex2})** ✅'):
        returns_result = pd.DataFrame({"Year":df_asset1_ex2["Year"].iloc[1:], f"Return ({risky_asset1_ex2})":asset1_returns})
        
        st.success("**Instruction**: *Please select one stock and compute its realized (holding-period) returns. Assume that holding, is one year.*")
        st.dataframe(returns_result)
        
        st.markdown(" ")

        asset_expected_return = np.round(np.mean(asset1_returns),4)
        asset_std_dev = np.round(np.std(asset1_returns, ddof=1), 4)
        
        st.success(f"**Instruction**: *Compute the expected return and standard deviation of the holding-period returns*")
        st.markdown(f"""- **Expected return**: {asset_expected_return} 
- **Standard deviation**: {asset_std_dev}
                    """, unsafe_allow_html=True)
        
        
    st.markdown("  ")
    st.markdown("  ")




    ######################## RISKY ASSET 2 ############################

    st.subheader(f"Risky stock 2: **{risky_asset2_ex2}** 📋")
    st.markdown("  ")


    ## Compute holding-period returns
    asset2_returns = Q1_compute_holdingperiod_returns(df_asset2_ex2)


    ## Holding-period returns
    st.write(f"**Compute the holding-period returns**")
    
    upload_expected_return = st.file_uploader("Drop your results in an excel file (.xlsx)", key="Ex2.Q1.21",type=['xlsx'])
    answer_2_Q1_2a = ""
    if upload_expected_return is not None:
        answer_2_Q1_2a = u"Received"

    st.markdown("  ")


    ## Expected returns
    st.write(f"**Compute the expected return**")
    answer_2_Q1_2b = st.text_input("Enter your results","", key="Ex2.Q1.22")
    st.markdown("  ")


    ## Standard deviation
    st.write(f"**Compute the standard deviation**")
    answer_2_Q1_2c = st.text_input(f"Enter your results","", key="Ex2.Q2.23")
    st.markdown("  ")
    
    
    if st.checkbox(f'**Solutions - Question 1 ({risky_asset2_ex2})** ✅'):
        returns_result = pd.DataFrame({"Year":df_asset2_ex2["Year"].iloc[1:], f"Return ({risky_asset2_ex2})":asset2_returns})
        st.success("**Instruction**: *Please select one stock and compute its realized (holding-period) returns. Assume that holding, is one year.*")
        st.dataframe(returns_result)
        
        st.markdown(" ")

        asset_expected_return = np.round(np.mean(asset2_returns),4)
        asset_std_dev = np.round(np.std(asset2_returns, ddof=1), 4)
        
        st.success(f"**Instruction**: *Compute the expected return and standard deviation of the holding-period returns*")
        st.markdown(f"""- **Expected return**: {asset_expected_return} 
- **Standard deviation**: {asset_std_dev}
                    """, unsafe_allow_html=True)
        
        
    st.markdown("  ")
    st.markdown("  ")



    
    ############## CORRELATION ASSET 1 AND ASSET 2 ##############
    
    st.subheader(f"Correlation between {risky_asset1_ex2} and {risky_asset2_ex2} 📈")
    st.markdown("  ")
    
    # Input answers
    st.write(f"**Compute the correlation between both assets**")
    answer_2_Q1_3 = st.text_input(f"Enter your results","", key="Ex2.Q2.3")
    st.markdown("  ")

    if st.checkbox(f'**Solutions - Question 1 (Correlation)** ✅'):
        asset12_corr = np.corrcoef(asset1_returns, asset2_returns)[0,1]
        st.markdown(f"Correlation between {risky_asset1_ex2} and {risky_asset2_ex2}: **{np.round(asset12_corr,3)}**.")
        

    
    st.markdown("   ")
    st.markdown("   ") 
    st.markdown("   ")     
    st.markdown("   ")
    st.markdown("   ")






    ##################################### QUESTION 2 #####################################

    st.subheader("Question 2 📝")

    st.markdown('''<p style="font-size: 22px;"> Compose different <b>portfolios of two risky assets</b> by investing in one risky asset x% of your wealth and in the other asset (1-x)%.
                Vary x from -50% to 150% with an increment of 1%. Compute the <b>expected returns</b> and <b>standard deviations</b> of the resulting portfolios.''', 
                unsafe_allow_html=True)
    
    st.info("**Hint**: Do not forget about the correlation between the returns on these two stocks.")

    st.markdown("  ")
    st.markdown("  ")
    
    

    # Feasible portfolios graph
    # chart_portfolios = alt.Chart(df_exp_std_return_portfolios).mark_circle(size=40).encode(y="Expected return",x="Standard deviation")

    weight_portfolios = np.round(np.arange(-0.5,1.55,0.01),2)
    df_exp_std_return_portfolios = Q2_return_std_portfolios_risky(asset1_returns, asset2_returns, weight_portfolios)

    st.write("**Compute the expected return and standard deviation for each portfolio**")

    upload_expected_return = st.file_uploader("Drop your results in an excel file (.xlsx)", key="Q3.21", type=['xlsx'])
    answer_2_Q2 = ""
    if upload_expected_return is not None:
        answer_2_Q2 = "Received"

    st.markdown("  ")
    
    if st.checkbox(f'**Solutions - Question 2** ✅'):
        st.dataframe(df_exp_std_return_portfolios)
    



    st.markdown("   ")
    st.markdown("   ") 
    st.markdown("   ")     
    st.markdown("   ")
    st.markdown("   ") 






    ##################################### QUESTION 3 #####################################

    st.subheader("Question 3 📝")

    st.markdown('''<p style="font-size: 22px;"> Indicate the set of <b>feasible portfolios</b> and the set of <b>efficient portfolios</b>. Next, <b>draw a graph in which you represent the portfolios</b>, that is, the sigma-expected return pairs, you obtain with different combinations of the two risky assets.''', 
                unsafe_allow_html=True)
    
    st.markdown(" ")

    ## 1. Set of feasible portfolio
    st.write("**What is the set of feasible portfolios ?**")
    answer_2_Q3_1 = st.text_area("Write your answer here", default_text, key="Q3.Ex2.11")

    st.markdown("  ")
    st.markdown("   ")


    ## 2. Set of efficient portfolios
   
    st.write("**What is the set of efficient portfolios ?**")

    upload_efficient_portfolios = st.file_uploader("Drop your results in an excel file (.xlsx)", key="Q3.Ex2.U12",type=['xlsx'])
    answer_2_Q3_2 = ""
    if upload_efficient_portfolios is not None:
        answer_2_Q3_2 = "Received"

    
    st.markdown("  ")
    st.markdown("   ")
    


    ## Draw the set of feasible portfolios 
    st.write("**Draw the set of feasible portfolios**")

    upload_graph = st.file_uploader("Drop the graph as an image (jpg, jpeg, png)", key="Q3.Ex2.13", type=['jpg','jpeg','png'])
    answer_2_Q3_3 = ""
    if upload_graph is not None:
        answer_2_Q3_3 = "Received"
    

        
    st.markdown("   ")
    
    if st.checkbox(f'**Solutions - Question 3** ✅'):
        st.success("**Instruction**: *What is the set of feasible portfolios ?*")
        st.markdown(f"The **set of all portfolios** (standard deviation-expected return) that can be obtained by building portfolios with {risky_asset1_ex2} and {risky_asset2_ex2}.")
        
        df_ex2_q3_efficient = Q3_efficient_portfolios(df_exp_std_return_portfolios)
        
        st.markdown("  ")
        
        st.success("**Instruction**: *What is the set of efficient portfolios ?*")
        st.markdown("The portfolios that **offer the greatest expected rate of return for each level of standard deviation** (risk).")
        # st.dataframe(df_ex2_q3_efficient.iloc[min_std_q3_exp:].reset_index(drop=True))
        st.dataframe(df_ex2_q3_efficient)
        
        st.markdown("  ")
        
        st.success("**Instruction**: *Draw the set of feasible portfolios*")
        
        chart_portfolios_q3 = alt.Chart(df_exp_std_return_portfolios).mark_circle(size=20).encode(
            x=alt.X('Standard deviation:Q'),
            y=alt.Y('Expected return:Q'))
        
        st.altair_chart(chart_portfolios_q3.interactive(), use_container_width=True)
        #st.dataframe(df_exp_std_return_portfolios)

    st.markdown("   ")
    st.markdown("   ") 
    st.markdown("   ")     
    st.markdown("   ")
    st.markdown("   ")





    ##################################### QUESTION 4 #####################################

    st.subheader("Question 4 📝")

    st.markdown('''<p style="font-size: 22px;"> Assume that you cannot short-sell any of the risky assets. 
                Indicate the new <b>set of feasible portfolios</b> and the new <b>set of efficient portfolios</b>.''', 
                unsafe_allow_html=True)
    
    
    st.markdown("  ")


    ## 1. Set of feasible portfolios
    st.write("**What is the set of feasible portfolios ?**")
    
    upload_portfolios = st.file_uploader("Drop your results in an excel file (.xlsx)", key="Q4.Ex2.U11",type=['xlsx'])
    answer_2_Q4_1 = ""
    if upload_portfolios is not None:
        answer_2_Q4_1 = "Received"

        
    st.markdown("  ")
    st.markdown("  ")


    ## 2. Set of efficient portfolios
    st.write("**What is the set of efficient portfolios ?**")
    upload_efficient_portfolios = st.file_uploader("Drop your results in an excel file (.xlsx)", key="Q4.Ex2.U12",type=['xlsx'])
    
    answer_2_Q4_2 = ""
    if upload_efficient_portfolios is not None:
        answer_2_Q4_2 = "Received"

        
    st.markdown("  ")
        
    if st.checkbox(f'**Solutions - Question 4** ✅'):
        df_exp_std_return_portfolios_q4 = df_exp_std_return_portfolios.loc[(df_exp_std_return_portfolios[risky_asset1_ex2]>=0) & (df_exp_std_return_portfolios[risky_asset2_ex2]>=0)]        

        st.success("**Instruction**: *What is the set of feasible portfolios ?*")
        st.markdown(f"The set of feasible portfolios are the **portfolios with only positive or null weights in {risky_asset1_ex2} and {risky_asset2_ex2}.**")
        st.dataframe(df_exp_std_return_portfolios_q4)        
        
        df_ex2_q4_efficient = Q3_efficient_portfolios(df_exp_std_return_portfolios)
        
        st.markdown("  ")
        
        st.success("**Instruction**: *What is the set of efficient portfolios ?*")
        st.dataframe(df_ex2_q4_efficient)
                
        
    st.markdown("   ")
    st.markdown("   ") 
    st.markdown("   ")     
    st.markdown("   ")
    st.markdown("   ")






    ##################################### QUESTION 5 #####################################

    st.subheader("Question 5 📝")

    st.markdown('''<p style="font-size: 22px;"> Assume that you also have a risk-free asset with a rate of return of 2% per annum. 
                <b>Find the tangency portfolio</b>.''', 
                unsafe_allow_html=True)
    
    st.info("**Hint**: Compute the Sharpe ratio (the reward-to-variability ratio) for all feasible portfolios in Question 2. Find the portfolio with the maximal one.")
    st.markdown(" ")

    st.write("**What is the tangency portfolio ?**")
    answer_2_Q5 = st.text_area("Write your answer here", default_text, key="UQ5.Ex2")
    
    df_exp_std_return_portfolios, max_sharpe, max_sharpe_weight1, max_sharpe_weight2 = Q5_tangency_portfolio(df_exp_std_return_portfolios)

    if st.checkbox(f'**Solutions - Question 5** ✅'):
        st.markdown(f"""The tangency portfolio is the portfolio where you invest **{max_sharpe_weight1}** in {risky_asset1_ex2} and **{max_sharpe_weight2}** in {risky_asset2_ex2}, with a sharpe ratio of **{max_sharpe}**. <br>
                    *The tangency portfolio is highlighted in green in the dataset*""", unsafe_allow_html=True)
        st.dataframe(df_exp_std_return_portfolios.style.highlight_max(color="lightgreen", subset="Sharpe Ratio",axis=0))
        
    st.markdown("   ")
    st.markdown("   ") 
    st.markdown("   ")     
    st.markdown("   ")
    st.markdown("   ")



    ######################################### QUESTION 6 #########################################

    st.subheader("Question 6 📝")

    ### Q5 PART 1
    st.markdown('''<p style="font-size: 22px;">Indicate the <b>set of efficient portfolios</b> that you can achieve if you invest in two risky assets and one risk-free asset.''', 
                unsafe_allow_html=True)

    ## Efficient portfolios ?
    st.write("**What is the set of efficient portfolios ?**")
    
    upload_efficient_portfolios = st.file_uploader("Drop your results in an excel file (.xlsx)", key="UQ6.Ex6",type=['xlsx'])
    answer_2_Q6 = ""
    if upload_efficient_portfolios is not None:
        answer_2_Q6 = "Received"





    if st.checkbox(f'**Solutions - Question 6** ✅'):
        st.markdown(f"""The efficient portfolios are the portfolios with a **combination of the risk-free asset and the tangency portfolio of Question 5.** <br>
                    *The weights for {risky_asset1_ex2} and {risky_asset2_ex2} where computed based on the overall portfolio, not on the risky portfolio (the portfolio with only risky assets).*""", unsafe_allow_html=True)
        
        df_efficient_portfolios = Q6_portfolio_tworisky_riskfree(asset1_returns, asset2_returns)
        st.markdown(" "
                    )
        st.dataframe(df_efficient_portfolios)
        
    st.markdown(" ")
    st.markdown(" ")
    st.markdown("#### Congratulations you finished Exercise 2 🎉")




    ######### SUBMIT ANSWERS #########
    list_answer = [answer_2_Q1_1a,
    answer_2_Q1_1b,
    answer_2_Q1_1c,
    answer_2_Q1_2a,
    answer_2_Q1_2b,
    answer_2_Q1_2c,
    answer_2_Q1_3,
    answer_2_Q2,
    answer_2_Q3_1,
    answer_2_Q3_2,
    answer_2_Q3_3,
    answer_2_Q4_1,
    answer_2_Q4_2,
    answer_2_Q5,
    answer_2_Q6]

    ## SUBMISSION EXERCICE 1
    #if st.button('**Submit answers Ex2**'):
        ######### CONNEXION WITH GOOGLE SHEET API ##########
    with st.sidebar:
        if st.button('**Submit answers Ex2**'):
            with st.spinner('Processing...'):

                ## Connect to google sheet
                credentials = service_account.Credentials.from_service_account_info(
                    st.secrets["gcp_service_account"],
                    scopes=scope,
                )

                gc = gspread.authorize(credentials)
                answers = [x for x in list_answer if x not in [np.nan,"", None]]
                count = len(answers)
                select_assets = "-".join(two_assets)

                list_answers_ = [select_teacher,
                select_code,
                student_ids,
                2,
                select_assets,
                str(startdate),
                str(datetime.now()),
                count,
                f"{round((count/len(list_answer))*100,1)}%",
                answer_2_Q1_1a,
                answer_2_Q1_1b,
                answer_2_Q1_1c,
                answer_2_Q1_2a,
                answer_2_Q1_2b,
                answer_2_Q1_2c,
                answer_2_Q1_3,
                answer_2_Q2,
                answer_2_Q3_1,
                answer_2_Q3_2,
                answer_2_Q3_3,
                answer_2_Q4_1,
                answer_2_Q4_2,
                answer_2_Q5,
                answer_2_Q6]
                

                ## Append new row to the google sheet
                sh = gc.open('App-finance-HEC-students-results').get_worksheet(1)
                insertRow = list_answers_
                # st.write(list_answers_)
                sh.append_row(insertRow)

                sh_looker = gc.open('App-finance-HEC-students-results').get_worksheet(2)
                insertRow2 = list_answers_[:9]
                sh_looker.append_row(insertRow2)
            
            st.info('**Your answers have been submitted !**')


    st.sidebar.divider()
    st.sidebar.image(image_hiparis, width=150)
    url = "https://www.hi-paris.fr/"
    st.sidebar.markdown("**Made in collaboration with: [Hi! PARIS Engineering Team](%s)**" % url)



