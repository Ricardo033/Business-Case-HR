#====================#
# Required packages  #
#====================#

import pandas as pd
import numpy as np


class contract_basis_preprocessing (object):
    
    def data_types(contract_data):
        
        ''' 
        This function converts variables into times, and objects and deletes NAN values.
        
        Input
        contract_data: raw data with contracts registers.
        
        Output
        contract_data: Cleaned contract data. 
        '''

        #New Variable To calculate Age and Seniority angainst present  

        #Times
        Time_Variables = ['Company Start Date','Contract Start Date', 'Contract End Date','Birth Date']

        for i in Time_Variables:
            contract_data[i]=pd.Series(contract_data[i],  dtype="string")
            contract_data[i]= pd.to_datetime(contract_data[i],dayfirst=True)

        #Objects
        Object_Variables = ['Firm ID','Department ID','Category ID','Person ID']
        for i in Object_Variables:
            contract_data[i]=pd.Series(contract_data[i],  dtype=object)
        
        # Replacing blank values for null values in Zip
        contract_data['Contract ZIP Code']= contract_data['Contract ZIP Code'].replace(r"    ", "Unknown")#np.NaN)

        return contract_data
    
    # New Columns
    
    def additional_colunmns(contract_data):
        
        '''
        This function creates unique identification, Age and Seniority variables. The birth day of a person, is compared to 
        current date, while seniority uses minimum and maximum dates.
        
        Input
        contract_data: raw data with contracts registers.
        
        Output
        contract_data: dataset with additional columns for the contract data.
        '''

        # Unique Identification 
        contract_data['unique ID'] = (contract_data['Firm ID'].astype("string") +"|"+ contract_data['Department ID'].astype("string") +"|"+ contract_data['Category ID'].astype("string") +"|"+ contract_data['Person ID'].astype("string")).astype(object)

        # Age and Seniority 

        ##Present Time: To calculate Seniority and Age##
        contract_data['present'] = pd.Timestamp.now().date()
        contract_data['present']= pd.to_datetime(
                                     pd.Series(contract_data['present'],  dtype="string"),dayfirst=True
                                                )

        contract_data['Company Start Year_Month'] = contract_data['Company Start Date'].dt.strftime('%Y-%m')
        contract_data['Contract Start Year_Month'] = contract_data['Contract Start Date'].dt.strftime('%Y-%m')

        # Age and Seniority 
        Seniority = contract_data['present']- contract_data['Contract Start Date'] 
        contract_data['Seniority_years'] = round((pd.Series(Seniority).dt.days)/365,2)
        contract_data['Seniority_class'] = np.where(
                            contract_data['Seniority_years']<6,"<6_years",">6_years"
                                                    )

        Age =contract_data['present']- contract_data['Birth Date'] 
        contract_data['Age'] = round((pd.Series(Age).dt.days)/365,0)
        
        contract_data['Age_class']= (
                    np.where(contract_data['Age']<19,'<20',
                       (np.where((contract_data['Age']>=20) & (contract_data['Age']<=25) ,'20-25',
                           (np.where((contract_data['Age']>=26) & (contract_data['Age']<=30) ,'25-30',
                               (np.where((contract_data['Age']>=31) & (contract_data['Age']<=40) ,'30-40',
                                   (np.where((contract_data['Age']>=41) & (contract_data['Age']<=50),'40-50',"50+"
                                                ))))))))))

        return contract_data
    
    def time_filter(contract_data):
    
        '''
        This function filters data based on the last 24 months. Using "Start Contract Date" as reference point.
        
        Input
        contract_data: "Start Contract Date" column from the contracts registers.
        
        Output
        contract_data: Contract data filtered based on time restrictions. 
        '''
        # Limits
        maximum = max(contract_data['Contract Start Date'])
        minimum = maximum - pd.offsets.MonthBegin(24)

        #Filter
        contract_data =contract_data[(contract_data['Contract Start Date']>minimum)&(
                       contract_data['Contract Start Date']<maximum)].sort_values(by='Contract Start Date')
    
        return contract_data
    

        