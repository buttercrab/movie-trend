import argparse
import json

import matplotlib.font_manager as fm
import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

# for korean font
path = 'font/NanumBarunpenRegular.ttf'
font = fm.FontProperties(fname=path, size=18)

parser = argparse.ArgumentParser()
parser.add_argument('--movie', type=str)
args = parser.parse_args()

if __name__ == '__main__':
	conf = json.loads(open('data/conf.json', 'r').readline())
	cnt = 0
	for movie in conf:
		if args.movie is None or args.movie == movie:
			cnt += 1
			print(str(cnt) + ': ' + movie)
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
				if time in audience:
					xdata.append(search[time])
					ydata.append(audience[time])

			if len(ydata) <= 1:
				continue


			def f(x, a, b):
				return a * x + b


			prop = curve_fit(f, np.array(xdata), np.array(ydata))
			a, b = prop[0][0], prop[0][1]

			x = np.linspace(0, 100, 1000)
			plt.scatter(xdata, ydata)
			plt.savefig('plot/' + movie + '.pdf')
			plt.clf()
