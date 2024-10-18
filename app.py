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

# Function to plot heatmaps
def plot_heatmap(data, title, yticklabels=None):
    fig, ax = plt.subplots(figsize=(15, 5))

    if not data.empty:
        if yticklabels is None:
            if isinstance(data.index, pd.MultiIndex):
                yticklabels = data.index.get_level_values('Gene')
            else:
                yticklabels = data.index

        sns.heatmap(data, cmap="vlag", annot=False, linewidths=.5,
                    yticklabels=yticklabels, linecolor='grey', annot_kws={"size": 12},
                    cbar_kws={'ticks': [0.0, 0.5, 1.0]}, vmin=0, vmax=1)
        plt.title(title, fontfamily='sans-serif')
        plt.xlabel("Gene Structure", fontfamily='sans-serif')
        plt.ylabel("Gene Name", fontfamily='sans-serif')
        plt.tick_params(left=False, bottom=False)
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

        # Iterate through selected cancers and plot heatmaps
        for cancer in selected_cancers:
            # Data for Cancer
            selected_cancer_data = data_dict[cancer]['cancer'][
                data_dict[cancer]['cancer']['Gene'].isin(selected_genes) |
                data_dict[cancer]['cancer'].get('alias_symbol', pd.Series([])).isin(selected_genes)
            ]

            if not selected_cancer_data.empty:
                selected_cancer_data.set_index(['Gene', 'alias_symbol'], inplace=True)
                plot_heatmap(selected_cancer_data, f"{cancer} Cancer")
            else:
                st.write(f"No data available for {cancer} Cancer.")

            # Data for Normal
            selected_normal_data = data_dict[cancer]['normal'][
                data_dict[cancer]['normal']['Gene'].isin(selected_genes) |
                data_dict[cancer]['normal'].get('alias_symbol', pd.Series([])).isin(selected_genes)
            ]

            if not selected_normal_data.empty:
                selected_normal_data.set_index(['Gene', 'alias_symbol'], inplace=True)
                plot_heatmap(selected_normal_data, f"{cancer} Normal")
            else:
                st.write(f"No data available for {cancer} Normal.")

            # Data for Differences
            if 'diff' in data_dict[cancer]:
                selected_diff_data = data_dict[cancer]['diff'][
                    data_dict[cancer]['diff']['Gene'].isin(selected_genes) |
                    data_dict[cancer]['diff'].get('alias_symbol', pd.Series([])).isin(selected_genes)
                ]

                if not selected_diff_data.empty:
                    selected_diff_data.set_index(['Gene', 'alias_symbol'], inplace=True)
                    plot_heatmap(selected_diff_data, f"{cancer} Differences")

                    # Get the common columns between selected_cancer_data and selected_diff_data
                    common_columns = selected_cancer_data.columns.intersection(selected_diff_data.columns)

                    # Create values_data by filtering columns in selected_diff_data that exist in selected_cancer_data
                    values_data = selected_cancer_data.loc[:, common_columns]

                    # Check if values_data has non-null values
                    values_data = values_data[values_data.notna().any(axis=1)]  # Keep only rows with non-null values

                    if not values_data.empty:
                        plot_heatmap(values_data, f"{cancer} Selected Genes with Values from Differences")
                    else:
                        st.write("No data available in values_data for the selected differences.")
                else:
                    st.write(f"No difference data available for {cancer}.")
