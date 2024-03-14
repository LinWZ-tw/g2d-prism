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
print('select primary tissue from the following list:','\n', 
      '1: esophagus ','\n', 
      '2: uterus','\n',
      '3: pancreas','\n',
      '4: colorectal','\n',
      '5: liver','\n',
      '6: central_nervous_system','\n',
      '7: urinary_tract','\n',
      '8: lung','\n',
      '9: rhabdoid','\n',
      '10: ovary','\n',
      '11: bone','\n',
      '12: mesothelioma','\n',
      '13: skin','\n',
      '14: kidney','\n',
      '15: soft_tissue','\n',
      '16: thyroid','\n',
      '17: upper_aerodigestive','\n',
      '18: peripheral_nervous_system','\n',
      '19: gastric','\n',
      '20: bile_duct','\n',
      '21: breast','\n',
      '22: prostate','\n',
      '23: fibroblast','\n',
      '24: rhabdomyosarcoma','\n','')
list_primary_tissue ={
    1: 'esophagus',
    2: 'uterus',
    3: 'pancreas',
    4: 'colorectal',
    5: 'liver',
    6: 'central_nervous_system',
    7: 'urinary_tract',
    8: 'lung',
    9: 'rhabdoid',
    10: 'ovary',
    11: 'bone',
    12: 'mesothelioma',
    13: 'skin',
    14: 'kidney',
    15: 'soft_tissue',
    16: 'thyroid',
    17: 'upper_aerodigestive',
    18: 'peripheral_nervous_system',
    19: 'gastric',
    20: 'bile_duct',
    21: 'breast',
    22: 'prostate',
    23: 'fibroblast',
    24: 'rhabdomyosarcoma'}
def check_input(number):
    while number not in list_primary_tissue:
        print ('entered number out of range, there are only 24 primary tissues')
        number = int(input('try again: '))
        print ()
    return list_primary_tissue[number]
number = int(input("select primary tissue (please enter the number ONLY): "))
print (check_input(number))
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
