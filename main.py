import streamlit as st
import pandas as pd
import numpy as np
import math
#Title
st.title("Viscosity Index Calulator")
st.subheader("By José Isaac Hernández Gámez")
#Dataframe
source = pd.read_csv("data_source/VI_L_H_Values.csv")
#Interpolation
def interpolate(x,xp,fp):
    result = np.interp(x, xp, fp)
    return result
#ValidateInputs
def valid_float_input(textInput):
    try:
        user_input = float(textInput)
        return user_input
    except:
        return
#Conditions
def getValuesHL(valueV40,valueV100):
    try:
        if valueV100 > 70:
            L = (0.8353*valueV100*valueV100) + (14.67*valueV100) - 216
            H = (0.1684*valueV100*valueV100) + (11.85*valueV100) - 97
        elif valueV100 <= 70:
            L = interpolate(valueV100,source["VI"].values,source["L"].values)
            H = interpolate(valueV100,source["VI"].values,source["H"].values)
        results = [L,H]
        return results
    except:
        return
#Final Result
def viscosityIndex(valueV40,valueV100,L,H):
    try: 
        if valueV40 > H:
            vi = ((L-valueV40)/(L-H))*100
        elif valueV40 < H:
            N = (math.log10(H) - math.log10(valueV40))/math.log10(valueV100)
            vi = ((pow(10,N)-1)/0.00715)+100
        elif valueV40 == H:
            vi = 100
        return vi
    except:
        return
#Main
V40 = st.text_input("V 40°C (mm2/s)")
V100 = st.text_input("V 100°C (mm2/s)")
#Button
if st.button("Calulate", type="primary"):
    valFloat40 = valid_float_input(V40)
    valFloat100 = valid_float_input(V100)
    if valFloat40 < 3 or valFloat100 < 2: 
        valFloat100 = None
        valFloat100 = None
        st.error('Invalid input, try again', icon="🚨")
    else:
        resultsLH = getValuesHL(valFloat40,valFloat100)
        resultsViscosity = viscosityIndex(valFloat40,valFloat100,resultsLH[0],resultsLH[1])
        st.success(resultsViscosity)