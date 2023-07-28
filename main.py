import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

tesla = pd.read_csv('TESLA Search Trend vs Price.csv')
bitcoin_search = pd.read_csv('Bitcoin Search Trend.csv')
bitcoin_price = pd.read_csv('Daily Bitcoin Price.csv')
benefits = pd.read_csv('UE Benefits Search vs UE Rate 2004-20.csv')

# [1] describe the dataframes
# # get the max, min, mean values
# >>> print(f'The shape of TESLA dataframe: {tesla.shape}')
# >>> print(f'Maximum value in TESLA dataframe: {tesla.TSLA_USD_CLOSE.max()}')
# >>> print(f'Minimum value in TESLA dataframe: {tesla.TSLA_USD_CLOSE.min()}')
# >>> print(f'Average value in TESLA dataframe: {round(tesla.TSLA_USD_CLOSE.mean(),2)}')
# # another approach
# >>> print(tesla.describe())

# [2] missing values
# .isna() will return series of True and False
# chained with .values.any() will return True if any were True or False if all of them are False
# >>> print(tesla.isna().values.any())
# tesla, and both benefits trends don't have any missing values
# >>> print(bitcoin_price.isna().values.any())
# however, bitcoing_price df has some missing values
# to check how many, we will add .sum()
# >>> print(bitcoin_price.isna().values.sum())
# this prints: 2; let's drop them - use the inplace=True argument to not have to assign this to a variable
bitcoin_price.dropna(inplace=True)
# instead of bitcoin_price = bitcoin_price.dropna()

# [3] convert string date values into pandas timestamp
tesla.MONTH = pd.to_datetime(tesla.MONTH)
bitcoin_search.MONTH = pd.to_datetime(bitcoin_search.MONTH)
bitcoin_price.DATE = pd.to_datetime(bitcoin_price.DATE)
benefits.MONTH = pd.to_datetime(benefits.MONTH)


# [4] resample bitcoin_price daily data to monthly data
# .resample()
# resamples time series data - frequency conversion
# we only want the last BTC price for the month
bitcoin_price_monthly = bitcoin_price.resample('M', on='DATE').last()
# print(bitcoin_price_monthly.head())
#                  DATE       CLOSE      VOLUME
# DATE
# 2014-09-30 2014-09-30  386.944000  34707300.0
# 2014-10-31 2014-10-31  338.321014  12545400.0
# 2014-11-30 2014-11-30  378.046997   9194440.0
# 2014-12-31 2014-12-31  320.192993  13942900.0
# 2015-01-31 2015-01-31  217.464005  23348200.0
# >>> print(bitcoin_price_monthly.shape)
# (73, 3)

# [5] basic line chart with Tesla stock price and the search popularity
# [6] add time ticks (more precise X-axis values)
years = mdates.YearLocator()
months = mdates.MonthLocator()
years_fmt = mdates.DateFormatter('%Y')

plt.figure(figsize=(14,8), dpi=120)
plt.title('Tesla Web Search vs Price', fontsize=18)
plt.xticks(fontsize=14, rotation=45)

ax1 = plt.gca()
ax2 = ax1.twinx()

# format the ticks
ax1.xaxis.set_major_locator(years)
ax1.xaxis.set_major_formatter(years_fmt)
ax1.xaxis.set_minor_locator(months)

ax1.set_ylabel('TSLA Stock Price', color='#E6232E', fontsize=14)
ax2.set_ylabel('Search Trend', color='skyblue', fontsize=14)

# set the minimum and maximum values on the axes
ax1.set_ylim([0, 600])
ax1.set_xlim([tesla.MONTH.min(), tesla.MONTH.max()])

ax1.plot(tesla.MONTH, tesla.TSLA_USD_CLOSE, color='#E6232E', linewidth=3)
ax2.plot(tesla.MONTH, tesla.TSLA_WEB_SEARCH, color='skyblue', linewidth=3)

plt.show()
