#env python3.8
#coding: utf-8
"""
@author: Wei-Zhi Lin
version: 1.001
"""
#%% import statement 
import pandas as pd
import sys
#%% input compound data 
print('path of compound input list =')
input_path = input() 
    #type in the path of input
    #example-input could be downloaded from here: https://github.com/LinWZ-tw/g2d-prism/blob/main/example-input-compounds-for-py.csv
input_compounds = pd.read_csv(input_path)
print('\n', 'selected compounds = \n', input_compounds, '\n\n\n')
#%% input primary tissue
print('select primary tissue from the following list: esophagus , uterus , pancreas , colorectal , liver , central_nervous_system , urinary_tract , lung , rhabdoid , ovary , bone , mesothelioma , skin , kidney , soft_tissue , thyroid , upper_aerodigestive , peripheral_nervous_system , gastric , bile_duct , breast prostate , fibroblast , rhabdomyosarcoma. \n\
copy and paste below:')
list_primary_tissue = ['esophagus', 'uterus', 'pancreas', 'colorectal, liver', 'central_nervous_system', 'urinary_tract', 'lung, rhabdoid', 'ovary', 'bone', 'mesothelioma', 'skin', 'kidney', 'soft_tissue', 'thyroid', 'upper_aerodigestive', 'peripheral_nervous_system', 'gastric', 'bile_duct', 'breast', 'prostate', 'fibroblast', 'rhabdomyosarcoma']
input_pt = input() #input 
if input_pt in list_primary_tissue:
    print ('input in list, checked!')
else:
    print ('"', input_pt, '"', 'NOT in list, please check again.')
    sys.exit() #if input not in list, exit.
print('--------------------------------------------------------------------')
#%% import data from depmap
print('Start to download data from PRSIM 19Q4. \n \
(It will take few minutes)')
#get cell line information
print('loading cell line information')
cell_line_info = pd.read_csv('https://ndownloader.figshare.com/files/20237718')
#get compounds/treatments information
print('loading treatments/compounds information')
treatment_info = pd.read_csv('https://ndownloader.figshare.com/files/20237715')
#get sensitivity data
print('loading sensitivity data')
prism_data = pd.read_csv('https://ndownloader.figshare.com/files/20237709' )
print('--------------------------------------------------------------------')
#%% filter cell line by selected primary tissue
f_cell_line_info = cell_line_info[cell_line_info['primary_tissue'] == input_pt]
f_cell_line_info = f_cell_line_info[['depmap_id','ccle_name','primary_tissue', 'secondary_tissue', 'tertiary_tissue']]
print('number of selected cell lines =', len(f_cell_line_info))
#filter compounds/treatments by input list
f_treatment_info = pd.merge(input_compounds, treatment_info, on='name')
f_treatment_info = f_treatment_info[['column_name', 'name']]
print("number of treatments = ", len(f_treatment_info)-1) 
print('--------------------------------------------------------------------')
#%% align selected cell line to prism data
f_prism_data = pd.merge(f_cell_line_info, prism_data, how = 'inner', left_on = 'depmap_id', right_on = 'Unnamed: 0', sort = bool)
select_info = ['depmap_id', 'ccle_name','primary_tissue'] # select needed info. column
headlist = select_info+list(f_treatment_info['column_name'])
f_prism_data = f_prism_data[headlist]
#%% align treatment info to prism data
f_prism_data = f_prism_data.transpose()
f_prism_data.reset_index(level=0, inplace=True)
f_prism_data = pd.merge(f_treatment_info, f_prism_data, how = 'outer', left_on = 'column_name', right_on = 'index', sort = bool)
f_prism_data = f_prism_data.transpose()
#%% export results
print('output result to "result.xlsx"')
f_prism_data.to_excel('result.xlsx')
