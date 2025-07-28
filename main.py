# -*- coding: utf-8 -*-
"""
Created on Wed Jun 25 11:31:51 2025

@author: says
"""

import streamlit as st
from diet_optimisation_app_version2 import model_quad_2
from diet_optimisation_app_version3 import model_linear
from diet_optimisation_app_version4 import model_quad_substitute


st.set_page_config(layout="wide")
col1, col2 = st.columns([4, 2])
col1.header('National Food Institute')
col1.write('**Research** **Group** **for** **Risk-Benefit**')
st.sidebar.image('DTU.png', width=50)

st.sidebar.header("Choose Country")
model_choice = st.sidebar.selectbox(" ", ("DENMARK", "NETHERLANDS"),)
st.sidebar.write("You selected:", model_choice)
if model_choice == "DENMARK":
    st.sidebar.header("Choose Diet Optimization Model")
    model_choice = st.sidebar.radio("Select a model:", ["***QUADRATIC***", "***LINEAR***", "***SUBSTITUTION***"],
                                    captions=[
            "A diet close to current habits.",
            "A diet which gives the best health benefit.",
            "A diet close to current habits and which allows for eliminating meat and dairy products.",],)

    if model_choice == "***QUADRATIC***":
        model_quad_2()
    elif model_choice == "***LINEAR***":
        model_linear()
    elif model_choice == "***SUBSTITUTION***":
        model_quad_substitute()
elif model_choice == "NETHERLANDS":
    st.sidebar.header("Choose Diet Optimization Model")
    model_choice = st.sidebar.radio("Select a model:", ["***QUADRATIC***", "***LINEAR***", "***SUBSTITUTION***"],
                                    captions=[
            "A diet close to current habits.",
            "A diet which gives the best health benefit.",
            "A diet close to current habits and which allows for eliminating meat and dairy products.",],)

    if model_choice == "***QUADRATIC***":
        model_quad_2()
    elif model_choice == "***LINEAR***":
        model_linear()
    elif model_choice == "***SUBSTITUTION***":
        model_quad_substitute()

