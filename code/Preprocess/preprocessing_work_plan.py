#====================#
# Required packages  #
#====================#

import pandas as pd
import numpy as np

class work_plan_preprocessing(object):

    def fdcp_duplicates_cleaning(work_plan_data):
        
        '''
        This function removes the extra zeros from the column FDCP, and deletes duplicates from salary data. 
        
        Input
        work_plan_data: Raw dataset with salary registers.
        
        Output
        work_plan_data: work plan data with modified columns.
        '''
        # Deleting Extra Zeros from FDCP COlumn
        work_plan_data[['A','B','C','D']]=(
                                             work_plan_data['FDCP'].copy().str.split('|', 4, expand=True)
                                            ).astype(int).astype("string")
        work_plan_data['FDCP']=(
                         work_plan_data['A']+'|'+work_plan_data['B']+'|'+work_plan_data['C']+'|'+work_plan_data['D']
                                 ).astype(object)

        # Replacing NAN values
        names = {'NACE Description':'Not Registered'}
        work_plan_data.fillna(value=names, inplace=True)
        work_plan_data = work_plan_data.drop(['A','B','C','D'], axis =1)
        
        # Replacing blank values 
        work_plan_data['NACE Code']=work_plan_data['NACE Code'].replace(r'     ', "0")
        return work_plan_data