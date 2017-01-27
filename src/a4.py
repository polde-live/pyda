# -*- coding: utf-8 -*-
"""
Assignment 4.
Hypothesis Testing
"""

import pandas as pd
import numpy as np
# from scipy.stats import ttest_ind

# Use this dictionary to map state names to two letter acronyms
states = {'OH': 'Ohio',
          'KY': 'Kentucky',
          'AS': 'American Samoa',
          'NV': 'Nevada',
          'WY': 'Wyoming',
          'NA': 'National',
          'AL': 'Alabama',
          'MD': 'Maryland',
          'AK': 'Alaska',
          'UT': 'Utah',
          'OR': 'Oregon',
          'MT': 'Montana',
          'IL': 'Illinois',
          'TN': 'Tennessee',
          'DC': 'District of Columbia',
          'VT': 'Vermont',
          'ID': 'Idaho',
          'AR': 'Arkansas',
          'ME': 'Maine',
          'WA': 'Washington',
          'HI': 'Hawaii',
          'WI': 'Wisconsin',
          'MI': 'Michigan',
          'IN': 'Indiana',
          'NJ': 'New Jersey',
          'AZ': 'Arizona',
          'GU': 'Guam',
          'MS': 'Mississippi',
          'PR': 'Puerto Rico',
          'NC': 'North Carolina',
          'TX': 'Texas',
          'SD': 'South Dakota',
          'MP': 'Northern Mariana Islands',
          'IA': 'Iowa',
          'MO': 'Missouri',
          'CT': 'Connecticut',
          'WV': 'West Virginia',
          'SC': 'South Carolina',
          'LA': 'Louisiana',
          'KS': 'Kansas',
          'NY': 'New York',
          'NE': 'Nebraska',
          'OK': 'Oklahoma',
          'FL': 'Florida',
          'CA': 'California',
          'CO': 'Colorado',
          'PA': 'Pennsylvania',
          'DE': 'Delaware',
          'NM': 'New Mexico',
          'RI': 'Rhode Island',
          'MN': 'Minnesota',
          'VI': 'Virgin Islands',
          'NH': 'New Hampshire',
          'MA': 'Massachusetts',
          'GA': 'Georgia',
          'ND': 'North Dakota',
          'VA': 'Virginia'}


def get_list_of_university_towns():
    '''Returns a DataFrame of towns and the states they are in from the
    university_towns.txt list. The format of the DataFrame should be:
    DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ],
    columns=["State", "RegionName"]  )

    The following cleaning needs to be done:

    1. For "State", removing characters from "[" to the end.
    2. For "RegionName", when applicable, removing every character from " ("
    to the end.
    3. Depending on how you read the data, you may need to remove newline
    character '\n'.
    '''

    uc = pd.read_table('../data/university_towns.txt', header=None).iloc[:, 0]
    uc = uc.tolist()

    dat = []
    for town in uc:
        if town.endswith('[edit]'):
            state = town.replace('[edit]', '')
        else:
            dat.append([state, town])
    cnam = ['State', 'RegionName']
    df = pd.DataFrame(dat, columns=cnam)
    df['RegionName'] = df['RegionName'].str.replace('\[.+', '')
    df['RegionName'] = df['RegionName'].str.replace('\(.+', '')
    # remove trailing whitespaces
    df['RegionName'] = df['RegionName'].str.replace('\s+$', '')
    df['RegionName'] = df['RegionName'].str.replace('\s+$', '')
    return(df)


def gdp_ind(tm1, t0, t1, t2):
    """ Helper funcion, calculate business cycle indicators:
        Find business cycle indicator for t1:
    """
    if t0 > t1 > t2:
        return "recession"
    if tm1 < t0 < t1:
        return "recovery"
    else:
        return "stable"


def get_gdp():
    """
    Helper to read gdp data into data frame.
    Returns data frame from gdplev.xls.
    """
    gdp = pd.read_excel('../data/gdplev.xls', skiprows=8, header=None)
    gdp = gdp.loc[:][[4, 5, 6]]
    gdp.columns = ['qt', 'gdpcur', 'gdp09']
    gdp = gdp[gdp['qt'] >= '2000q1']
    # calculate business cycle indicators
    gdp['bc'] = np.nan
    for i in range(2, len(gdp)-2):
        tm1 = gdp.iloc[i-2, 2]
        t0 = gdp.iloc[i-1, 2]
        t1 = gdp.iloc[i, 2]
        t2 = gdp.iloc[i+1, 2]
        gdp.iloc[i, 3] = gdp_ind(tm1, t0, t1, t2)
    gdp.set_index('qt', inplace=True)

    return(gdp)


def get_recession_start():
    '''Returns the year and quarter of the recession start time as a
    string value in a format such as 2005q3
    A recession is defined as starting with two consecutive quarters of GDP
    decline, and ending with two consecutive quarters of GDP growth
    '''
    gdp = get_gdp()
    for i in range(0, len(gdp)):
        if gdp.iloc[i, 2] == 'recession':
            return(gdp.index[i])


def get_recession_end():
    '''Returns the year and quarter of the recession end time as a
    string value in a format such as 2005q3
    A recession is defined as starting with two consecutive quarters of GDP
    decline, and ending with two consecutive quarters of GDP growth.'''
    # find gdp after recession start
    recstart = get_recession_start()
    gdp = get_gdp()
    gdp = gdp[gdp.index > recstart]
    for i in range(0, len(gdp)):
        if gdp.iloc[i, 2] == 'recovery':
            return(gdp.index[i])


def get_recession_bottom():
    '''Returns the year and quarter of the recession bottom time as a
    string value in a format such as 2005q3
    A recession bottom is the quarter within a recession which had the lowest
    GDP.'''
    # dates of recession period
    rstart = get_recession_start()
    rend = get_recession_end()
    gdp = get_gdp()
    gdp = gdp[gdp.index >= rstart]
    gdp = gdp[gdp.index <= rend]
    return(gdp['gdp09'].argmin())


def convert_housing_data_to_quarters():
    '''Converts the housing data to quarters and returns it as mean
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].

    Note: Quarters are defined in the assignment description, they are
    not arbitrary three month periods.

    The resulting dataframe should have 67 columns, and 10,730 rows.
    '''

    return "ANSWER"


def run_ttest():
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values,
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence.

    Return the tuple (different, p, better) where different=True if the t-test
    is True at a p<0.01 (we reject the null hypothesis), or different=False if
    otherwise (we cannot reject the null hypothesis). The variable p should
    be equal to the exact p value returned from scipy.stats.ttest_ind(). The
    value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss).'''

    return "ANSWER"