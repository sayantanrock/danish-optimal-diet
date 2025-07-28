# -*- coding: utf-8 -*-
"""
Created on Wed Jun 25 12:05:19 2025

@author: says
"""

import streamlit as st
import pandas as pd
import altair as alt

def model_linear():
   
    #col1.title('How does your optimal diet looks like ?')
    col1, col2 = st.columns([4, 2])
    

    st.sidebar.header('Select Category')
    custom_options = [0, 10, 20, 30, 40, 50, 60, 68, 70, 73]
    cf_in = st.sidebar.select_slider("Reduce Carbon footprint by (%)", options=custom_options)




    ######################### INITIAL DATA MANIPULATION FOR APP READY DATASET########################
    df = pd.read_excel("./data_LP.xlsx")
    daly = pd.read_excel("./data_LP.xlsx", sheet_name='DALY', header = 0)
    slack = pd.read_excel("./data_LP.xlsx", sheet_name='SLACK', header = 0)
    #############################################################################################
    ##################Reshape the OPTIMAL DIET table############################################
    ############## DATA PREPROCESSING FOR MAIN FOOD GROUP (7) CHART ##########################################
    df_temp = df.drop(columns=["Foodgroup","Group"])
    df_long1 = df_temp.melt(id_vars=["Aggregatename", "Aggregategroup", "Baseline"], var_name="CF", value_name="Value")
    df_long1["CF"] = df_long1["CF"].str.extract(r'C(\d+)', expand=False).astype(int)    
    data_filtered1 = df_long1[(df_long1['CF'] ==  cf_in )]
    data_filtered1.drop(columns=["CF"], inplace=True)
    data_filtered1.rename(columns={"Value": "Optimal diet"}, inplace=True)
    ############## DATA PREPROCESSING FOR FOOD SUB GROUP (22) CHART ##########################################
    df_temp = df.drop(columns=["Aggregatename","Aggregategroup"])
    df_long = df_temp.melt(id_vars=["Foodgroup", "Group", "Baseline"], var_name="CF", value_name="Value")
    df_long["CF"] = df_long["CF"].str.extract(r'C(\d+)', expand=False).astype(int)
    data_filtered = df_long[(df_long1['CF'] ==  cf_in )]
    data_filtered.drop(columns=["CF"], inplace=True)
    data_filtered.rename(columns={"Value": "Optimal diet"}, inplace=True)
    ##################################################################################################
    
    data_group = data_filtered.groupby(['Group'], sort=True)[['Baseline','Optimal diet']].sum()
    data_group['Baseline'] = data_group['Baseline'].apply(lambda x: round(x, 2))
    data_group['Optimal diet'] = data_group['Optimal diet'].apply(lambda x: round(x, 2))

    data_group.drop(0, inplace = True)
    data_group['Food Group'] = ['WHOLE GRAIN', 'DAIRY', 'FISH', 'FRUIT', 'VEGETABLE', 'MEAT', 'NUTS', 'LEGUMES']
    data_group.columns = data_group.columns.str.strip()
    data_group = data_group[['Food Group', 'Baseline', 'Optimal diet']]
    data_melted = data_group.melt(id_vars='Food Group', 
                            value_vars=['Baseline', 'Optimal diet'], 
                            var_name='Diet Type', 
                            value_name='Consumption')
    chart_foodgroup = alt.Chart(data_melted).mark_bar().encode(
        y=alt.Y('Food Group:N', title='Food Group'),
        x=alt.X('Consumption:Q', title='Consumption (g/day)'),
        color=alt.Color('Diet Type:N', title='Diet Type',scale=alt.Scale(scheme='set2')),
        yOffset='Diet Type:N'  # Optional: or use x='Variable:N' for grouped bars
    ).properties(width=600, height=600)
    ##################################################################################################
    ########################  Reshape the DALY table ################################################## df_long["CF"].str.extract(r'C(\d+)', expand=False).astype(int)
    ##################################################################################################
    daly_long = daly.melt(id_vars=["DISEASES", "BASELINE"], var_name="CF", value_name="Value")
    daly_long['CF'] = daly_long["CF"].str.extract(r'C(\d+)', expand=False).astype(int)

    ################### DATA PREPROCESSING FOR DALY CHART ###########################################
    daly_filtered = daly_long[(daly_long['CF'] ==  cf_in )]
    daly_filtered.drop(columns=["CF"], inplace=True)
    daly_filtered.rename(columns={"Value": "OPTIMAL"}, inplace=True)
    daly_long_melted = daly_filtered.melt(id_vars='DISEASES', 
                            value_vars=['BASELINE', 'OPTIMAL'], 
                            var_name='Diet Type', 
                            value_name='Burden')
    chart_daly = alt.Chart(daly_long_melted).mark_bar().encode(
        x=alt.X('DISEASES:N', title='Health Outcome'),
        y=alt.Y('Burden:Q', title='DALY/100k'),
        color=alt.Color('Diet Type:N', title='Diet Type',scale=alt.Scale(scheme='set2')),
        xOffset='Diet Type:N'  # Optional: or use x='Variable:N' for grouped bars
    ).properties(width=600, height=400)
    #############################################################################################
    ##################Reshape the SLACK table############################################
    slack.drop(['Target Value'], inplace=True, axis=1)
    slack_long = slack.melt(id_vars=["Nutrient", "Baseline"], var_name="CF", value_name="Value")
    slack_long['CF'] = slack_long['CF'].str.extract(r'C(\d+)', expand=False).astype(int)

    ############## DATA PREPROCESSING FOR SLACK CHART ##########################################
    slack_filtered = slack_long[(slack_long['CF'] ==  cf_in )]
    slack_filtered.drop(columns=["CF"], inplace=True)
    slack_filtered.rename(columns={"Value": "Optimal diet"}, inplace=True)
    ########################## DIVIDE SLACK DATA IN TO TWO PARTS ################################
    ############# ONE FOR PER GRAMS  #########################
    slack_g = slack_filtered.iloc[[0,1,2,3,9,10,12]]
    slack_mg = slack_filtered.iloc[[15,16,18,20]]
    slack_mineral_high = slack_filtered.iloc[[4,19,22,23,24,25]]
    slack_mineral_low = slack_filtered.iloc[[14,17,21,26,27,28,29]]
    slack_g_melted = slack_g.melt(id_vars='Nutrient', 
                            value_vars=['Baseline', 'Optimal diet'], 
                            var_name='Diet Type', 
                            value_name='Consumption')
    slack_mg_melted = slack_mg.melt(id_vars='Nutrient', 
                            value_vars=['Baseline', 'Optimal diet'], 
                            var_name='Diet Type', 
                            value_name='Consumption')
    slack_mineral_high_melted = slack_mineral_high.melt(id_vars='Nutrient', 
                            value_vars=['Baseline', 'Optimal diet'], 
                            var_name='Diet Type', 
                            value_name='Consumption')
    slack_mineral_low_melted = slack_mineral_low.melt(id_vars='Nutrient', 
                            value_vars=['Baseline', 'Optimal diet'], 
                            var_name='Diet Type', 
                            value_name='Consumption')

    chart_slack_g_melted= alt.Chart(slack_g_melted).mark_bar().encode(
        x=alt.X('Nutrient:N', title='Nutrient'),
        y=alt.Y('Consumption:Q', title='Consumption (g/day)'),
        color=alt.Color('Diet Type:N', title='Diet Type',scale=alt.Scale(scheme='dark2')),
        xOffset='Diet Type:N'  # Optional: or use x='Variable:N' for grouped bars
    ).properties(width=600, height=300)
    chart_slack_mg_melted= alt.Chart(slack_mg_melted).mark_bar().encode(
        x=alt.X('Nutrient:N', title='Nutrient'),
        y=alt.Y('Consumption:Q', title='Consumption (mg/day)'),
        color=alt.Color('Diet Type:N', title='Diet Type',scale=alt.Scale(scheme='dark2')),
        xOffset='Diet Type:N'  # Optional: or use x='Variable:N' for grouped bars
    ).properties(width=600, height=300)
    chart_slack_mineral_high_melted= alt.Chart(slack_mineral_high_melted).mark_bar().encode(
        x=alt.X('Nutrient:N', title='Nutrient'),
        y=alt.Y('Consumption:Q', title='Consumption (mg/day)'),
        color=alt.Color('Diet Type:N', title='Diet Type',scale=alt.Scale(scheme='dark2')),
        xOffset='Diet Type:N'  # Optional: or use x='Variable:N' for grouped bars
    ).properties(width=600, height=300)
    chart_slack_mineral_low_melted= alt.Chart(slack_mineral_low_melted).mark_bar().encode(
        x=alt.X('Nutrient:N', title='Nutrient'),
        y=alt.Y('Consumption:Q', title='Consumption (mg/day)'),
        color=alt.Color('Diet Type:N', title='Diet Type',scale=alt.Scale(scheme='dark2')),
        xOffset='Diet Type:N'  # Optional: or use x='Variable:N' for grouped bars
    ).properties(width=600, height=300)
    
    temp = {'BURDEN':'DALY', 'BASELINE':[daly_filtered['BASELINE'].sum()],'OPTIMAL':[daly_filtered['OPTIMAL'].sum()]}
    daly_summary = pd.DataFrame(temp)
    daly_summary_melted = daly_summary.melt(id_vars='BURDEN', 
                            value_vars=['BASELINE', 'OPTIMAL'], 
                            var_name='Diet Type', 
                            value_name='Burden')
    chart_daly_summary = alt.Chart(daly_summary_melted).mark_bar().encode(
        x=alt.X('Diet Type:N', title='Diet'),
        y=alt.Y('Burden:Q', title='DALY/100k'),
        color=alt.Color('Diet Type:N', title='Diet Type',scale=alt.Scale(scheme='set1')),
        xOffset='Diet Type:N'  # Optional: or use x='Variable:N' for grouped bars
    ).properties(width=200, height=300)
    
    slack_filtered.reset_index(drop=True, inplace=True)
    temp1 = {'cf':'Carbon', 'BASELINE':[slack_filtered['Baseline'].iloc[6]],'OPTIMAL':slack_filtered['Optimal diet'].iloc[6]}
    cf_summary = pd.DataFrame(temp1)
    cf_summary_melted = cf_summary.melt(id_vars='cf', 
                            value_vars=['BASELINE', 'OPTIMAL'], 
                            var_name='Diet Type', 
                            value_name='CF')
    chart_cf_summary = alt.Chart(cf_summary_melted).mark_bar().encode(
        x=alt.X('Diet Type:N', title='Diet'),
        y=alt.Y('CF:Q', title='Kg'),
        color=alt.Color('Diet Type:N', title='Diet Type',scale=alt.Scale(scheme='set1')),
        xOffset='Diet Type:N'  # Optional: or use x='Variable:N' for grouped bars
    ).properties(width=200, height=300)
    
    #data_filtered.drop(['CF'], axis=1, inplace=True)
    data_filtered1.reset_index(drop=True,inplace=True)
    data_group1 = data_filtered1.groupby('Aggregategroup').agg({
    'Aggregatename': lambda x: ', '.join(sorted(set(x))),  # unique names
    'Baseline': 'sum',
    'Optimal diet': 'sum'
    })
    data_group1['Baseline'] = data_group1['Baseline'].apply(lambda x: round(x, 2))
    data_group1['Optimal diet'] = data_group1['Optimal diet'].apply(lambda x: round(x, 2))
    data_group1.rename(columns={"Aggregatename": "Food Product"})
    data_group1.reset_index(drop=True, inplace=True)
    
    col2.subheader("Burden of your Diet")
    col2.altair_chart(chart_daly_summary, use_container_width=True)
    col2.subheader("Carbon Footprint of your Diet")
    col2.altair_chart(chart_cf_summary, use_container_width=True)
    ###########################################################################################################
    #################### STYLING THE TABLE FOR BETTER VISUAL EFFECTS ##########################################
    ###########################################################################################################
    col1.subheader('Optimal Diet Composition')
    col1.altair_chart(chart_foodgroup, use_container_width=True)  
    col1.dataframe(data_group.round(2))
    col1.subheader('Burden of your Optimal Diet (DALY/100k) ')
    col1.altair_chart(chart_daly, use_container_width=True)
    col1.subheader('Nutritional Composition of your Optimal Diet ')
    col1.altair_chart(chart_slack_g_melted, use_container_width=True)
    col1.altair_chart(chart_slack_mg_melted, use_container_width=True)
    col1.altair_chart(chart_slack_mineral_high_melted, use_container_width=True)
    col1.altair_chart(chart_slack_mineral_low_melted, use_container_width=True)
    col1.subheader("Optimal Diet(g/day)")
    col1.dataframe(data_group1.round(2))
 

   