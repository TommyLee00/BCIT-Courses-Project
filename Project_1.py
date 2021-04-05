#This application allows users to examine daily and cumulative changes to closing price and volume for stocks in the stock market.  
#The application prompts the user to either examine a stock or terminate the application.
import pandas_datareader as pdr
import datetime
import pandas as pd
pd.options.mode.chained_assignment = None
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

def getStock(stk,days):
    dt = datetime.date.today()
    dtPast = dt + datetime.timedelta(days=-days)
    df = pdr.get_data_yahoo(stk, start=datetime.datetime(dtPast.year, dtPast.month, dtPast.day),
                            end=datetime.datetime(dt.year, dt.month, dt.day))
    newdf = df[['Close', 'Volume']]
    newdf['Volume % Change'] = 0.0
    volPercentChange_IDX = 2
    for i in range(0, len(newdf)):
        volume = newdf.iloc[i]['Volume']
        previousVolume = newdf.iloc[i - 1]['Volume']
        newdf.iat[i, volPercentChange_IDX] = round((volume - previousVolume) / previousVolume, 4)
        newdf.iat[0, volPercentChange_IDX] = 0

    newdf['Close % Change'] = 0.0
    closePercentChange_IDX = 3
    for i in range(0, len(newdf)):
        close = newdf.iloc[i]['Close']
        previousClose = newdf.iloc[i - 1]['Close']
        newdf.iat[i, closePercentChange_IDX] = round((close - previousClose) / previousClose, 4)
        newdf.iat[0, closePercentChange_IDX] = 0
    return newdf

def start():
    print("-------------------------------------------------")
    print("Stock Report Menu Options")
    print("-------------------------------------------------")
    print("1. Report changes for a stock")
    print("2. Quit")
    answer = int(input())
    if answer == 1:
        print("Please enter the stock symbol: ")
        stockAnswer=input()
        print("Please enter the number of days for the analysis: ")
        numDayAnswer=int(input())
        dateToday= datetime.date.today()
        datePast = dateToday + datetime.timedelta(days=-numDayAnswer)
        print("************************************************************")
        print("Daily Percent Changes - " + str(datePast) + " to " + str(dateToday)+ " * " + stockAnswer.upper() + " * ")
        print("************************************************************")
        dfStock = getStock(stockAnswer,numDayAnswer)
        print(dfStock)
        print("------------------------------------------------------------")
        print("Summary of Cumulative Changes for " + stockAnswer)
        print("------------------------------------------------------------")
        print(str(datePast) + " to " + str(dateToday))

        numRows = len(dfStock)
        periodEndClose = dfStock.iloc[numRows-1]['Close']
        periodStartClose = dfStock.iloc[0]['Close']
        periodEndVolume = dfStock.iloc[numRows-1]['Volume']
        periodStartVolume = dfStock.iloc[0]['Volume']
        periodClosePercentChange = round((periodEndClose-periodStartClose)/periodStartClose,3)
        periodVolumePercentChange = round((periodEndVolume-periodStartVolume)/periodStartVolume,3)
        print("% Volume Change:  " + str(periodVolumePercentChange))
        print("% Close Price Change:  " + str(periodClosePercentChange))
        start()
    else:
        print("The Program has been terminated.")

start()
