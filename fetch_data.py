import argparse
import json
import urllib.parse
from datetime import datetime
from datetime import timedelta
from urllib.request import urlopen

import requests
from bs4 import BeautifulSoup

secret_key = ''
conf = json.loads(open('data/conf.json', 'r').readline())

parser = argparse.ArgumentParser()
parser.add_argument('--movie', type=str)
args = parser.parse_args()


def make_date(d: datetime):
	return "%04d-%02d-%02d" % (d.year, d.month, d.day)


def fetch_api_key():
	global secret_key
	if secret_key == '':
		secret = open('secret/secret.txt', 'r')
		secret_key = secret.readline()
	return secret_key


def save_conf():
	global conf
	conf_file = open('data/conf.json', 'w')
	conf_file.write(json.dumps(conf, ensure_ascii=False))


if __name__ == '__main__':
	fetch_api_key()
	movies = []

	if args.movie is None:
		html = urlopen('https://movie.naver.com/movie/sdb/rank/rmovie.nhn')
		bs_object = BeautifulSoup(html, 'html.parser')

		for item in bs_object.select('.tit3'):
			movies.append(str(item.find_all('a')[0].text))
	else:
		movies.append(args.movie)

	cnt = 0
	for movie in movies:
		cnt += 1
		print(str(cnt) + ': downloading movie "' + movie + '"')
		try:
			encoded = urllib.parse.quote(movie)
			html = urlopen('http://www.kobis.or.kr/kobis/business/mast/mvie/searchMovieList.do?sMovName=' + encoded)
			bs_object = BeautifulSoup(html, 'html.parser')
			code = str(bs_object.select('.tac')[0].find_all('span')[0].text).strip()

			encoded = urllib.parse.quote(movie + ' 개봉일')
			html = urlopen('https://search.naver.com/search.naver?query=' + encoded)
			bs_object = BeautifulSoup(html, 'html.parser')
			date = str(bs_object.select('.property')[0].text).split()[0][:-1].replace('.', '-')

			html = urlopen(
				'http://www.kobis.or.kr/kobis/business/mast/mvie/searchMovieDtlXls.do?sType=box&code=' + code)
			bs_object = BeautifulSoup(html, 'html.parser')

			flag = False
			audience_data = []
			for item in bs_object.select('tbody')[0].find_all('tr'):
				cur_date = str(item.find_all('td')[0].text)
				if cur_date == date:
					flag = True

				if flag:
					audience_data.append({
						'time': cur_date,
						'data': int(str(item.find_all('td')[10].text).replace(',', ''))
					})

			body = {
				'startDate': make_date(datetime.strptime(date, '%Y-%m-%d') - timedelta(days=10)),
				'endDate': make_date(
					min(datetime.now() - timedelta(days=1), datetime.strptime(date, '%Y-%m-%d') + timedelta(days=60))),
				'timeUnit': 'date',
				'keywordGroups': [
					{
						'groupName': movie,
						'keywords': [
							movie,
						]
					},
				]
			}

			headers = {
				'X-Naver-Client-Id': '1vwchK27lb2hC4W3Cufh',
				'X-Naver-Client-Secret': secret_key,
				'Content-Type': 'application/json'
			}

			res = requests.post('https://openapi.naver.com/v1/datalab/search', data=json.dumps(body), headers=headers)
			search_data = []

			for i in res.json()['results'][0]['data']:
				search_data.append({
					'time': i['period'],
					'data': i['ratio']
				})
		except:
			cnt -= 1
			continue

		file = open('data/' + movie + '.json', 'w+')
		file.write(json.dumps({
			'audience_data': audience_data,
			'search_data': search_data
		}))
		file.close()
		conf[movie] = date
		save_conf()

	print('downloaded ' + str(cnt) + ' movie data, ' + str(len(movies) - cnt) + ' failed')
