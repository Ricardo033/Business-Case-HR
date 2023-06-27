#====================#
# Required packages  #
#====================#

import pandas as pd
import numpy as np


class postcodes_preprocessing(object):
    

    def data_types(postcodes_data):
        
        '''
        This function converts some columns into object types.
        
        Input
        postcodes_data: dataset with a list of postcodes and regions
        
        Output
        contract_data: Postcodes dataset with data types modified.
        '''

        #Objects
        Object_Variables = ['PostCode','Region_Code','Region']
        for i in Object_Variables:
            postcodes_data[i]=pd.Series(postcodes_data[i],  dtype="string")
            postcodes_data[i]=pd.Series(postcodes_data[i],  dtype=object)
            
        return postcodes_data
    
    def location_types(locations_data):
    
        Object_Variables = ['zip','city']
        for i in Object_Variables:
            locations_data[i]=pd.Series(locations_data[i],  dtype="string")
            locations_data[i]=pd.Series(locations_data[i],  dtype=object)

        return locations_data

    def coordinates_cities(postcodes_data,locations_data):
        
        '''
        This function includes latitudes and longitudes of cities based on postcodes.
        
        Input
        postcodes_data: dataset with a list of postcodes and regions
        locations_data: Dataframe with a list that contains latitudes and longitudes in Belgium
        
        Output
        postcodes_data: Postcodes data after being merged with locations.
        '''

        postcodes_data=pd.merge(postcodes_data, locations_data,left_on='PostCode',right_on='zip')
        postcodes_data.drop('zip',axis = 1, inplace = True)
        
        return postcodes_data
