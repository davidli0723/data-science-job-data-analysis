#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# Third-party libraries
# NOTE: You may **only** use the following third-party libraries:
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd 
from thefuzz import fuzz
from thefuzz import process
# NOTE: It isn't necessary to use all of these to complete the assignment, 
# but you are free to do so, should you choose.

# Standard libraries
# NOTE: You may use **any** of the Python 3.11 or Python 3.12 standard libraries:
# https://docs.python.org/3.11/library/index.html
# https://docs.python.org/3.12/library/index.html
from pathlib import Path
# ... import your standard libraries here ...


######################################################
# NOTE: DO NOT MODIFY THE LINE BELOW ...
######################################################
studentid = Path(__file__).stem

######################################################
# NOTE: DO NOT MODIFY THE FUNCTION BELOW ...
######################################################
def log(question, output_df, other):
    print(f"--------------- {question}----------------")

    if other is not None:
        print(question, other)
    if output_df is not None:
        df = output_df.head(5).copy(True)
        for c in df.columns:
            df[c] = df[c].apply(lambda a: a[:20] if isinstance(a, str) else a)

        df.columns = [a[:10] + "..." for a in df.columns]
        print(df.to_string())


######################################################
# NOTE: YOU MAY ADD ANY HELPER FUNCTIONS BELOW ...
######################################################
def fuzzy_merge(df_1, df_2, key1, key2, threshold=90, limit=1):
    """
    :param df_1: the left table to join
    :param df_2: the right table to join
    :param key1: key column of the left table
    :param key2: key column of the right table
    :param threshold: how close the matches should be to return a match, based on Levenshtein distance
    :param limit: the amount of matches that will get returned, these are sorted high to low
    :return: dataframe with boths keys and matches
    """
    s = df_2[key2].tolist()
    
    m = df_1[key1].apply(lambda x: process.extract(x, s, limit=limit))    
    df_1['matches'] = m
    
    m2 = df_1['matches'].apply(lambda x: ', '.join([i[0] for i in x if i[1] >= threshold]))
    df_1['matches'] = m2
    
    return df_1


######################################################
# QUESTIONS TO COMPLETE BELOW ...
######################################################

######################################################
# NOTE: DO NOT MODIFY THE FUNCTION SIGNATURE BELOW ...
######################################################
def question_1(jobs_csv):
    """Read the data science jobs CSV file into a DataFrame.

    See the assignment spec for more details.

    Args:
        jobs_csv (str): Path to the jobs CSV file.

    Returns:
        DataFrame: The jobs DataFrame.
    """

    ######################################################
    # TODO: Your code goes here ...
    ######################################################
    df = pd.read_csv(jobs_csv)

    ######################################################
    # NOTE: DO NOT MODIFY THE CODE BELOW ...
    ######################################################
    log("QUESTION 1", output_df=df, other=df.shape)
    return df



######################################################
# NOTE: DO NOT MODIFY THE FUNCTION SIGNATURE BELOW ...
######################################################
def question_2(cost_csv, cost_url):
    """Read the cost of living CSV into a DataFrame.  If the CSV file does not 
    exist, scrape it from the specified URL and save it to the CSV file.

    See the assignment spec for more details.

    Args:
        cost_csv (str): Path to the cost of living CSV file.
        cost_url (str): URL of the cost of living page.

    Returns:
        DataFrame: The cost of living DataFrame.
    """

    ######################################################
    # TODO: Your code goes here ...
    ######################################################
    cost_csv_file = Path(cost_csv)
    if cost_csv_file.exists():
        df = pd.read_csv(cost_csv_file)
    else:
        df = pd.read_html(cost_url)
        df = df[0]
        df.columns = df.columns.str.replace(' ', '_')
        df.columns = df.columns.str.lower()
        df.to_csv(cost_csv, index=False)

    
    ######################################################
    # NOTE: DO NOT MODIFY THE CODE BELOW ...
    ######################################################
    log("QUESTION 2", output_df=df, other=df.shape)
    return df


######################################################
# NOTE: DO NOT MODIFY THE FUNCTION SIGNATURE BELOW ...
######################################################
def question_3(currency_csv, currency_url):
    """Read the currency conversion rates CSV into a DataFrame.  If the CSV 
    file does not exist, scrape it from the specified URL and save it to 
    the CSV file.

    See the assignment spec for more details.

    Args:
        cost_csv (str): Path to the currency conversion rates CSV file.
        cost_url (str): URL of the currency conversion rates page.

    Returns:
        DataFrame: The currency conversion rates DataFrame.
    """

    ######################################################
    # TODO: Your code goes here ...
    ######################################################
    currency_csv_file = Path(currency_csv)
    if currency_csv_file.exists():
        df = pd.read_csv(currency_csv_file)
    else:
        df = pd.read_html(currency_url)
        df = df[0]
        df.drop(columns='Nearest actual exchange rate', inplace=True)
        df.columns = map(lambda x: x[1], df.columns)
        df.columns = df.columns.str.replace('\xa0', ' ')
        df.columns = df.columns.str.lower()
        df.drop(columns='30 jun 23', inplace=True)
        df.rename(columns={'31 dec 23': 'rate'}, inplace=True)
        df.to_csv(currency_csv, index=False)

    ######################################################
    # NOTE: DO NOT MODIFY THE CODE BELOW ...
    ######################################################
    log("QUESTION 3", output_df=df, other=df.shape)
    return df


######################################################
# NOTE: DO NOT MODIFY THE FUNCTION SIGNATURE BELOW ...
######################################################
def question_4(country_csv, country_url):
    """Read the country codes CSV into a DataFrame.  If the CSV file does not 
    exist, it will be scrape the data from the specified URL and save it to the 
    CSV file.

    See the assignment spec for more details.

    Args:
        cost_csv (str): Path to the country codes CSV file.
        cost_url (str): URL of the country codes page.

    Returns:
        DataFrame: The country codes DataFrame.
    """

    ######################################################
    # TODO: Your code goes here ...
    ######################################################
    country_csv_file = Path(country_csv)
    if country_csv_file.exists():
        df = pd.read_csv(country_csv_file)
    else:
        df = pd.read_html(country_url)
        df = df[0]
        df.drop(columns=['Year', 'ccTLD', 'Notes'], inplace=True)
        df.rename(columns={'Country name (using title case)': 'country', 'Code': 'code'}, inplace=True)
        df.to_csv(country_csv, index=False)


    ######################################################
    # NOTE: DO NOT MODIFY THE CODE BELOW ...
    ######################################################
    log("QUESTION 4", output_df=df, other=df.shape)
    return df


######################################################
# NOTE: DO NOT MODIFY THE FUNCTION SIGNATURE BELOW ...
######################################################
def question_5(jobs_df):
    """Summarise some dimensions of the jobs DataFrame.

    See the assignment spec for more details.

    Args:
        jobs_df (DataFrame): The jobs DataFrame returned in question 1.

    Returns:
        DataFrame: The summary DataFrame.
    """

    ######################################################
    # TODO: Your code goes here ...
    ######################################################
    df = jobs_df

    num_of_rows = df.shape[0]
    num_of_rows

    summary_list = []

    for column in df:
        number_of_missing = df[column].isnull().sum()
        number_of_distinct = df[column].nunique()
        number_of_observartion = num_of_rows - number_of_missing
        summary_list.append([number_of_observartion, number_of_distinct, number_of_missing])

    summary_df = pd.DataFrame(summary_list, columns=['observations', 'distinct', 'missing'], index=list(df.columns))
    df = summary_df

    ######################################################
    # NOTE: DO NOT MODIFY THE CODE BELOW ...
    ######################################################
    log("QUESTION 5", output_df=df, other=df.shape)
    return df


######################################################
# NOTE: DO NOT MODIFY THE FUNCTION SIGNATURE BELOW ...
######################################################
def question_6(jobs_df):
    """Add an experience rating column to the jobs DataFrame.

    See the assignment spec for more details.

    Args:
        jobs_df (DataFrame): The jobs DataFrame returned in question 1.

    Returns:
        DataFrame: The jobs DataFrame with the experience rating column added.
    """

    ######################################################
    # TODO: Your code goes here ...
    ######################################################
    df = jobs_df
    def rating(level):
        if level == 'EN':
            return 1
        elif level == 'MI':
            return 2
        elif level == 'SE':
            return 3
        elif level == 'EX':
            return 4
    df['experience_rating'] = df['experience_level'].apply(rating)

    ######################################################
    # NOTE: DO NOT MODIFY THE CODE BELOW ...
    ######################################################
    log("QUESTION 6", output_df=df, other=df.shape)
    return df


######################################################
# NOTE: DO NOT MODIFY THE FUNCTION SIGNATURE BELOW ...
######################################################
def question_7(jobs_df, country_df):
    """Merge the jobs and country codes DataFrames.

    See the assignment spec for more details.

    Args:
        jobs_df (DataFrame): The jobs DataFrame returned in question 6.
        country_df (DataFrame): The country codes DataFrame returned in 
                                question 4.

    Returns:
        DataFrame: The merged DataFrame.
    """

    ######################################################
    # TODO: Your code goes here ...
    ######################################################
    df = pd.merge(jobs_df, country_df, how='left', left_on='employee_residence', right_on='code')
    df.drop(columns='code', inplace=True)


    ######################################################
    # NOTE: DO NOT MODIFY THE CODE BELOW ...
    ######################################################
    log("QUESTION 7", output_df=df, other=df.shape)
    return df


######################################################
# NOTE: DO NOT MODIFY THE FUNCTION SIGNATURE BELOW ...
######################################################
def question_8(jobs_df, currency_df):
    """Add an Australian dollar salary column to the jobs DataFrame.

    See the assignment spec for more details.

    Args:
        jobs_df (DataFrame): The jobs DataFrame returned in question 7.
        currency_df (DataFrame): The currency conversion rates DataFrame 
                                 returned in question 3.

    Returns:
        DataFrame: The jobs DataFrame with the Australian dollar salary column
                   added.
    """

    ######################################################
    # TODO: Your code goes here ...
    ######################################################
    df = jobs_df.query('work_year == 2023')
    currency_df = currency_df
    currency_df['rate'] = currency_df['rate'].replace('na', 0)
    currency_df['rate'] = pd.to_numeric(currency_df['rate'])
    exchange_rate = currency_df.query('currency == "United States dollar"')['rate'].iloc[0]
    df['salary_in_aud'] = df['salary_in_usd']/exchange_rate
    df['salary_in_aud'] = df['salary_in_aud'].astype('int64')

    
    ######################################################
    # NOTE: DO NOT MODIFY THE CODE BELOW ...
    ###################################### ################
    log("QUESTION 8", output_df=df, other=df.shape)
    return df


######################################################
# NOTE: DO NOT MODIFY THE FUNCTION SIGNATURE BELOW ...
######################################################
def question_9(cost_df):
    """Re-scale the cost of living DataFrame to be relative to Australia.

    See the assignment spec for more details.

    Args:
        cost_df (DataFrame): The cost of living DataFrame returned in question 2.

    Returns:
        DataFrame: The re-scaled cost of living DataFrame.
    """

    ######################################################
    # TODO: Your code goes here ...
    ######################################################
    df = cost_df[['country', 'cost_of_living_plus_rent_index']]

    aus_index = df.query('country == "Australia"')['cost_of_living_plus_rent_index'].iloc[0]

    df['cost_of_living_plus_rent_index'] = df['cost_of_living_plus_rent_index'] / aus_index * 100
    df['cost_of_living_plus_rent_index'] = df['cost_of_living_plus_rent_index'].round(1)

    df.sort_values(by='cost_of_living_plus_rent_index', inplace=True)
    
    ######################################################
    # NOTE: DO NOT MODIFY THE CODE BELOW ...
    ######################################################
    log("QUESTION 9", output_df=df, other=df.shape)
    return df


######################################################
# NOTE: DO NOT MODIFY THE FUNCTION SIGNATURE BELOW ...
######################################################
def question_10(jobs_df, cost_df):
    """Merge the jobs and cost of living DataFrames.

    See the assignment spec for more details.

    Args:
        jobs_df (DataFrame): The jobs DataFrame returned in question 8.
        cost_df (DataFrame): The cost of living DataFrame returned in question 9.

    Returns:
        DataFrame: The merged DataFrame.
    """

    ######################################################
    # TODO: Your code goes here ...
    ######################################################
    df = fuzzy_merge(jobs_df, cost_df, 'country', 'country', threshold=90)
    df = df.query('matches != ""')
    df = pd.merge(df, cost_df, how='left', left_on='matches', right_on='country')
    df.drop(['matches', 'country_y'], axis=1, inplace=True)
    df.rename(columns={'country_x': 'country', 'cost_of_living_plus_rent_index': 'cost_of_living'}, inplace=True)


    ######################################################
    # NOTE: DO NOT MODIFY THE CODE BELOW ...
    ######################################################
    log("QUESTION 10", output_df=df, other=df.shape)
    return df


######################################################
# NOTE: DO NOT MODIFY THE FUNCTION SIGNATURE BELOW ...
######################################################
def question_11(jobs_df):
    """Create a pivot table of the average salary in AUD by country and 
    experience rating.

    See the assignment spec for more details.

    Args:
        jobs_df (DataFrame): The jobs DataFrame returned in question 10.

    Returns:
        DataFrame: The pivot table.
    """

    ######################################################
    # TODO: Your code goes here ...
    ######################################################
    df = pd.pivot_table(jobs_df, values="salary_in_aud", index=['country'], columns=['experience_rating'], aggfunc=np.average)
    df.columns = pd.MultiIndex.from_product([['salary_in_aud'], df.columns])
    df = df.fillna(0)
    df = df.astype(int)
    df = df.sort_values(by=list(df.columns), ascending=False)

    ######################################################
    # NOTE: DO NOT MODIFY THE CODE BELOW ...
    ######################################################
    log("QUESTION 11", output_df=None, other=df)
    return df


######################################################
# NOTE: DO NOT MODIFY THE FUNCTION SIGNATURE BELOW ...
######################################################
def question_12(jobs_df):
    """Create a visualisation of data science jobs to help inform a decision
    about where to live, based (minimally) on salary and cost of living.

    See the assignment spec for more details.

    Args:
        jobs_df (DataFrame): The jobs DataFrame returned in question 10.
    """

    ######################################################
    # TODO: Your code goes here ...
    ######################################################
    df = jobs_df

    #filter executive level record
    filter_experience_df = df.query('experience_rating != 4')

    #only count countries with more than or equal to five disinct records to get accuracy and avoid outliers
    value_counts = filter_experience_df['country'].value_counts()
    filtered_country = value_counts[value_counts >= 5].index.tolist()
    filter_country_df = filter_experience_df.query('country in @filtered_country or country == "Australia"')

    #create pivot table to calculate average salary of different countries
    q12_pivot_table = pd.pivot_table(filter_country_df, values=["salary_in_aud", "cost_of_living"], index=['country'], aggfunc=np.average)
    q12_pivot_table.rename(index={'United States of America': 'US', 'United Kingdom of Great Britain and Northern Ireland': 'UK'}, inplace=True)

    #plot scatter graph
    graph_df = q12_pivot_table.reset_index()

    cost_of_living = graph_df['cost_of_living']
    salary_in_aud = graph_df['salary_in_aud']
    countries = graph_df['country']

    plt.figure(figsize=(10, 6))

    plt.xlabel('Cost of Living Index')
    plt.ylabel('Salary in AUD')
    plt.title('Compare cost of living vs salary in AUD in non-executive level data science jobs in different countries')
    for i, country in enumerate(countries):
        if country == "Australia":
            plt.scatter(x=cost_of_living[i], y=salary_in_aud[i], color='red')
        else:
            plt.scatter(x=cost_of_living[i], y=salary_in_aud[i], color='blue')
        plt.annotate(country, (cost_of_living[i], salary_in_aud[i]), textcoords="offset points", xytext=(0,5), ha='center', fontsize=11)

    ######################################################
    # NOTE: DO NOT MODIFY THE CODE BELOW ...
    ######################################################
    plt.savefig(f"{studentid}-Q12.png")


######################################################
# NOTE: DO NOT MODIFY THE MAIN FUNCTION BELOW ...
######################################################
if __name__ == "__main__":
    # data ingestion and cleaning
    df1 = question_1("ds_jobs.csv")
    df2 = question_2("cost_of_living.csv", 
                     "https://www.cse.unsw.edu.au/~cs9321/24T1/ass1/cost_of_living.html")
    df3 = question_3("exchange_rates.csv", 
                     "https://www.cse.unsw.edu.au/~cs9321/24T1/ass1/exchange_rates.html")
    df4 = question_4("country_codes.csv", 
                     "https://www.cse.unsw.edu.au/~cs9321/24T1/ass1/country_codes.html")

    # data exploration
    df5 = question_5(df1.copy(True))

    # data manipulation
    df6 = question_6(df1.copy(True))
    df7 = question_7(df6.copy(True), df4.copy(True))
    df8 = question_8(df7.copy(True), df3.copy(True))
    df9 = question_9(df2.copy(True))
    df10 = question_10(df8.copy(True), df9.copy(True))
    df11 = question_11(df10.copy(True))

    # data visualisation
    question_12(df10.copy(True))
