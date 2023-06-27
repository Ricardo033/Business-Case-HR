#====================#
# Required packages  #
#====================#

import pandas as pd
import numpy as np

class absenses_preprocessing  (object):

    def data_types(absences_data):
        ''' 
        This function is used to assign a new data type to some columns for future processes, like joining data.
        
        Input
        absences_data: raw data with absences registers
        
        Output
        absences_data: Clean absences data
        '''

        #Objects
        Object_Variables = ['Firm ID','Department ID','Category ID','Person ID','Year','Quarter','Month']
        for i in Object_Variables:
            absences_data[i]=pd.Series(absences_data[i],  dtype=object)
        
        #Floats
        float_Variables = ['Qty_Days_Worked','Qty_Working_Days']
        for i in float_Variables:
            absences_data[i] = pd.Series(absences_data[i],  dtype="string").apply(lambda x: x.replace(',','.'))
            absences_data[i] = absences_data[i].astype(float)
        
        #Fixing name
        absences_data.rename(columns={'Freq_Z3_Daqs':'Freq_Z3_Days'}, inplace=True)

        return absences_data
    
    def additional_colunmns(absences_data):
        
        ''' 
        This function creates the unique id FDCP to link contracts dataset with other data.
        
        Input
        absences_data: raw data  or clean absences dataset can be used.
        
        Output
        absences_data: Unique identification per employee, to connect with FDCP.
        '''

        # Unique Identification 
        absences_data['unique ID'] = (absences_data['Firm ID'].astype("string") +"|"+ absences_data['Department ID'].astype("string") +"|"+ absences_data['Category ID'].astype("string") +"|"+ absences_data['Person ID'].astype("string")).astype(object)
        
        return absences_data