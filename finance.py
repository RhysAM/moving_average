import json
import urllib.request
import matplotlib.pyplot as plt
from scipy import stats

import numpy as np
import sys

QUERY_URL = "https://www.alphavantage.co/query?function={REQUEST_TYPE}&apikey={KEY}&symbol={SYMBOL}&outputsize={SIZE}"
API_KEY = "ESTNBW8NL54H99JS"

def _request(symbol, req_type, full=False):

	if full:
		size = "full"
	else:
		size = "compact"

	with urllib.request.urlopen(QUERY_URL.format(REQUEST_TYPE=req_type, KEY=API_KEY, SYMBOL=symbol, SIZE=size)) as req:
		data = req.read().decode("UTF-8")

	return data

def get_daily_data(symbol):
    return json.loads(_request(symbol, 'TIME_SERIES_DAILY_ADJUSTED'))

def get_full_daily_data(symbol):
	return json.loads(_request(symbol, 'TIME_SERIES_DAILY_ADJUSTED', full=True))

def get_daily_time_series(symbol):
	return get_full_daily_data(symbol)["Time Series (Daily)"]

def get_list_close_prices(daily_data):

	daily_list = list()

	for day in daily_data.values():

		daily_list.append(day["4. close"])

	return np.array(daily_list).astype(np.float)

def hedge_ratio(first_symbol, second_symbol):

	first_daily_data = get_daily_data(first_symbol)["Time Series (Daily)"]
	second_daily_data = get_daily_data(second_symbol)["Time Series (Daily)"]

	x = get_list_close_prices(first_daily_data)
	y = get_list_close_prices(second_daily_data)


	slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
	print("slope: %f    intercept: %f" % (slope, intercept))

	plt.plot(x, y, 'o', label='original data')
	plt.plot(x, intercept + slope*x, 'r', label='fitted line')
	plt.xlabel(first_symbol)
	plt.ylabel(second_symbol)
	plt.legend()
	plt.show()

	print("r-squared: %f" % r_value**2)

	return 1/slope

if (__name__ == "__main__"):

	first_symbol = sys.argv[1]
	second_symbol = sys.argv[2]

	hedge_ratio = hedge_ratio(first_symbol, second_symbol)

	print("You should buy " + str(hedge_ratio) + " stocks of " 
		+ second_symbol + " for every 1 stock of " + first_symbol)
