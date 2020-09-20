import finance as f
import sys
import matplotlib.pyplot as plt

LAST_PERIODS = -365

SHORT = 15
LONG = 50

STARTING_NAV = 10000

def get_moving_average(ticker, length):

	daily_data = f.get_daily_time_series(ticker)

	close_prices = f.get_list_close_prices(daily_data)
	close_prices = close_prices[::-1]

	average_list = list()

	for i in range(length, len(close_prices)):

		total = sum(close_prices[(i-length+1):i+1])
		average = total / length
		average_list.append(average)

	return close_prices[LAST_PERIODS:], average_list[LAST_PERIODS:]

def moving_average_crossover(ticker):

	close_prices, ten_day = get_moving_average(ticker, SHORT)
	close_prices, fifty_day = get_moving_average(ticker, LONG)

	holding = False

	total_profit = 0

	entry_points = list()
	closing_points = list()

	NAV = STARTING_NAV

	print("Starting with $", NAV, ".")

	for i in range(len(fifty_day)):

		if not holding and ten_day[i] >= fifty_day[i]:

			if close_prices[i] > NAV:
				continue

			print('entering at ', close_prices[i])
			entry_points.append(i)
			holding = True
			enter_price = close_prices[i]

			stocks_held = NAV // enter_price

		elif holding and ten_day[i] < fifty_day[i]:

			print('closing at ', close_prices[i])

			holding = False
			ending_price = close_prices[i]

			print("Profit is ", (stocks_held * ending_price) - (stocks_held * enter_price))

			closing_points.append(i)

			NAV += (stocks_held * ending_price) - (stocks_held * enter_price)

	if holding:

		print('closing at ', close_prices[i])

		holding = False
		ending_price = close_prices[i]

		print("Profit is ", (stocks_held * ending_price) - (stocks_held * enter_price))

		closing_points.append(i)

		NAV += (stocks_held * ending_price) - (stocks_held * enter_price)

	ten_MA = plt.plot(ten_day, label=str(SHORT) + ' Day MA')
	fifty_MA = plt.plot(fifty_day, label=str(LONG) + ' Day MA')
	close_plt = plt.plot(close_prices, label='Closing Prices')
	plt.ylabel(ticker)
	plt.legend()

	for xc in entry_points:
		plt.axvline(x=xc, color='r', linestyle='--')
	for xc in closing_points:
		plt.axvline(x=xc, color='k', linestyle='--')

	print("Ending with $", NAV, ".")

	returns = (NAV - STARTING_NAV)/STARTING_NAV * 100
	returns_from_buy_and_hold = (close_prices[-1] - close_prices[0])/(close_prices[0]) * 100
	print("Made returns of %.4f%% using the strategy." % returns)
	print("Buying and holding would have returned %.4f%%" % returns_from_buy_and_hold)
	return 


ticker = sys.argv[1]
moving_average_crossover(ticker)
plt.show()


