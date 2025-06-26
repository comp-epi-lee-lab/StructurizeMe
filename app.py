import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Function to load data for each cancer type
def load_data():
    return {
        'BRCA': {
            'cancer': pd.read_csv('data/BRCA-Cancer.tsv.gz', sep='\t', compression='gzip'),
            'normal': pd.read_csv('data/BRCA-Normal.tsv.gz', sep='\t', compression='gzip')
        },
        'COAD': {
            'cancer': pd.read_csv('data/COAD-Cancer.tsv.gz', sep='\t', compression='gzip'),
            'normal': pd.read_csv('data/COAD-Normal.tsv.gz', sep='\t', compression='gzip')
        },
        'OV': {
            'cancer': pd.read_csv('data/HM450k_EpicGeneSum1.tsv.gz', sep='\t', compression='gzip'),
            'normal': pd.read_csv('data/EPIC850k_EpicGeneSum1.tsv.gz', sep='\t', compression='gzip'),
            'diff': pd.read_csv('data/Differences_HM450EPICv1.gz', sep='\t', compression='gzip')
        }
    }

data = load_data()
