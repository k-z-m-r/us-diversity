# IMPORT STATEMENTS
import pandas as pds
import numpy as np 

def get_census_df(year = 2017, remove_cols = True):

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

print(get_census_df().head())