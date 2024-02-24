import streamlit as st
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import io 

st.title('NoramlizeMe HGS-OvCa in HM450k')import streamlit as st
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.title('NoramlizeMe HGS-OvCa in HM450k and EPICv1')

input = st.text_input("Enter gene names separated by commas..", "")
selected_gene_names = [gene.strip() for gene in input.split(',') if gene.strip()]
st.button("VisualizeMe", type="primary")


def load_data_hm450k(nrows):
    data = pd.read_csv('HM450k_EpicGeneSum1.tsv.gz', nrows=nrows, sep='\t', compression='gzip')
    return data

data = load_data_hm450k(22847)

def load_data_epic850k(nrows):
    df = pd.read_csv('EPIC850k_EpicGeneSum1.tsv.gz', nrows=nrows, sep='\t', compression='gzip')
    return df

df = load_data_epic850k(23747)

#def load_data_diff(nrows):
    #diff = pd.read_csv('Differences_HM450EPICv1.gz', nrows=nrows, sep='\t', compression='gzip')
    #return df

#diff = load_data_diff(24875)
    
df_cols = df.columns 
data_cols = data.columns
#diff_cols = diff.columns

indexes = ['Gene','alias_symbol']
gene_names = pd.concat([data['Gene'], df['Gene']], ignore_index=True)

if selected_gene_names:
    selected_data_hm450k = data[data['Gene'].isin(selected_gene_names)]
    selected_data_epic850k = df[df['Gene'].isin(selected_gene_names)]

    st.write(f'Data for Selected Gene Names: {", ".join(selected_gene_names)}')

    fig1, ax1 = plt.subplots(figsize=(15, 5))

    if not selected_data_hm450k.empty:
        
        work_hm450k = selected_data_hm450k.set_index('Gene')
        plt.title("HM450K", fontfamily='sans-serif')
        ax1 = sns.heatmap(work_hm450k, cmap="vlag", annot=False, linewidths=.5,
                          yticklabels=True, linecolor='grey', annot_kws={"size": 12},
                          cbar_kws={'ticks': [0.0, 0.5, 1.0]}, vmin=0, vmax=1)
        plt.tick_params(left=False, bottom=False)
        plt.xlabel("Gene Structure", fontfamily='sans-serif')
        ax1.spines['bottom'].set_visible(True)
        ax1.spines['right'].set_visible(True)
        ax1.spines['bottom'].set_linewidth(.5)
        ax1.spines['right'].set_linewidth(.5)
        spine_color = 'grey'
        ax1.spines['bottom'].set_color(spine_color)
        ax1.spines['right'].set_color(spine_color)
        ax1.patch.set_edgecolor('lightgrey')
        ax1.patch.set_hatch('///')
    else:
        st.write("No data available for selected genes in HM450k.")

    fig2, ax2 = plt.subplots(figsize=(15, 5))

    if not selected_data_epic850k.empty:
        
        work_epic850k = selected_data_epic850k.set_index('Gene')
        ax2 = sns.heatmap(work_epic850k, cmap="vlag", annot=False, linewidths=.5,
                          yticklabels=True, linecolor='grey', annot_kws={"size": 12},
                          cbar_kws={'ticks': [0.0, 0.5, 1.0]}, vmin=0, vmax=1)
        plt.title("EPIC850K", fontfamily='sans-serif')
        plt.xlabel("Gene Structure", fontfamily='sans-serif')
        plt.tick_params(left=False, bottom=False)
        ax2.spines['bottom'].set_visible(True)
        ax2.spines['right'].set_visible(True)
        ax2.spines['bottom'].set_linewidth(.5)
        ax2.spines['right'].set_linewidth(.5)
        spine_color = 'grey'
        ax2.spines['bottom'].set_color(spine_color)
        ax2.spines['right'].set_color(spine_color)
        ax2.patch.set_edgecolor('lightgrey')
        ax2.patch.set_hatch('///')
    else:
        st.write("No data available for selected genes in EPIC850k.")

    col1, col2 = st.columns(2)

    with col1:
        st.write("Selected Genes in HM450k:")
        st.pyplot(fig1)
        st.write(selected_data_hm450k.set_index('Gene'))

    with col2:
        st.write("Selected Genes in EPIC850k:")
        st.pyplot(fig2)
        st.write(selected_data_epic850k.set_index('Gene'))

else:
    st.write("Please enter gene names.")
