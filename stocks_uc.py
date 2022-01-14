# libraries
import os
import pandas as pd

# main
if __name__ == '__main__':

    print('Initiating.')

    # file location of CSV and it's fields 
    # (UC > 1.04 and UC < 1.25)
    file_loc = 'resources\stocks_uc.csv'
    fields = ['date', 'symbol', 'marketcapname', 'sector']

    # check if the file exists
    print('Check if the file exists at: ' + file_loc)
    if not os.path.exists(file_loc):
        print('File does not exist at path: ' + file_loc + '. Terminating.')
        exit(0)
    print('File found.')

    # read data from csv into panda dataframes
    try:
        # reading csv file
        df = pd.read_csv(file_loc, usecols=fields)
        print('CSV data read into dataframes.')
    except Exception as e:
        print('Error while reading data from CSV.' + e)

    # store the symbols into set
    unique_symbol = set(pd.Series(df.symbol))
    print(unique_symbol)

    print('Exit.')
