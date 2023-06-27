#-------------------------#
# Preprocessing Functions #
#-------------------------#

#====================#
# Required packages  #
#====================#

import pandas as pd
import numpy as np


class contract_basis_preprocessing (object):
    

    def data_types(contract_data):

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

        # Unique Identification 
        contract_data['unique ID'] = (contract_data['Firm ID'].astype("string") +"|"+ contract_data['Department ID'].astype("string") +"|"+ contract_data['Category ID'].astype("string") +"|"+ contract_data['Person ID'].astype("string")).astype(object)

        # Age and Seniority 

        ##Present Time: To calculate Seniority and Age##
        contract_data['present'] = pd.Timestamp.now().date()
        contract_data['present']= pd.to_datetime(pd.Series(contract_data['present'],  dtype="string"),dayfirst=True)

        contract_data['Company Start Year_Month'] = contract_data['Company Start Date'].dt.strftime('%Y-%m')
        contract_data['Contract Start Year_Month'] = contract_data['Contract Start Date'].dt.strftime('%Y-%m')

        # Age and Seniority 
        Seniority = contract_data['present']- contract_data['Contract Start Date'] 
        contract_data['Seniority_years'] = round((pd.Series(Seniority).dt.days)/365,2)
        contract_data['Seniority_class'] = np.where(contract_data['Seniority_years']<6,"Less than 6 years","More than 6 years")

        Age =contract_data['present']- contract_data['Birth Date'] 
        contract_data['Age'] = round((pd.Series(Age).dt.days)/365,0)
        contract_data['Age_class']  = np.where(contract_data['Age']<30, "less 30_Years",
                                     (np.where(contract_data['Age']>50,"Over 50_years","30-50 Years")))

        return contract_data
    
    def time_filter(contract_data):
    
        # Limits
        maximum = max(contract_data['Contract Start Date'])
        minimum = maximum - pd.offsets.MonthBegin(24)

        #Filter
        contract_data =contract_data[(contract_data['Contract Start Date']>minimum)&(
                       contract_data['Contract Start Date']<maximum)].sort_values(by='Contract Start Date')
    
        return contract_data
    

        