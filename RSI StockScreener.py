# define parametetrs here

candle_width = "5m"
adx_limit = 20
rsi_limit = 40
stock_price_limit = 20
step_5_flag = 0

rsi_type = "rsi_6"


import pandas as pd
import yfinance as yf
import datetime
from stockstats import StockDataFrame

# stocklist = ['MTSL', 'LPCN', 'CLRB', 'TMQ']
#stocklist = ['MIST' ,  'ABUS' ,  'RNET' ,  'BCOV' ,  'MOGO' ,  'HLX' ,  'REED' ,  'CBAY' ,  'XSPA', 'TMQ' ,  'TNXP' ,  'TUP' ,  'OMI' ,  'SALM' ,  'YVR' ,  'ENTX' ,  'AMAG' ,  'GNCA' ,  'AIKI' ,  'PRTY' ,  'PEIX' ,  'UMC' ,  'MYOS' ,  'CNTG' ,  'PLG' ,  'CLSN' ,  'SINT' ,  'MITO' ,  'FI' ,  'CPSH' ,  'IMRN' ,  'EQT' ]
def createList():
	df = pd.read_csv("stocks_list_07232020_fromIB2.csv")
	stock_list = df['Financial Instrument'].values
	return list(stock_list)
stocklist = createList()


Final_List = []

pd.core.common.is_list_like = pd.api.types.is_list_like


for stock in stocklist:
    data = pd.DataFrame(columns=stocklist)

    start_date = datetime.datetime.now() - datetime.timedelta(days=5)
    end_date = datetime.date.today()
    # start_date = datetime.date(2020,6,23)
    #end_date = "2020-06-23"
    
    data = yf.download(stock,interval = candle_width ,start=start_date, end=end_date)
    data.fillna(method='bfill', inplace=True)
    data.fillna(method='ffill', inplace=True)
    my_stock = StockDataFrame.retype(data)

    # UnComment down lines for evaluation
    # print(data)
    # print(my_stock['adx'])
    # print(my_stock[rsi_type])

    print("\n\n",stock)
    if my_stock['adx'][-1] > adx_limit:
        print("greater than adx_limit")
        if my_stock['adx'][-1] > my_stock['adx'][-2] > my_stock['adx'][-3] > my_stock['adx'][-4]:
            print("increasing adx")
            if my_stock[rsi_type][-1] > rsi_limit:
                print( "rsi greater than rsi_limit")
                proceed = 1
                if step_5_flag == 1:
                    print("step 5 executed")
                    if my_stock[rsi_type][-1] > my_stock[rsi_type][-2] > my_stock[rsi_type][-3] > my_stock[rsi_type][-4]:
                        print("Increasing RSI")
                    else:
                        proceed = 0
                if proceed == 1:
                    print("adding to list with adx ", my_stock["adx"][-1], stock)
                    Final_List.append({"name" : stock , "adx" : my_stock["adx"][-1]})



print("\n---------------\n\n")
df = pd.DataFrame(Final_List)
try:
    df = df.sort_values(by=['adx'], ascending= False)
    print(df)

    df = df.iloc[0:11,:]

except:
    print("######################\nNO STOCK MEETING THE CRITERIA\n######################")
    pass

with open("Output_Stocks.txt", "w") as File:
    df.to_string(File, index = None)
    File.close()