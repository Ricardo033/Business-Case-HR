#====================#
# Required packages  #
#====================#

import pandas as pd
import numpy as np

class process_funtions(object):

    def categories_by_person(absenses_data):
        
        # Variables
        filt = absenses_data.drop(['Firm ID', 'Department ID', 'Category ID', 'Person ID', 'Year',
           'Quarter', 'Month', 'Date', 'Period', 'Qty_Illness_Days', 'Freq_Z0_Days', 'Freq_Z1_Days', 'Freq_Z2_Days',
           'Freq_Z3_Days', 'Freq_P0_Days', 'Freq_P1_Days', 'Freq_P2_Days',
           'Freq_P3_Days', 'Freq_A1_Days', 'Freq_A2_Days', 'Qty_Days_Worked',
           'Qty_Working_Days'],axis = 1)
    
        person_ab_categories = pd.DataFrame(absenses_data['unique ID'].unique())
        person_ab_categories.columns =['unique ID'] 
        iterations = len(filt.columns)-1

        # Creating Table that shows wheter a person had a type of absense (1 = Absence ,0 = No Absence)
        for i in range(0,iterations):
            #print(f"{i}, iteration") 
            # Filter Values based on 
            filt2 = filt.iloc[:,[-1,i]]
            filt3 = filt2[filt2.iloc[:,1] > 0]
        
            names =list(filt3.columns.values.tolist())
            column = names[1]
            filt3[column]=1
            
            # Getting Unique ID values
            group = filt3.groupby('unique ID')
            filt4 = group.min()

            person_ab_categories = pd.merge(person_ab_categories,filt4, on='unique ID', how ='left')
            
        person_ab_categories = person_ab_categories.fillna(0)
        return person_ab_categories
    
    def regions_categories(contract_data,postcodes_data,categories_data):
         
        join1 = pd.merge(contract_data, postcodes_data,left_on='Contract ZIP Code',right_on='PostCode',how="left")
        join2 = pd.merge(join1, categories_data,on='unique ID',how="left")
        
        # Assigning Category based on 1= Absent , 0= Not Absent, NAN = Not Registered
        category_mames = ['Qty_Z0_Days','Qty_Z1_Days', 'Qty_Z2_Days', 'Qty_Z3_Days','Qty_P0_Days',
                          'Qty_P1_Days','Qty_P2_Days', 'Qty_P3_Days', 'Qty_A1_Days','Qty_A2_Days']
        
        for i in category_mames:
            join2[i]  = np.where(join2[i]==0,"Not Absent",
                                (np.where(join2[i]==1,"Absent","Not Registered")))
            
        # Indicating contracts with unknown location
        locations_names = ['Contract ZIP Code','Region_Code','Region', 'city', 'PostCode']
        
        for i in locations_names:
            join2[i]= join2[i].replace(np.NAN, "Unknown")#np.NaN)
        
        # Assigning Central location (Belgium Geographic coordinates, lat-lng) to unkonw locations
        join2['lat']= join2['lat'].replace(np.NAN, 50.503887)#np.NaN)
        join2['lng']= join2['lng'].replace(np.NAN, 4.469936)#np.NaN)
        
        return join2
    
    def head_counts(unified_contract_data):
        
        # Variables with categories to filter the count of contracts
        names1 =['Region', 'city','lng','lat','Contract Start Year_Month']
        names2 =['Region','Contract Start Year_Month','Gender','Seniority_class','Age_class',
                 'Qty_Z1_Days','Qty_Z2_Days', 'Qty_Z3_Days','Qty_P1_Days', 'Qty_P2_Days', 
                 'Qty_P3_Days', 'Qty_A1_Days','Qty_A2_Days']

        #Counting contracts per category 
        contracts_evolution = unified_contract_data.groupby(names1).aggregate({'unique ID':'count'}).reset_index()
        contracts_category = unified_contract_data.groupby(names2).aggregate({'unique ID':'count'}).reset_index()

        # List with 2 different results (Counts by location by city, and counts with all categories by region) 
        head_count = [contracts_evolution.copy(), contracts_category.copy()]

        return head_count    
    
    def variation(unified_contract_data):
        
        # Setting Variables
        
        # Considering all contracts are valid from 1st day of the month 
        unified_contract_data['variation_start_date'] = pd.to_datetime(
                             unified_contract_data['Contract Start Date'].copy()).apply(lambda x: x.replace(day=1))
        unified_contract_data['Variation_IN'] = np.where(
                             unified_contract_data['variation_start_date'].isnull()!= True,'IN','Unregistered')
        unified_contract_data['Variation_Out'] = np.where(
                             unified_contract_data['Contract End Date'].isnull() != True,'Out','Unregistered')
        unified_contract_data['Contract Terminatio Reason'] = (
                        unified_contract_data['Contract Terminatio Reason'].copy().replace(np.NAN, 'Unregistered'))
        
        names_in =['Region','variation_start_date','Gender','Variation_IN',
                'Contract Terminatio Reason','Seniority_class','Age_class','Qty_Z1_Days', 'Qty_Z2_Days', 
                'Qty_Z3_Days','Qty_P1_Days', 'Qty_P2_Days', 'Qty_P3_Days', 'Qty_A1_Days','Qty_A2_Days']
        
        names_out =['Region','Contract End Date','Gender','Variation_Out',
                'Contract Terminatio Reason','Seniority_class','Age_class','Qty_Z1_Days', 'Qty_Z2_Days', 
                'Qty_Z3_Days','Qty_P1_Days', 'Qty_P2_Days', 'Qty_P3_Days', 'Qty_A1_Days','Qty_A2_Days']
        
        #Counting contracts per category 
        variation_in = unified_contract_data.groupby(names_in).aggregate({'unique ID':'count'}).reset_index()
        variation_out = unified_contract_data.groupby(names_out,dropna=False).aggregate({'unique ID':'count'}).reset_index()
        
        variation= [variation_in, variation_out]

        return variation

    def salary_analysis(salary_data, unified_contract_data):
    
        # Variables to merge contracts and salaries
        contract_info = unified_contract_data.copy().drop(
                            ['Contract ZIP Code', 'Firm ID', 'Department ID', 'Category ID',
                           'Person ID', 'Contract Start Date', 'Contract End Date',
                           'Company Start Date', 'Birth Date', 'Contract Terminatio Reason',
                           'Contract Type', 'present','Company Start Year_Month', 'Contract Start Year_Month',
                           'Seniority_years', 'Age', 'Qty_Z0_Days', 'Qty_P0_Days', 
                            'variation_start_date', 'Variation_IN', 'Variation_Out'],axis=1
                                                                    )
        salary_all =  pd.merge(salary_data.copy(),contract_info.copy(),left_on='FDCP',right_on='unique ID',how="left")
        # Salaries for people in and out of the contract list
        salary_out = salary_all.copy()[salary_all['unique ID'].isnull() == True]
        salary_in =  pd.merge(salary_data.copy(),contract_info,left_on='FDCP',right_on='unique ID',how="inner")

        # Salary costs
        in_names = ['Period','Gender','Nationality','Seniority_class', 'Age_class', 
                    'PostCode','Region_Code', 'Region', 'city', 'lng', 'lat',
                    'Qty_Z1_Days', 'Qty_Z2_Days', 'Qty_Z3_Days', 'Qty_P1_Days',
                    'Qty_P2_Days', 'Qty_P3_Days', 'Qty_A1_Days', 'Qty_A2_Days']
        out_names =['Period','FDCP']

        salary_cost_in = salary_in.groupby(in_names,dropna=False).aggregate({'Gross Salary':'sum'}).reset_index()
        salary_cost_out = salary_out.groupby(out_names,dropna=False).aggregate({'Gross Salary':'sum'}).reset_index()

        # List with total salary costs for people in and out of the contract list
        salary_cost = [salary_cost_in,salary_cost_out]

        return salary_cost
    
    def absence_analysis(unified_contract_data,work_plan_data,absences_data):
    
        #Variables 
        categories=['unique ID','Gender', 'Nationality','Seniority_class', 'Age_class','Region_Code', 'Region']
        employes_categories = unified_contract_data[categories].copy()


        # Unique work_plan: FDCP + NACE Code
        work_plan_data['NC']=work_plan_data['NACE Code'].copy()
        work_plan_data = (work_plan_data.groupby(['FDCP','NACE Code'],dropna=False).aggregate(
                                            {'NC':'count'}).reset_index()).drop('NC',axis=1)

        absences_cat=pd.merge(absences_data,employes_categories, on ='unique ID', how='left')
        absences_cat_work=pd.merge(absences_cat,work_plan_data, left_on ='unique ID', right_on='FDCP', how='left')

        cat_names = ['NACE Code','Region','Period','Age_class','Seniority_class' ]
        abs_days = absences_cat_work.groupby(cat_names,dropna=False).aggregate(
                        {'Qty_Z0_Days':'sum','Qty_Z1_Days':'sum',
                         'Qty_Z2_Days':'sum','Qty_Z3_Days':'sum',
                         'Qty_P0_Days':'sum','Qty_P1_Days':'sum',
                         'Qty_P2_Days':'sum','Qty_P3_Days':'sum',
                         'Qty_A1_Days':'sum','Qty_A2_Days':'sum'}).reset_index()
        
        abs_freq = absences_cat_work.groupby(cat_names,dropna=False).aggregate(
                        {'Freq_Z0_Days':'sum','Freq_Z1_Days':'sum',
                         'Freq_Z2_Days':'sum','Freq_Z3_Days':'sum',
                         'Freq_P0_Days':'sum','Freq_P1_Days':'sum',
                         'Freq_P2_Days':'sum','Freq_P3_Days':'sum',
                         'Freq_A1_Days':'sum','Freq_A2_Days':'sum'}).reset_index()

        names = ['Region','Age_class','Seniority_class' ]

        for i in names:
            abs_days[i]= abs_days[i].replace(np.NAN, "Unknown")
            abs_freq[i]= abs_freq[i].replace(np.NAN, "Unknown")
            absences_cat_work[i]= absences_cat_work[i].replace(np.NAN, "Unknown")
            
        absences =[abs_days,abs_freq,absences_cat_work]


        return absences

    