import streamlit as st
import pandas as pd 
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


streamlit app.py
st.title('NoramlizeMe HGS-OvCa in HM450k')

df = pd.read_csv('gdac.broadinstitute.org_OV.Merge_methylation__humanmethylation450__jhu_usc_edu__Level_3__within_bioassay_data_set_function__data.Level_3.2016012800.0.0.tar.gz', sep = '\t', compression='gzip', low_memory=False)
df

df.rename(columns = {'././@LongLink':'OV_HM450'}, inplace = True)
df.set_index(['OV_HM450'], inplace=True)
df

df = df.loc[:, ~df.iloc[0].isin(['Gene_Symbol', 'Chromosome','Genomic_Coordinate'])]
df1 = df.drop(['Composite Element REF']) 
df1

new_columns = [item[:16] for item in df1.columns]
df1.columns = new_columns
df1

df1 = df1.astype('float')
df1['mean_Meth_Ratio'] = df1.mean(axis=1)
df1 = df1.sort_index()
df1

an = pd.read_csv('EPIC-8v2-0_A1.sim.sel.tsv.gz', sep = '\t', low_memory=False)
an.set_index(['EPICv2'], inplace=True)
an = an.sort_index()
an

df2 = df1.merge(an, left_index=True, right_index=True, how='inner')
df2

df2 = df2.sort_values(by=['CHR', 'Pos']) 
df2

df2 = df2.iloc[:,10:]
df2

gene_list = list(set(df2['mode_Gene_Name']))
gene_list

df_out = pd.DataFrame()
i = 0

for gene in gene_list: 
    df_gene = df2.drop(['CHR','Pos','mode_Gene_Name'],axis=1)[df2['mode_Gene_Name'] == gene]
    i = i + 1 
    print(i, gene)
    df_group = df_gene.groupby('mode_GenecodeV41_Group').mean()
    df_group["Gene"] = [gene] * df_group.shape[0]
    df_out = pd.concat([df_out, df_group])

df_out.reset_index(inplace=True)
df_out = df_out.pivot(index='Gene', columns='mode_GenecodeV41_Group', values='mean_Meth_Ratio')
df_out 

df_out = df_out.loc[:,['TSS1500','TSS200','5UTR','exon_1','exon_2','exon_3','exon_4','exon_5','exon_6','exon_7','exon_8','exon_9','exon_10', 'exon_11','exon_12','exon_13','exon_14','exon_15','exon_16','exon_17', 'exon_18','exon_19','exon_20','exon_21','exon_22','exon_23','exon_24','exon_25','exon_26','exon_27','exon_28','exon_29','exon_30','exon_31','exon_32','exon_33','exon_34','exon_35','exon_36','exon_37','exon_38','exon_39','exon_40','exon_41','exon_42','exon_43','exon_44','exon_45','exon_46','exon_47','exon_48','exon_49','exon_50','exon_51','exon_52','exon_53','exon_54','exon_55','exon_56','exon_57','exon_58','exon_59','exon_60','exon_61','exon_62','exon_63','exon_65','exon_66','exon_67','exon_68','exon_69','exon_70','exon_71','exon_72','exon_73','exon_74','exon_75','exon_76','exon_77','exon_78','exon_79','exon_80','exon_84','exon_85','exon_87','exon_88','exon_89','exon_90','exon_91','exon_92','exon_93','exon_97','exon_98','exon_101','exon_102','exon_103','exon_105','exon_106','exon_107','exon_111','exon_115','exon_116','exon_134','exon_154','exon_186','3UTR']]
df_out

