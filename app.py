import streamlit as st
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Function to load data for each cancer type
def load_data():
    return {
        'BRCA': {
            'cancer': pd.read_csv('data/BRCA-Cancer.tsv.gz', sep='\t', compression='gzip'),
            'normal': pd.read_csv('data/BRCA-Normal.tsv.gz', sep='\t', compression='gzip'),
            'diff': pd.read_csv('data/BRCA-Differences.tsv.gz', sep='\t', compression='gzip')
        },
        'COAD': {
            'cancer': pd.read_csv('data/COAD-Cancer.tsv.gz', sep='\t', compression='gzip'),
            'normal': pd.read_csv('data/COAD-Normal.tsv.gz', sep='\t', compression='gzip'),
            'diff': pd.read_csv('data/COAD-Differences.tsv.gz', sep='\t', compression='gzip')
        },
        'OV': {
            'cancer': pd.read_csv('data/HM450k_EpicGeneSum1.tsv.gz', sep='\t', compression='gzip'),
            'normal': pd.read_csv('data/EPIC850k_EpicGeneSum1.tsv.gz', sep='\t', compression='gzip'),
            'diff': pd.read_csv('data/Differences_HM450EPICv1.gz', sep='\t', compression='gzip')
        }
    }

# Function to plot heatmaps
def plot_heatmap(data, title):
    fig, ax = plt.subplots(figsize=(15, 5))
    if not data.empty:
        sns.heatmap(data, cmap="vlag", annot=False, linewidths=.5,
                          yticklabels=data.index.get_level_values('Gene'), linecolor='grey', annot_kws={"size":
                          12}, cbar_kws={'ticks': [0.0, 0.5, 1.0]}, vmin=0, vmax=1))
        plt.title(title, fontfamily='sans-serif')
        plt.xlabel("Gene Structure", fontfamily='sans-serif')
        plt.ylabel("Gene Name", fontfamily='sans-serif')
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
        st.write("Selected Genes in EPIC850k:")
        st.pyplot(fig)
    else:
        st.write("No data available for this selection.")

# Main app logic
st.title('StructurizeMe: Cancer and Normal Samples in HM450k and EPICv1')

# Load all data once at the beginning
data_dict = load_data()

# Select cancer types
cancer_options = list(data_dict.keys())
selected_cancers = st.multiselect('Select cancer types:', cancer_options)

# Get unique gene names based on selected cancers
if selected_cancers:
    all_gene_names = pd.concat([data_dict[cancer]['cancer']['Gene'] for cancer in selected_cancers]).unique()
    selected_genes = st.multiselect('Select gene names:', all_gene_names)

    if selected_genes:
        st.write(f'Selected Cancer Types: {", ".join(selected_cancers)}')
        st.write(f'Selected Gene Names: {", ".join(selected_genes)}')

        # Plot heatmaps for each selected cancer type
        for cancer in selected_cancers:
            # Filter for selected gene names
            selected_cancer_data = data_dict[cancer]['cancer'][data_dict[cancer]['cancer']['Gene'].isin(selected_genes) |
                                                                data_dict[cancer]['cancer']['alias_symbol'].isin(selected_genes)]
            selected_normal_data = data_dict[cancer]['normal'][data_dict[cancer]['normal']['Gene'].isin(selected_genes) |
                                                                data_dict[cancer]['normal']['alias_symbol'].isin(selected_genes)]
            selected_diff_data = data_dict[cancer]['diff'][data_dict[cancer]['diff']['Gene'].isin(selected_genes) |
                                                            data_dict[cancer]['diff']['alias_symbol'].isin(selected_genes)]

            # Set index for each dataset
            selected_cancer_data.set_index(['Gene', 'alias_symbol'], inplace=True)
            selected_normal_data.set_index(['Gene', 'alias_symbol'], inplace=True)
            selected_diff_data.set_index(['Gene', 'alias_symbol'], inplace=True)

            # Plotting heatmaps for each dataset separately
            plot_heatmap(selected_cancer_data, f"{cancer} Cancer")
            plot_heatmap(selected_normal_data, f"{cancer} Normal")
            plot_heatmap(selected_diff_data, f"{cancer} Difference")
    else:
        st.write("Please select gene names.")
else:
    st.write("Please select cancer types.")

