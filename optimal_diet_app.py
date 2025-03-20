# -*- coding: utf-8 -*-
"""
Created on Wed Mar 19 14:16:33 2025

@author: says
"""

#import streamlit as st
import pandas as pd
import numpy as np
import streamlit as st
#import os
import matplotlib.pyplot as plt


######################### INITIAL DATA MANIPULATION FOR APP READY DATASET########################


# df = pd.read_excel("C:\\Users\\says\\Projects\\DROSH\\app\\data.xlsx")  # Assuming it's stored in CSV format
# # Reshape the table
# df_long = df.melt(id_vars=["Food group", "Group", " Baseline"], var_name="CF_DALY", value_name="Value")
# # Split the CF and DALY information into separate columns
# df_long[['CF1','CF', 'DALY1', 'DALY']] = df_long['CF_DALY'].str.extract(r'(\w+)\s(\d+%)\s*,\s*(\w+)\s(\d+%)')
# df_long.drop(columns=["CF1" , "DALY1"], inplace=True)
# # Drop unnecessary column
# df_long.drop(columns=["CF_DALY"], inplace=True)
# # Convert percentages to numeric (if needed)
# df_long['CF'] = df_long['CF'].str.rstrip('%').astype(float) / 100
# df_long['DALY'] = df_long['DALY'].str.rstrip('%').astype(float) / 100
# df_long.to_excel("app_data.xlsx")
# df_long.to_csv("app_data.csv")


##################################################################################################




multi = '''
Eat smart, live long, and save the planet—one bite at a time! The perfect diet isn’t just about fueling your body; it’s about nourishing the world around you. Imagine a plate packed with vibrant veggies, hearty grains, and planet-friendly proteins—good for your health, great for the Earth, and designed to keep diet-related diseases at bay. With the right balance, you can lower your carbon footprint, maximize nutrition, and add healthy years to your life. Ready to eat for a better you and a better world? Let’s dig in!
'''
col1, col2 = st.columns([3, 1])
col1.subheader('National Food Institute')
col1.write('**Research** **Group** **for** **Risk-Benefit**')
col1.title('How does your optimal diet looks like ?')
col2.image('DTU.png', width=50)

col2.subheader('What is an optimal diet ? ')
col2.image('DALYs.webp')
col2.markdown(multi)
#col2.image('DALY1.webp')
#Create and name sidebar
#st.image('DALY1.webp')
st.sidebar.image('DALY1.webp')
st.sidebar.header('Choose your category')
cf_in = st.sidebar.slider('Reduce Carbon footprint by (%)', min_value=0, max_value=50, step = 25)
#st.sidebar.write(f'Selected reduction in Carbon footprint: {cf_in} %')
daly_in = st.sidebar.slider('Reduce DALYs by (%)', min_value=0, max_value=50, step = 25)
#st.sidebar.write(f'Selected reduction in DALY: {daly_in} %')



#sex1 = st.sidebar.selectbox('Sex',('Male', 'Female'))
# meat_con = st.sidebar.number_input('What is your Daily average Meat consumption ? *(gm/day)*',step=1,value=40)
# pulse_con = st.sidebar.number_input('What is your Daily average Pulse consumption ? *(gm/day)*',step=1,value=10)

#os.chdir('C:\\Users\\says\\Projects\\DROSH\\app')
data = pd.read_csv("./app_data.csv")

data_filtered = data[(data['CF'] ==  cf_in/100 ) & (data['DALY']== daly_in/100 )]
data_filtered.drop(columns=["CF", "DALY", 'Unnamed: 0'], inplace=True)
data_filtered.rename(columns={"Value": "Optimal_diet"}, inplace=True)

data_group = data_filtered.groupby(['Group'], sort=True)[' Baseline','Optimal_diet'].sum()
data_group['Food Group'] = ['WHOLE GRAIN', 'DAIRY', 'FISH', 'FRUIT', 'VEGETABLE', 'MEAT', 'NUTS', 'LEGUMES']

st.write("Optimal Diet Suggestions based on your inputs:")
st.dataframe(data_filtered)

st.write("Optimal Diet Suggestions for each food group:")
st.dataframe(data_group)

#data[(data['CF'] == 0.0 ) & (data['DALY']== 0.0 )].reset_index()

#X = {'Colorectal Cancer': [0, consumption_meat_subset.groupby(['sex'], sort=True)['delta_daly_crc'].mean().values[0]*-1, 0], 'Ischemic Heart Disease': [consumption_pulses_subset.groupby(['sex'], sort=True)['delta_daly_ihd'].mean().values[0]*-1, 0,0 ],   'Type-2 Diabetes': [0, 0, consumption_meat_subset.groupby(['sex'], sort=True)['delta_daly_t2d'].mean().values[0]*-1 ]}

chart_data = pd.DataFrame(data_filtered)

#chart_data = chart_data.transpose()
col1.subheader('Food group composition in your optimal diet *(gm/day)*')
# col1.bar_chart(chart_data)

# fig, ax = plt.subplots(figsize=(10, 6))
# fig.patch.set_facecolor('black')  # Change figure background
# ax.set_facecolor('black')  # Change plot background
# # Plot stacked bars: each food group will have two bars (Value 1 and Value 2 stacked)
# ax.bar(data_group['Food Group'], data_group[' Baseline'], label='Baseline diet', color='cyan')
# ax.bar(data_group['Food Group'], data_group['Optimal_diet'], bottom=data_group[' Baseline'], label='Optimal diet', color='red')
# # Adding labels and title
# ax.set_xlabel('Food Group')
# ax.set_ylabel('Consumption (gm/day)')
# ax.set_title('Optimal Diet Composition of Food Groups')
# ax.legend()
# # Change text and tick colors to white for better visibility
# ax.spines['bottom'].set_color('white')
# ax.spines['left'].set_color('white')
# ax.xaxis.label.set_color('white')
# ax.yaxis.label.set_color('white')
# ax.tick_params(axis='x', colors='white')
# ax.tick_params(axis='y', colors='white')

# Sample data (replace with your actual data)
food_groups = data_group['Food Group']
baseline_values = data_group[' Baseline']
optimal_values = data_group['Optimal_diet']

# Define bar width and positions
x = np.arange(len(food_groups))  # Numeric positions for each food group
width = 0.4  # Width of the bars

fig, ax = plt.subplots(figsize=(10, 6))
fig.patch.set_facecolor('black')  # Change figure background
ax.set_facecolor('black')  # Change plot background

# Plot side-by-side bars
ax.bar(x - width/2, baseline_values, width, label='Baseline diet', color='cyan')
ax.bar(x + width/2, optimal_values, width, label='Optimal diet', color='red')

# Formatting the plot
ax.set_xlabel('Food Group')
ax.set_ylabel('Consumption (gm/day)')
ax.set_title('Optimal Diet Composition of Food Groups')
ax.legend()

# Adjust x-axis labels
ax.set_xticks(x)
ax.set_xticklabels(food_groups, rotation=45, ha='right', color='white')

# Change text and tick colors to white for better visibility
ax.spines['bottom'].set_color('white')
ax.spines['left'].set_color('white')
ax.xaxis.label.set_color('white')
ax.yaxis.label.set_color('white')
ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')







# Display the plot in Streamlit
col1.pyplot(fig)

#st.write('You consume',np.round(pulse_con/consumption_pulses_subset.total.mean() , 2) ,'times pulses of the average consumption in the age group of', age-2 ,'to', age+2 )
#st.write('You consume',np.round(meat_con/consumption_meat_subset.total.mean(),2 ) ,'times meat of the average consumption in the age group of', age-2 ,'to', age+2 )




