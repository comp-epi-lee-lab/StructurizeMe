import streamlit as st
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

st.title('NoramlizeMe HGS-OvCa in HM450k')

df = st.file_uploader("HM450k_EpicGeneSum.tsv.gz")

if df is not None:
    dataframe = pd.read_csv(df)
    st.write(dataframe)