'''the feeders sends daily prices of Apple and Microsoft into the datastream'''

# f = open("keys.txt", "r")
# key = f.read()
# my_key = key
# # from keys import twelveDataKey as api_key
# from twelvedata import TDClient
# td = TDClient(apikey = my_key)

import pandas as pd
import time, sys
import pathlib

# helper function that grabs data from api. Outputs datda as a pandas df
# def get_data(sym, start, end):
#     ts = td.time_series(
#          symbol=sym,
#          interval="1day" ,
#          start_date=start, 
#          end_date=end,
#          type = "Common Stock",
#          outputsize = 5000

#     ).as_pandas()
#     return ts

# reading data from twelvedata api as dataframes. For some reason the datetime column is ommitted in the df created, and so I had to save that df to a csv first then re-read it as a df.
# aapl = get_data('AAPL','2020-10-31','2024-10-31').to_csv('aapl.csv',encoding = 'utf-8')
# msft = get_data('MSFT','2020-10-31','2024-10-31').to_csv('msft.csv',encoding = 'utf-8')
aapl = pd.read_csv('aapl.csv')
msft = pd.read_csv('msft.csv')
aapl['Symbol'] = 'AAPL'
msft['Symbol'] = 'MSFT'

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
# print (sys.path, file=sys.stderr)

dates = aapl['datetime']
init_date = list(dates)[-1]
last_hist_date = list(dates)[0]

init_delay_seconds = 30
interval = 1

# scaling the data in the two dataframes
scaler = aapl.loc[aapl['datetime'] == init_date, 'close'].values[0]/msft.loc[msft['datetime'] == init_date, 'close'].values[0]
closing  = msft['close']
msft['close'] = closing*scaler
all_stock = pd.merge(aapl, msft, on='datetime')
all_stock.to_csv('all.csv',encoding='utf-8')
if __name__ == '__main__':
    print ('Sending daily AAPL and MSFT prices from %10s to %10s ...' % (str(init_date)[:10], str(last_hist_date)[:10]), flush=True, file=sys.stderr)
    print ("... each day's data sent every %d seconds ..." % (interval), flush=True, file=sys.stderr)
    print ('... beginning in %02d seconds ...' % (init_delay_seconds), flush=True, file=sys.stderr)
    print ("... MSFT prices adjusted to match GOOG prices on %10s ..."  % (init_date), flush=True, file=sys.stderr)

    from tqdm import tqdm
    for left in tqdm(range(init_delay_seconds)):
        time.sleep(0.5)
    updated_dates = all_stock['datetime']
    for date in list(updated_dates):     
        # format: date, aapl closing price, msft closing price
        print ('%10s\t%.4f\t%.4f' % (str(date)[:10], all_stock.loc[all_stock['datetime'] == date, 'close_x'].values[0], all_stock.loc[all_stock['datetime'] == date, 'close_y'].values[0]), flush=True)
        time.sleep(float(interval))

    exit(0)

# Real Time Prices
# Eventually we want to make it a day trading platform in the spirit of 
# https://www.investopedia.com/articles/trading/05/011705.asp
# !pip install yahoo_fin
# import datetime, time
# from yahoo_fin import stock_info

# for t in range(10):
#     now = datetime.datetime.now()
#     goog_price = stock_info.get_live_price('GOOG')
#     msft_price = stock_info.get_live_price('MSFT')
#     print ('%10s\t%.4f\t%.4f' % (str(now)[:19], goog_price, msft_price))
#     time.sleep(5.0)

# exit(0)
