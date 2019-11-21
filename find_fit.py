import argparse
import json
from datetime import datetime, timedelta

import matplotlib.font_manager as fm
import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit


def make_date(d: datetime):
	return "%04d-%02d-%02d" % (d.year, d.month, d.day)


# for korean font
path = 'font/NanumBarunpenRegular.ttf'
font = fm.FontProperties(fname=path, size=18)

parser = argparse.ArgumentParser()
parser.add_argument('--movie', type=str)
args = parser.parse_args()

if __name__ == '__main__':
	conf = json.loads(open('data/conf.json', 'r').readline())
	cnt = 0
	r_squares = []
	for movie in conf:
		if args.movie is None or args.movie == movie:
			data = json.loads(open('data/' + movie + '.json').readline())
			audience_data = data['audience_data']
			search_data = data['search_data']

			max_value = 0
			for item in audience_data:
				max_value = max(max_value, item['data'])

			audience = {}
			search = {}
			for item in search_data:
				search[item['time']] = item['data']

			for item in audience_data:
				audience[item['time']] = float(item['data']) / max_value * 100

			xdata, ydata = [], []
			for time in search:
				new_time = make_date(datetime.strptime(time, '%Y-%m-%d') - timedelta(days=0))
				if new_time in audience:
					xdata.append(search[time])
					ydata.append(audience[new_time])

			if len(ydata) <= 1:
				continue


			def f(x, a, b):
				return a * x + b


			xdata = np.array(xdata)
			ydata = np.array(ydata)
			prop = curve_fit(f, xdata, ydata)
			a, b = prop[0][0], prop[0][1]

			x = np.linspace(0, 100, 1000)

			ss_res = np.sum((ydata - f(xdata, a, b)) ** 2)
			ss_tot = np.sum((ydata - np.mean(ydata)) ** 2)
			r_squared = 1 - ss_res / ss_tot

			# if r_squared < 0.5:
			# 	continue

			r_squares.append(r_squared)

			plt.scatter(xdata, ydata)
			plt.plot(x, f(x, a, b))
			plt.title(movie, fontproperties=font)
			plt.savefig('plot/' + movie + '.pdf')
			plt.clf()

			cnt += 1
			print(str(cnt) + ': ' + movie + '  ' + str(r_squared))

	print('avg: ' + str(np.mean(np.array(r_squares))))
