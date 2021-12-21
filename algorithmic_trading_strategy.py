import pandas as pd
import numpy as np
import yfinance as yf
import math
import matplotlib.pyplot as plt
from pprint import pprint


def fint(x):
    if x > 100:
        return int(x)
    else:
        return x


def ema(ema_n, param_str):  # ema - exponential moving average - recursive sum with weight coefficients

    ema_k = 2 / (ema_n + 1)

    ema_arr = []
    param = history[f'{param_str}']
    for i in range(len(history)):
        if i == 0:
            ema_arr.append(fint(param[i]))
        else:
            ema_arr.append(fint(ema_k * param[i] + (1 - ema_k) * ema_arr[i - 1]))

    history[f'Ema_{param_str}_{ema_n}'] = np.array(ema_arr)


def status(history):
    status = []
    bgpvo, delta_price = history['BGPVO'], history['delta_price']
    for i in range(len(bgpvo)):
        if (bgpvo[i] * delta_price[i] >= 0):
            status.append('BUY')
        else:
            status.append('SELL')
    history['status'] = status


def trade(history):
    cash_arr, stock_arr, total_arr = [], [], []
    cash = 10000  # let it be $10'000
    stock = 0
    total = 10000
    status = history['status']
    open = history['Open']
    for i in range(len(status)):
        if status[i] == 'BUY' and cash != 0:
            stock = (cash / open[i]) * (1 - broker_comission)
            cash = 0
        elif status[i] == 'SELL' and stock != 0:
            cash = (stock * open[i]) * (1 - broker_comission)
            stock = 0
        cash_arr.append(cash)
        stock_arr.append(stock)
        total_arr.append(cash_arr[i] + stock_arr[i] * open[i])

    history['return'] = total_arr
    history['return'] = (history['return'] / 100) - 100  # in %


broker_comission = 0.00025  # 0.025% in TinkoffBank with trader status
start_date = '2020-01-01'  # потому что первый год идет не в счет - он подготовительный
end_date = '2021-08-13'
ticker_arr = ['A', 'AAL', 'AAP', 'AAPL', 'ABBV', 'ABC', 'ABMD', 'ABT', 'ACN', 'ADBE', 'ADI', 'ADM', 'ADP', 'ADSK',
              'AEE', 'AEP', 'AES', 'AFL', 'AIG', 'AIZ', 'AJG', 'AKAM', 'ALB', 'ALGN', 'ALK', 'ALL', 'ALLE', 'AMAT',
              'AMCR', 'AMD', 'AME', 'AMGN', 'AMP', 'AMT', 'AMZN', 'ANET', 'ANSS', 'ANTM', 'AON', 'AOS', 'APA', 'APD',
              'APH', 'APTV', 'ARE', 'ATO', 'ATVI', 'AVB', 'AVGO', 'AVY', 'AWK', 'AXP', 'AZO', 'BA', 'BAC', 'BAX',
              'BBWI', 'BBY', 'BDX', 'BEN', 'BF.B', 'BIIB', 'BIO', 'BK', 'BKNG', 'BKR', 'BLK', 'BLL', 'BMY', 'BR', 'BRK',
              'BSX', 'BWA', 'BXP', 'C', 'CAG', 'CAH', 'CAT', 'CB', 'CBRE', 'CCI', 'CCL', 'CDNS', 'CDW', 'CE',
              'CERN', 'CF', 'CFG', 'CHD', 'CHRW', 'CHTR', 'CI', 'CINF', 'CL', 'CLX', 'CMA', 'CMCS', 'CME', 'CMG', 'CMI',
              'CMS', 'CNC', 'CNP', 'COF', 'COG', 'COO', 'COP', 'COST', 'CPB', 'CPRT', 'CRL', 'CRM', 'CSCO', 'CSX',
              'CTAS', 'CTLT', 'CTSH', 'CTVA', 'CTXS', 'CVS', 'CVX', 'CZR', 'D', 'DAL', 'DD', 'DE', 'DFS', 'DG', 'DGX',
              'DHI', 'DHR', 'DIS', 'DISC', 'DISH', 'DLR', 'DLTR', 'DOV', 'DOW', 'DPZ', 'DRE', 'DRI', 'DTE', 'DUK',
              'DVA', 'DVN', 'DXC', 'DXCM', 'EA', 'EBAY', 'ECL', 'ED', 'EFX', 'EIX', 'EL', 'EMN', 'EMR', 'ENPH', 'EOG',
              'EQIX', 'EQR', 'ES', 'ESS', 'ETN', 'ETR', 'ETSY', 'EVRG', 'EW', 'EXC', 'EXPD', 'EXPE', 'EXR', 'F', 'FANG',
              'FAST', 'FB', 'FBHS', 'FCX', 'FDX', 'FE', 'FFIV', 'FIS', 'FISV', 'FITB', 'FLT', 'FMC', 'FOX', 'FOXA',
              'FRC', 'FRT', 'FTNT', 'FTV', 'GD', 'GE', 'GILD', 'GIS', 'GL', 'GLW', 'GM', 'GNRC', 'GOOG', 'GPC', 'GPN',
              'GPS', 'GRMN', 'GS', 'GWW', 'HAL', 'HAS', 'HBAN', 'HBI', 'HCA', 'HD', 'HES', 'HIG', 'HII', 'HLT', 'HOLX',
              'HON', 'HPE', 'HPQ', 'HRL', 'HSIC', 'HST', 'HSY', 'HUM', 'HWM', 'IBM', 'ICE', 'IDXX', 'IEX', 'IFF',
              'ILMN', 'INCY', 'INFO', 'INTC', 'INTU', 'IP', 'IPG', 'IPGP', 'IQV', 'IR', 'IRM', 'ISRG', 'IT', 'ITW',
              'IVZ', 'J', 'JBHT', 'JCI', 'JKHY', 'JNJ', 'JNPR', 'JPM', 'K', 'KEY', 'KEYS', 'KHC', 'KIM', 'KLAC', 'KMB',
              'KMI', 'KMX', 'KO', 'KR', 'KSU', 'L', 'LDOS', 'LEG', 'LEN', 'LH', 'LHX', 'LIN', 'LKQ', 'LLY', 'LMT',
              'LNC', 'LNT', 'LOW', 'LRCX', 'LUMN', 'LUV', 'LVS', 'LW', 'LYB', 'LYV', 'MA', 'MAA', 'MAR', 'MAS', 'MCD',
              'MCHP', 'MCK', 'MCO', 'MDLZ', 'MDT', 'MET', 'MGM', 'MHK', 'MKC', 'MKTX', 'MLM', 'MMC', 'MMM', 'MNST',
              'MO', 'MOS', 'MPC', 'MPWR', 'MRK', 'MRNA', 'MRO', 'MS', 'MSCI', 'MSFT', 'MSI', 'MTB', 'MTD', 'MU', 'MXIM',
              'NCLH', 'NDAQ', 'NEE', 'NEM', 'NFLX', 'NI', 'NKE', 'NLOK', 'NLSN', 'NOC', 'NOV', 'NOW', 'NRG', 'NSC',
              'NTAP', 'NTRS', 'NUE', 'NVDA', 'NVR', 'NWL', 'NWS', 'NWSA', 'NXPI', 'O', 'ODFL', 'OKE', 'OMC',
              'ORCL', 'ORLY', 'OXY', 'PAYC', 'PAYX', 'PBCT', 'PCAR', 'PEAK', 'PEG', 'PENN', 'PEP', 'PFE', 'PFG',
              'PG', 'PGR', 'PH', 'PHM', 'PKG', 'PKI', 'PLD', 'PM', 'PNC', 'PNR', 'PNW', 'POOL', 'PPG', 'PPL', 'PRGO',
              'PRU', 'PSA', 'PSX', 'PTC', 'PVH', 'PWR', 'PXD', 'PYPL', 'QCOM', 'QRVO', 'RCL', 'RE', 'REG', 'REGN', 'RF',
              'RHI', 'RJF', 'RL', 'RMD', 'ROK', 'ROL', 'ROP', 'ROST', 'RSG', 'RTX', 'SBAC', 'SBUX', 'SCHW', 'SEE',
              'SHW', 'SIVB', 'SJM', 'SLB', 'SNA', 'SNPS', 'SO', 'SPG', 'SPGI', 'SRE', 'STE', 'STT', 'STX', 'STZ', 'SWK',
              'SWKS', 'SYF', 'SYK', 'SYY', 'T', 'TAP', 'TDG', 'TDY', 'TEL', 'TER', 'TFC', 'TFX', 'TGT', 'TJX', 'TMO',
              'TMUS', 'TPR', 'TRMB', 'TROW', 'TRV', 'TSCO', 'TSLA', 'TSN', 'TT', 'TTWO', 'TWTR', 'TXN', 'TXT', 'TYL',
              'UA', 'UAA', 'UAL', 'UDR', 'UHS', 'ULTA', 'UNH', 'UNM', 'UNP', 'UPS', 'URI', 'USB', 'V', 'VFC', 'VIAC',
              'VLO', 'VMC', 'VNO', 'VRSK', 'VRSN', 'VRTX', 'VTR', 'VTRS', 'VZ', 'WAB', 'WAT', 'WBA', 'WDC', 'WEC',
              'WELL', 'WFC', 'WHR', 'WLTW', 'WM', 'WMB', 'WMT', 'WRB', 'WRK', 'WST', 'WU', 'WY', 'WYNN', 'XEL', 'XLNX',
              'XOM', 'XRAY', 'XYL', 'YUM', 'ZBH', 'ZBRA', 'ZION', 'ZTS']

final_results = dict()
for ticker in ticker_arr:

    obj = yf.Ticker(ticker)
    history = obj.history(start=start_date, end=end_date, interval='1d')  # pandas df

    ema(9, 'Volume')
    ema(12, 'Volume')
    ema(26, 'Volume')

    ema(9, 'Open')
    ema(12, 'Open')
    ema(26, 'Open')

    # PVO - percentage volume oscillator

    history['PVO'] = (history['Ema_Volume_12'] / history['Ema_Volume_26'] - 1).shift(periods=1, fill_value=0)
    ema(9, 'PVO')  # now history['Ema_PVO_9'] is our Signal line

    history['BGPVO'] = history['PVO'] - history[
        'Ema_PVO_9']  # BGPVO - bar graph of PVO. This is key parameter we will decide what to do
    history['delta_price'] = history['Open'] - (
            (5 / 9) * history['Ema_Open_9'] + (3 / 9) * history['Ema_Open_12'] + (1 / 9) * history['Ema_Open_26'])
    status(history)
    trade(history)

    results = dict()  # sr - Sharp Ratio, cr - Calmar ratio - https://www.investopedia.com/terms/c/calmarratio.asp

    # sr

    years = int(end_date[:4]) - int(start_date[:4]) + (int(end_date[5:7]) - int(start_date[5:7])) / 12 + (
            int(end_date[8:]) - int(start_date[8:])) / 365
    total = (history['return'] + 100) * 100
    try:
        stock_annual_return = (math.log(total[-1] / total[0]) / math.log(years)) * 100 - 100  # %
    except IndexError:
        continue
    risk_free_annual_return = 15  # %

    average_return = (history['Close'][365:] / history['Close'].shift(365)[365:]).mean() * 100 - 100
    standart_deviation = (np.square(((history['Close'][365:] / history['Close'].shift(365)[
                                                               365:]) * 100 - 100 - average_return)).to_numpy()).mean() ** (
                             0.5)

    results['Sharp ratio'] = (stock_annual_return - risk_free_annual_return) / standart_deviation

    # cr We assume it's mean by years

    calmar_numerator = (history['Close'][365:] - history['Close'].shift(365)[365:]) / history['Close'].shift(365)[365:]
    calmar_denominator = (history['Close'].rolling(365).min()[365:] - history['Close'].shift(365)[365:]).abs() / \
                         history['Close'].shift(365)[365:]
    results['Calmar ratio'] = (calmar_numerator / calmar_denominator).median()

    final_results[ticker] = results

# printing out most successful stocks
# counting results

print(final_results)
