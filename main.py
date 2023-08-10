import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

tesla = pd.read_csv('TESLA Search Trend vs Price.csv')
bitcoin_search = pd.read_csv('Bitcoin Search Trend.csv')
bitcoin_price = pd.read_csv('Daily Bitcoin Price.csv')
benefits_19 = pd.read_csv('UE Benefits Search vs UE Rate 2004-19.csv')
benefits_20 = pd.read_csv('UE Benefits Search vs UE Rate 2004-20.csv')

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
benefits_19.MONTH = pd.to_datetime(benefits_19.MONTH)
benefits_20.MONTH = pd.to_datetime(benefits_20.MONTH)


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

plt.figure(figsize=(14, 8), dpi=120)
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

# [7] BTC chart
plt.figure(figsize=(14, 8), dpi=120)
plt.title('Bitcoin News Search vs Resampled Price')
plt.xticks(fontsize=14, rotation=45)

ax1 = plt.gca()
ax2 = ax1.twinx()

ax1.set_ylabel('BRC Price', color='#F08F2E', fontsize=14)
ax2.set_ylabel('Seatch Trend', color='skyblue', fontsize=14)

ax1.xaxis.set_major_locator(years)
ax1.xaxis.set_major_formatter(years_fmt)
ax1.xaxis.set_minor_locator(months)

# proveri ovo
ax1.set_ylim(bottom=0, top=15000)
ax1.set_xlim([bitcoin_price_monthly.index.min(), bitcoin_price_monthly.index.max()])

# different linestyles and markers
ax1.plot(bitcoin_price_monthly.index, bitcoin_price_monthly.CLOSE, color='#F08F2E', linewidth=3, linestyle='--')
ax2.plot(bitcoin_price_monthly.index, bitcoin_search.BTC_NEWS_SEARCH, color='skyblue', linewidth=3, marker='o')

plt.show()

# [8] Unemployment chart
plt.figure(figsize=(14, 8), dpi=120)
plt.title('Monthly Search of "Unemployment Benefits" in the U.S. vs the U/E Rate', fontsize=18)
plt.yticks(fontsize=14)
plt.xticks(fontsize=14, rotation=45)

ax1 = plt.gca()
ax2 = ax1.twinx()

ax1.set_ylabel('FRED U/E Rate', color='purple', fontsize=14)
ax2.set_ylabel('Search Trend', color='skyblue', fontsize=14)

ax1.xaxis.set_major_locator(years)
ax1.xaxis.set_major_formatter(years_fmt)
ax1.xaxis.set_minor_locator(months)

ax1.set_ylim(bottom=3, top=10.5)
ax1.set_xlim(benefits_19.MONTH.min(), benefits_19.MONTH.max())

# show the grid lines as dark grey lines
ax1.grid(color='grey', linestyle='--')

# calculate the rolling average over a 6 month window
roll_df = benefits_19[['UE_BENEFITS_WEB_SEARCH', 'UNRATE']].rolling(window=6).mean()
# set up the dataset
ax1.plot(benefits_19.MONTH, roll_df.UNRATE, 'purple', linewidth=3, linestyle='--')
ax2.plot(benefits_19.MONTH, roll_df.UE_BENEFITS_WEB_SEARCH, 'skyblue', linewidth=3)

plt.show()

plt.figure(figsize=(14, 8), dpi=120)
plt.yticks(fontsize=14)
plt.xticks(fontsize=14, rotation=45)
plt.title('Monthly US "Unemployment Benefits" Web Search vs UNRATE incl 2020', fontsize=18)

ax1 = plt.gca()
ax2 = ax1.twinx()

ax1.set_ylabel('FRED U/E Rate', color='purple', fontsize=16)
ax1.set_ylabel('Search Trend', color='skyblue', fontsize=16)

ax1.set_xlim([benefits_20.MONTH.min(), benefits_20.MONTH.max()])

ax1.plot(benefits_20.MONTH, benefits_20.UNRATE, 'purple', linewidth=3)
ax2.plot(benefits_20.MONTH, benefits_20.UE_BENEFITS_WEB_SEARCH, 'skyblue', linewidth=3)

plt.show()
