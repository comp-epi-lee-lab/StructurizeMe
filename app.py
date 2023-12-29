import streamlit as st
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import io 

st.title('NoramlizeMe HGS-OvCa in HM450k')

cols = 'GenecodeV41_Group'
df = ('HM450k_EpicGeneSum.tsv.gz')

@st.cache_data
def load_data(nrows):
    data = pd.read_csv(df, nrows=nrows, sep='\t', compression='gzip')
    lowercase = lambda x: str(x).lower()
    data.rename(axis='columns', inplace=True)
    return data

data_load_state = st.text('Loading data...')
data = load_data(22847)
data_load_state.text('Data loaded successfully!')

st.write(data)
