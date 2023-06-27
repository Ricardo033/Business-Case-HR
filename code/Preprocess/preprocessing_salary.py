#====================#
# Required packages  #
#====================#

import pandas as pd
import numpy as np

class salary_preprocessing(object):

    def data_types(salary_data):
        
        ''' 
        This function converts variables into date and time, and float data types.
        
        Input
        salary_data: Raw dataset with salary registers.
        
        Output
        salary_data: Salary_data with modified data types for some columns. 
        '''
    
        # Floats
        float_variables=['Gross Salary','Net Salary','Gross Salary 108']
        for i in float_variables:
                salary_data[i]=pd.Series(salary_data[i].copy(),dtype="string").apply(lambda x: x.replace(',','.'))
                salary_data[i]=salary_data[i].copy().astype(float)

        # Time data
        salary_data['Period']=pd.Series(salary_data['Period'].copy(),dtype="string")
        salary_data['Period']=pd.to_datetime( salary_data['Period'].copy(),dayfirst=True)
        

        return salary_data 
    
    
    
    def fdcp_duplicates_cleaning(salary_data):
        
        '''
        This function removes the extra zeros from the column FDCP, and deletes duplicates from salary data. 
        
        Input
        salary_data: Raw dataset with salary registers.
        
        Output
        salary_data: Salary_data with modified columns.
        '''
        
        # Deleting Extra Zeros from FDCP COlumn
        salary_data[['A','B','C','D']]=(
                                         salary_data['FDCP'].copy().str.split('|', 4, expand=True)
                                        ).astype(int).astype("string")
        salary_data['FDCP']=(
                              salary_data['A']+'|'+salary_data['B']+'|'+salary_data['C']+'|'+salary_data['D']
                             ).astype(object)
        
        # Droping not necessary variables and duplicates
        duplicates = salary_data.duplicated().sum()
        
        print(f'{duplicates} duplicates were deleted')
        salary_data=salary_data.drop(['A','B','C','D'], axis=1).drop_duplicates()

        return salary_data
    
    def time_filter(salary_data):
        
        '''
        This function filters data based on the last 24 months. Using "Start Contract Date" as reference point.
        
        Input
        salary_data: Raw dataset with salary registers.
        
        Output
        salary_data: salary_ ata filtered based on time restrictions. 
        '''
    
        # Limits
        maximum = max(salary_data['Period'])
        minimum = maximum - pd.offsets.MonthBegin(24)

        #Filter
        salary_data =salary_data[(salary_data['Period']>minimum)&(
                                  salary_data['Period']<maximum)].sort_values(by='Period')
    
        return salary_data
    