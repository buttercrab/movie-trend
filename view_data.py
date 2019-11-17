import argparse
import json

import matplotlib.font_manager as fm
from matplotlib import pyplot as plt

# for korean font
path = 'font/NanumBarunpenRegular.ttf'
font = fm.FontProperties(fname=path, size=18)

parser = argparse.ArgumentParser()
parser.add_argument('--movie', type=str)
args = parser.parse_args()

if __name__ == '__main__':
	conf = json.loads(open('data/conf.json').readline())
	for movie in conf:
		if args.movie is None or args.movie == movie:
			data = json.loads(open('data/' + movie + '.json').readline())
			audience_data = data['audience_data']
			search_data = data['search_data']

			x, y = [], []
			for item in search_data:
				x.append(item['time'])
				y.append(item['data'])
			plt.plot(x, y)

			max_value = 0
			for item in audience_data:
				max_value = max(max_value, item['data'])

			x, y = [], []
			for item in audience_data:
				x.append(item['time'])
				y.append(float(item['data']) / max_value * 100)
			plt.plot(x, y)

			plt.xticks(rotation=90)

			plt.title(movie, fontproperties=font)
			plt.show()
