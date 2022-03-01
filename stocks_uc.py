# libraries
import os
import pandas as pd

from datetime import date, timedelta
from colorama import init, Fore, Style

# main
if __name__ == '__main__':

    print('Initiating.')
    init()

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

    # convert the `date` column in dataframe into datetime64 format.
    df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y').dt.date

    # filter the records based on `past_n_days`.
    filtered_df = df.loc[(df['date'] > past_n_date) & (df['date'] <= todays_date)]

    # prepare the date range to be filled for every ticker.
    date_range = [todays_date - timedelta(days=x) for x in range(past_n_days)]
    date_range = sorted(date_range)

    # prepare dict for each ticker to store 1 UC, -1 no UC and 0 holiday.
    date_uc_tracker = {}
    for ele in date_range:
        # all values filled with -1 (UC not hit) initially.
        # holidays marked with 0.
        if ele.weekday() > 4:
            date_uc_tracker[ele] = 0
            continue
        date_uc_tracker[ele] = -1 

    # fetch individual tickers.
    tickers = []
    for index, row in filtered_df.iterrows():
        tickers.append(row['symbol'])
    tickers = list( dict.fromkeys(tickers) )

    # attach date UC tracker with each ticker.
    # {
    #     "TCIEXP": { datetime.date(2022, 2, 26): -1, datetime.date(2022, 2, 27): -1, datetime.date(2022, 2, 28): -1}, 
    #     "FELDVR": { datetime.date(2022, 2, 26): -1, datetime.date(2022, 2, 27): -1, datetime.date(2022, 2, 28): -1}
    #      ......
    # }
    symbol_dict = {}
    for ticker in tickers:
        symbol_dict[ticker] = date_uc_tracker.copy()

    # fetch unique symbols and store the list of dates against them similiar to hashed table.
    for index, row in filtered_df.iterrows():
        # mark if the UC was hit or not.
        try:
            symbol_dict[row['symbol']][row['date']] = 1
        except KeyError:
            pass

    # show the hashed table in the form of grid.
    min_ucs = int(input('Enter the minimum number of UCs for selection: '))
    for symbol, date_list in symbol_dict.items():
        # count the number of UCs.
        uc_count = sum(x == 1 for x in date_list.values())
        if uc_count >= min_ucs:
            # to add apt. padding for the grid.
            print((symbol + '\t') if (len(symbol) < 8) else symbol, end='\t')
            for dt, uc in date_list.items():
                # print(date.strftime('%m/%d'), end=' ')
                # + for UC and - for no UC.
                if uc == 1:
                    print(Fore.GREEN + '+', end=' ')
                elif uc == -1:
                    print(Fore.RED + '-', end=' ')
                else:
                    print(Fore.LIGHTBLACK_EX + '.', end=' ')
            print(Style.RESET_ALL, end='\n')

    print('Exit.')
