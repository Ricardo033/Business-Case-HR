#====================#
# Required packages  #
#====================#

import pandas as pd
import numpy as np


class postcodes_preprocessing(object):
    

    def data_types(postcodes_data):

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

        postcodes_data=pd.merge(postcodes_data, locations_data,left_on='PostCode',right_on='zip')
        postcodes_data.drop('zip',axis = 1, inplace = True)
        
        return postcodes_data
