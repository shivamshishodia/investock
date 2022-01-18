# libraries
import os
import pandas as pd

from datetime import date, timedelta

# main
if __name__ == '__main__':

    print('Initiating.')

    # file location of CSV and it's fields.
    # (UC > 1.04 and UC < 1.25).
    file_loc = 'resources\stocks_uc.csv'
    fields = ['date', 'symbol', 'marketcapname', 'sector']

    # check if the file exists.
    print('Check if the file exists at: ' + file_loc)
    if not os.path.exists(file_loc):
        print('File does not exist at path: ' + file_loc + '. Terminating.')
        exit(0)
    print('File found.')

    # read data from csv into panda dataframes.
    try:
        # reading csv file.
        df = pd.read_csv(file_loc, usecols=fields)
        print('CSV data read into dataframes.')
    except Exception as e:
        print('Error while reading data from CSV.' + e)

    # pick only those entries which are no more than `past_n_days` days in past.
    todays_date = date.today() # datetime64 format (2022-01-18).
    past_n_days = int(input('Enter the past `n` days for which you want to filter the data for: '))
    past_n_date = (todays_date - timedelta(days=past_n_days))

    # Convert the `date` column in dataframe into datetime64 format.
    df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y').dt.date

    # filter the records based on `past_n_days`.
    filtered_df = df.loc[(df['date'] >= past_n_date) & (df['date'] <= todays_date)]

    # fetch unique symbols and store the list of dates against them similiar to hashed table.
    symbol_dict = {}
    for index, row in filtered_df.iterrows():
        # add the symbol if it does not exist.
        if symbol_dict.get(row['symbol']) is None:
            symbol_dict[row['symbol']] = []
        symbol_dict[row['symbol']].append(row['date'])

    # show the hashed table in the form of grid.
    min_ucs = int(input('Enter the minimum number of UCs for selection: '))
    for symbol, date_list in symbol_dict.items():
        # omit if the symbol has less than `min_ucs`.
        if len(date_list) <= min_ucs:
            continue
        # to add apt. padding for the grid.
        print((symbol + '\t') if (len(symbol) < 8) else symbol, end='\t')
        for date in date_list:
            # print(date.strftime('%m/%d'), end=' ')
            print('*', end=' ')
        print(end='\n')

    print('Exit.')
