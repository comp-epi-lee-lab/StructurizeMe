import streamlit as st
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import io 

st.title('NoramlizeMe HGS-OvCa in HM450k')

cols = 'BLANK'
df = ('HM450k_EpicGeneSum.tsv.gz')

def load_data(nrows):
    data = pd.read_csv(df, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[cols] = pd.to_datetime(data[cols])
    return data