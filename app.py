import streamlit as st
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def load_data():
    return {
        'BRCA': {
            'cancer': pd.read_csv('data/BRCA Files/BRCA-Cancer.tsv.gz', sep='\t', compression='gzip'),
            'normal': pd.read_csv('data/BRCA Files/BRCA-Normal.tsv.gz', sep='\t', compression='gzip')
            #'diff': pd.read_csv('data/BRCA-Differences.tsv.gz', sep='\t', compression='gzip')
        },
        'COAD': {
            'cancer': pd.read_csv('data/COAD Files/COAD-Cancer.tsv.gz', sep='\t', compression='gzip'),
            'normal': pd.read_csv('data/COAD Files/COAD-Normal.tsv.gz', sep='\t', compression='gzip')
            #'diff': pd.read_csv('data/COAD-Differences.tsv.gz', sep='\t', compression='gzip')
        },
        'OV': {
            'cancer': pd.read_csv('data/OV Files/HM450k_EpicGeneSum1.tsv.gz', sep='\t', compression='gzip'),
            'normal': pd.read_csv('data/OV Files/EPIC850k_EpicGeneSum1.tsv.gz', sep='\t', compression='gzip'),
            'diff': pd.read_csv('data/Differences_HM450EPICv1.gz', sep='\t', compression='gzip')
        }
    }
    
data = load_data()
