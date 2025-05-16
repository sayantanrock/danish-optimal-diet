# -*- coding: utf-8 -*-
"""
Created on Thu May 15 15:47:38 2025

@author: says
"""

import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import altair as alt


col1, col2 = st.columns([3, 1])
col1.subheader('National Food Institute')
col1.write('**Research** **Group** **for** **Risk-Benefit**')
col1.title('How does your optimal diet looks like ?')
col2.image('DTU.png', width=50)

st.sidebar.image('DALY1.webp')
st.sidebar.header('Choose your category')
cf_in = st.sidebar.slider('Reduce Carbon footprint by (%)', min_value=0, max_value=50, step = 25)
daly_in = st.sidebar.slider('Reduce DALYs by (%)', min_value=0, max_value=50, step = 25)


######################### INITIAL DATA MANIPULATION FOR APP READY DATASET########################
df = pd.read_excel("./data.xlsx")
daly = pd.read_excel("./data.xlsx", sheet_name='DALY', header = 0)
slack = pd.read_excel("./data.xlsx", sheet_name='SLACK', header = 0)
#############################################################################################
##################Reshape the OPTIMAL DIET table############################################
df_long = df.melt(id_vars=["Food group", "Group", " Baseline"], var_name="CF_DALY", value_name="Value")
df_long[['CF1','CF', 'DALY1', 'DALY']] = df_long['CF_DALY'].str.extract(r'(\w+)\s(\d+%)\s*,\s*(\w+)\s(\d+%)')
df_long.drop(columns=["CF1" , "DALY1"], inplace=True)
df_long.drop(columns=["CF_DALY"], inplace=True)
df_long['CF'] = df_long['CF'].str.rstrip('%').astype(float) / 100
df_long['DALY'] = df_long['DALY'].str.rstrip('%').astype(float) / 100
############## DATA PREPROCESSING FOR FOOD GROUP CHART ##########################################
data_filtered = df_long[(df_long['CF'] ==  cf_in/100 ) & (df_long['DALY']== daly_in/100 )]
data_filtered.drop(columns=["CF", "DALY"], inplace=True)
data_filtered.rename(columns={"Value": "Optimal diet"}, inplace=True)
data_group = data_filtered.groupby(['Group'], sort=True)[[' Baseline','Optimal diet']].sum()
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
    color=alt.Color('Diet Type:N', title='Diet Type',scale=alt.Scale(scheme='set1')),
    yOffset='Diet Type:N'  # Optional: or use x='Variable:N' for grouped bars
).properties(width=600, height=600)
##################################################################################################
########################  Reshape the DALY table ##################################################
##################################################################################################
daly_long = daly.melt(id_vars=["DISEASES", "BASELINE"], var_name="CF_DALY", value_name="Value")
daly_long[['CF1','CF', 'DALY1', 'DALY']] = daly_long['CF_DALY'].str.extract(r'(\w+)\s(\d+%)\s*,\s*(\w+)\s(\d+%)')
daly_long.drop(columns=["CF1" , "DALY1"], inplace=True)
daly_long.drop(columns=["CF_DALY"], inplace=True)
daly_long['CF'] = daly_long['CF'].str.rstrip('%').astype(float) / 100
daly_long['DALY'] = daly_long['DALY'].str.rstrip('%').astype(float) / 100
################### DATA PREPROCESSING FOR DALY CHART ###########################################
daly_filtered = daly_long[(daly_long['CF'] ==  cf_in/100 ) & (daly_long['DALY']== daly_in/100 )]
daly_filtered.drop(columns=["CF", "DALY"], inplace=True)
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
slack_long = slack.melt(id_vars=["Nutrient", "Baseline"], var_name="CF_DALY", value_name="Value")
slack_long[['CF1','CF', 'DALY1', 'DALY']] = slack_long['CF_DALY'].str.extract(r'(\w+)\s(\d+%)\s*,\s*(\w+)\s(\d+%)')
slack_long.drop(columns=["CF1" , "DALY1"], inplace=True)
slack_long.drop(columns=["CF_DALY"], inplace=True)
slack_long['CF'] = slack_long['CF'].str.rstrip('%').astype(float) / 100
slack_long['DALY'] = slack_long['DALY'].str.rstrip('%').astype(float) / 100
############## DATA PREPROCESSING FOR SLACK CHART ##########################################
slack_filtered = slack_long[(slack_long['CF'] ==  cf_in/100 ) & (slack_long['DALY']== daly_in/100 )]
slack_filtered.drop(columns=["CF", "DALY"], inplace=True)
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
# slack_melted = slack_filtered.melt(id_vars='Nutrient', 
#                         value_vars=['Baseline', 'Optimal diet'], 
#                         var_name='Diet Type', 
#                         value_name='Consumption')

chart_slack_g_melted= alt.Chart(slack_g_melted).mark_bar().encode(
    x=alt.X('Nutrient:N', title='Nutrient'),
    y=alt.Y('Consumption:Q', title='Consumption (g/day)'),
    color=alt.Color('Diet Type:N', title='Diet Type',scale=alt.Scale(scheme='set3')),
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
    color=alt.Color('Diet Type:N', title='Diet Type',scale=alt.Scale(scheme='pastel1')),
    xOffset='Diet Type:N'  # Optional: or use x='Variable:N' for grouped bars
).properties(width=600, height=300)
chart_slack_mineral_low_melted= alt.Chart(slack_mineral_low_melted).mark_bar().encode(
    x=alt.X('Nutrient:N', title='Nutrient'),
    y=alt.Y('Consumption:Q', title='Consumption (mg/day)'),
    color=alt.Color('Diet Type:N', title='Diet Type',scale=alt.Scale(scheme='accent')),
    xOffset='Diet Type:N'  # Optional: or use x='Variable:N' for grouped bars
).properties(width=600, height=300)


###########################################################################################################
#################### STYLING THE TABLE FOR BETTER VISUAL EFFECTS ##########################################
###########################################################################################################
styled_data_group = data_group.style.format({
    'Baseline': "{:.1f}",
    'Optimal_diet': "{:.1f}"
}).highlight_max(subset=['Baseline', 'Optimal diet'], axis=1, color='lightgreen')








col1.subheader('Food group composition in your optimal Diet')
col1.altair_chart(chart_foodgroup, use_container_width=True)
col1.subheader("Optimal Diet Suggestions for each food group(g/day)")
col1.table(styled_data_group)
st.subheader('Burden of your optimal Diet (DALY/100k) ')
st.altair_chart(chart_daly, use_container_width=True)
st.subheader('Nutritional Composition of your optimal Diet ')
st.altair_chart(chart_slack_g_melted, use_container_width=True)
st.altair_chart(chart_slack_mg_melted, use_container_width=True)
st.altair_chart(chart_slack_mineral_high_melted, use_container_width=True)
st.altair_chart(chart_slack_mineral_low_melted, use_container_width=True)
st.subheader("Optimal Diet Suggestions for all food items(g/day)")
st.table(data_filtered)








