# IMPORT STATEMENTS
import pandas as pds
import numpy as np

def get_data(year = 2017, remove_cols = True):

    '''
        year -> the year that the American Community Survey (ACS) was conducted; choices are 2015 and 2017.
        remove_cols -> a Boolean flag on whether to remove columns irrelevant to ethnic/gender diversity.
                       you may want to keep these for comparative analyses.
    '''

    # This is to make sure that the file exists and you're using the correct years.
    try:
        df = pds.read_csv('../data/census_data/acs{}_county_data.csv'.format(year), dtype = str)

        if remove_cols == True:
            columns_to_drop = df.keys()[12:]
            df = df.drop(columns_to_drop, axis = 1)

        # Look for counties such that their ID doesn't have the leading zero (malprocessing error)
        no_leading_zero = df['CountyId'].str.len() == 4

        # A simple fix, but necessary for processing.
        df['CountyId'][no_leading_zero] = '0' + df[no_leading_zero]['CountyId']

        return df


    except:
        print('Incorrect year or data not found!')
        return None

def entropy_by_county(df):

    '''
        df -> the dataframe to calculate the entropy of.
    
    '''
    entropy = lambda p: -p*np.log(p)

    try:
        # First, the entropy by ethnicity
        ethnicities = df.keys()[6:]
        ethnicity_probability = df[ethnicities].astype(float) / 100
        ethnicity_entropy = entropy(ethnicity_probability).fillna(0)
        total_ee = ethnicity_entropy.sum(axis = 1)

        # Second, the entropy by gender
        genders = ['Men', 'Women']
        gender_probability = df[genders].astype(int).divide(df['TotalPop'].astype(float), axis = 0)
        gender_entropy = entropy(gender_probability).fillna(0)
        total_ge = gender_entropy.sum(axis = 1)
        
        # We create a new dataframe.
        merged_df = df[df.keys()[:3]].copy()
        merged_df[ethnicities] = ethnicity_entropy
        merged_df[list(gender_entropy.keys())] = gender_entropy
        merged_df['Ethnicity Entropy'] = total_ee
        merged_df['Gender Entropy'] = total_ge

        return merged_df
    
    except:
        print('Poorly formatted dataframe!')
        return None