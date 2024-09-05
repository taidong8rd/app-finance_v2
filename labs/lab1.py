import pandas as pd
import numpy as np
from datetime import datetime
from PIL import Image # display an image

import gspread
from google.oauth2 import service_account

import altair as alt
from PIL import Image
import streamlit as st

from utils import load_csv, create_excel_file, submit_answers_page1



scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]


@st.cache_data()
def compute_riskfree(df_risky):
    returns = np.array([0.02 for i in range(df_risky.shape[0]-1)])
    exp_returns = np.mean(returns)
    std = np.std(returns, ddof=1)
    
    return returns, exp_returns, std


@st.cache_data()
def Q1_compute_holdingperiod_returns(df_risky):
    asset1_returns = (df_risky["Price"][1:].to_numpy() - df_risky["Price"][:-1].to_numpy() + df_risky["Dividends"].to_numpy()[1:])/df_risky["Price"][:-1].to_numpy()    
    return asset1_returns



@st.cache_data()
def Q3_return_std_portfolios(asset1_returns, weight_risky_portfolios, risky_asset, riskfree_std, riskfree_exp_returns):
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


@st.cache_data()
def Q4_feasible_portfolios_exp(df_portfolios, risky_asset):

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
def Q4_feasible_portfolios_std(df_portfolios, risky_asset):
    
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






def lab1_code(select_teacher, select_code, student_ids):

    startdate = datetime.now()
    default_text = ""
    list_risky_assets = ["ACMTA", "ACU", "AIR", "ASA", "BKTI", "CECO", "PRG"]


    #################################### SIDEBAR ##################################
    risky_asset = st.sidebar.selectbox("Select a risky asset ➡️", list_risky_assets, key="select_risky")
    


    ################################### DATAFRAMES ###############################

    # Risky asset dataframe (df_risky)
    # df_risky = data.loc[data["Stock"]==risky_asset]
    df_risky = load_csv(f"data/stocks/{risky_asset}.csv")
    
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

                
    # Convert the DataFrame to Excel bytes
    excel_data = create_excel_file(df_risky.drop(columns=["Stock"]))

    # Use the download button to allow users to download the Excel file
    st.download_button(
        label=f"📥 **Download the {risky_asset} dataset**",
        data=excel_data,
        file_name=f"{risky_asset}.xlsx",
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
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

    st.markdown("  ")
    st.markdown("  ")


    # Standard deviation
    st.write(f"**Compute the standard deviation**")
    answer_1_Q1_3 = st.text_input("Enter your results ","", key="AUQ1.2b")   
    st.markdown("   ")  
    

    
    if st.checkbox('**Solutions - Question 1** ✅'):
        asset1_returns = Q1_compute_holdingperiod_returns(df_risky)
        returns_result = pd.DataFrame({"Year":df_risky["Year"].iloc[1:], "Return":asset1_returns})
        st.success(f"""**Instruction**: Please select one stock and compute its realized (holding-period) returns. Assume that holding, is one year.""")
        st.dataframe(returns_result)
        
        st.markdown(" ")
        st.markdown(" ")
        
        asset_expected_return = np.round(np.mean(asset1_returns),4)
        asset_std_dev = np.round(np.std(asset1_returns, ddof=1), 4)
        
        st.success(f"""**Instruction**: Compute the expected return and standard deviation of the holding-period returns.""") 
        st.markdown(f"""
                    - <b>Expected return</b>: {asset_expected_return} <br>
                    - <b>Standard deviation</b>: {asset_std_dev}
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
        
        st.success("**Instruction**: *Compute the weight of each asset in your portfolio*")
        st.markdown(f"""
                    - **{risky_asset}**: {risky_weight} <br>
                    - **Risk-free asset**: {riskfree_weight}
                    """, unsafe_allow_html=True)
        
        # Compute portfolio returns, expected ret, std
        portfolio_returns = (risky_weight*asset1_returns) + (riskfree_weight*riskfree_returns)
        
        st.markdown(" ")
        
        st.success("**Instruction**: *Compute the expected return and standard deviation of the portfolio* ")
        st.markdown(f"""
                    - **Expected return**: {np.round(np.mean(portfolio_returns), 4)} <br>
                    - **Standard deviation**: {np.round(np.std(portfolio_returns, ddof=1), 4)}
                    """, unsafe_allow_html=True)
    
        
    st.markdown("   ")
    st.markdown("   ") 
    st.markdown("   ")     
    st.markdown("   ")




################## QUESTION 3 ##################

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
        
    
    st.markdown("   ")

    if st.checkbox('**Solutions - Question 3** ✅'):
        asset1_returns = Q1_compute_holdingperiod_returns(df_risky)
        weight_risky_portfolios = np.arange(0,1.01,0.01)
        df_portfolios = Q3_return_std_portfolios(asset1_returns, weight_risky_portfolios, risky_asset, riskfree_std, riskfree_exp_returns)            
        
        st.success("**Instruction**: *Compute the expected return and standard deviation for each portfolio*")
        st.dataframe(df_portfolios)
        
        st.markdown(" ")
        
        asset_expected_return = np.round(np.mean(asset1_returns),4)
        asset_std_dev = np.round(np.std(asset1_returns, ddof=1), 4)
        
        st.success("**Instruction**: *Draw the set of feasible portfolios*")
        chart_portfolios = alt.Chart(df_portfolios).mark_circle(size=40).encode(y="Expected return",x="Standard deviation")
        st.altair_chart(chart_portfolios.interactive(), use_container_width=True)
    


    st.markdown("   ")
    st.markdown("   ") 
    st.markdown("   ")     
    st.markdown("   ")
    st.markdown("   ") 




################## QUESTION 4 ##################

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
        
    
    if st.checkbox('**Solutions - Question 4** ✅'):
        asset1_returns = Q1_compute_holdingperiod_returns(df_risky)
        weight_risky_portfolios = np.arange(0,1.01,0.01)
        df_portfolios = Q3_return_std_portfolios(asset1_returns, weight_risky_portfolios, risky_asset, riskfree_std, riskfree_exp_returns)
        
        max_exp_risky, max_exp_riskfree, max_exp_value, min_exp_risky, min_exp_riskfree, min_exp_value = Q4_feasible_portfolios_exp(df_portfolios, risky_asset)
        max_std_risky, max_std_riskfree, max_std_value, min_std_risky, min_std_riskfree, min_std_value = Q4_feasible_portfolios_std(df_portfolios, risky_asset)        
        
        st.success("**Instruction**: *Can you find which portfolio has the highest expected return ?*")
        st.markdown(f"""
                    - The portfolio with **{max_exp_risky}** in the risky asset ({risky_asset}) and **{max_exp_riskfree}** in the risk free asset. <br>
                    - The portfolio's expected return is **{np.round(max_exp_value,4)}**
                    """, unsafe_allow_html=True)
        
        st.markdown(" ")
        
        st.success("**Instruction**: *Can you find which portfolio has the lowest expected return ?*")
        st.markdown(f"""
                    - The portfolio with **{min_exp_risky}** in the risky asset ({risky_asset}) and **{min_exp_riskfree}** in the risk free asset. <br>
                    - The portfolio's expected return is **{np.round(min_exp_value,4)}**
                    """, unsafe_allow_html=True)
        
        st.markdown(" ")
        
        st.success("**Instruction**: *Can you find which portfolio has the highest standard deviation ?*")
        st.markdown(f"""
                    - The portfolio with **{max_std_risky}** in the risky asset ({risky_asset}) and **{max_std_riskfree}** in the risk free asset. <br>
                    - The portfolio's standard deviation is **{np.round(max_std_value,4)}**

                    """, unsafe_allow_html=True)
        
        st.markdown(" ")
        
        st.success("**Instruction**: *Can you find which portfolio has the lowest standard deviation ?*")
        st.markdown(f"""
                    - The portfolio with **{min_std_risky}** in the risky asset ({risky_asset}) and **{min_std_riskfree}** in the risk free asset. <br>
                    - The portfolio's standard deviation is **{np.round(min_std_value,4)}**
                    """, unsafe_allow_html=True)
        
        st.markdown(" ")



    st.markdown("   ")
    st.markdown("   ") 
    st.markdown("   ")     
    st.markdown("   ")
    st.markdown("   ")





################## QUESTION 5 ##################


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
        df_portfolios = Q3_return_std_portfolios(asset1_returns, weight_risky_portfolios, risky_asset, riskfree_std, riskfree_exp_returns)             
        
        st.success(f"""**Instruction**: *Compute the expected return and standard deviation for each portfolio.*""")
        st.dataframe(df_portfolios)
        
        st.markdown(" ")
        
        asset_expected_return = np.round(np.mean(asset1_returns),4)
        asset_std_dev = np.round(np.std(asset1_returns, ddof=1), 4)
        
        st.success("""**Instruction**: *Draw the set of feasible portfolios*""")
        chart_portfolios = alt.Chart(df_portfolios).mark_circle(size=20).encode(y="Expected return",x="Standard deviation")
        st.altair_chart(chart_portfolios.interactive(), use_container_width=True)



    st.markdown("   ")
    st.markdown("   ") 
    st.markdown("   ")     
    st.markdown("   ")
    st.markdown("   ")
    



################## QUESTION 6 ##################

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
        df_portfolios = Q3_return_std_portfolios(asset1_returns, weight_risky_portfolios, risky_asset, riskfree_std, riskfree_exp_returns)
        
        max_exp_risky, max_exp_riskfree, max_exp_value, min_exp_risky, min_exp_riskfree, min_exp_value = Q4_feasible_portfolios_exp(df_portfolios, risky_asset)
        max_std_risky, max_std_riskfree, max_std_value, min_std_risky, min_std_riskfree, min_std_value = Q4_feasible_portfolios_std(df_portfolios, risky_asset)        
        
        st.success("**Instruction**: *Can you find which portfolio has the highest expected return ?*")
        st.markdown(f"""
                    - The portfolio with **{max_exp_risky}** in the risky asset ({risky_asset}) and **{max_exp_riskfree}** in the risk free asset. <br>
                    - The portfolio's expected return is **{np.round(max_exp_value,4)}**
                    """, unsafe_allow_html=True)
        
        st.markdown(" ")
        
        st.success("**Instruction**: *Can you find which portfolio has the lowest expected return ?*")
        st.markdown(f"""
                    - The portfolio with **{min_exp_risky}** in the risky asset ({risky_asset}) and **{min_exp_riskfree}** in the risk free asset. <br>
                    - The portfolio's expected return is **{np.round(min_exp_value,4)}**
                    """, unsafe_allow_html=True)
        
        st.markdown(" ")
        
        st.success("**Instruction**: *Can you find which portfolio has the highest standard deviation ?*")
        st.markdown(f"""
                    - The portfolio with **{max_std_risky}** in the risky asset ({risky_asset}) and **{max_std_riskfree}** in the risk free asset. <br>
                    - The portfolio's standard deviation is **{np.round(max_std_value,4)}**

                    """, unsafe_allow_html=True)
        
        st.markdown(" ")
        
        st.success("**Instruction**: *Can you find which portfolio has the lowest standard deviation ?* ")
        st.markdown(f"""
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
    
    answers = [x for x in list_answer if x not in [np.nan,"", None]]
    count = len(answers)

    # List with answers 
    list_answers_ = [select_teacher,
    select_code,
    student_ids,
    1,
    risky_asset,
    str(datetime.now().date()),
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


    ## SUBMISSION EXERCICE 1

    # Button to trigger submission
    submit_button = st.sidebar.button('**Submit answers Ex1**')  
    
    if 'submitted_page1' not in st.session_state:
        st.session_state['submitted_page1'] = False

    # If the button is clicked, run the submission function
    if submit_button:
        st.session_state['submitted_page1'] = True
        submit_answers_page1(list_answers_)


    # Show the success message if submission is complete
    if st.session_state.get('submitted_page1', True):
        st.sidebar.success('**Your answers have been submitted!**')
            
        st.session_state['submitted_page1'] = False

    st.sidebar.markdown("""**Note**: The green text box confirming your submission might not appear after clicking the submit button. 
                            This doesn't mean your submission wasn't registered, as it is just an app display issue.""", unsafe_allow_html=True)  


