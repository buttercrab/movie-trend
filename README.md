# Movie Trend

This is movie audience count predictor for South Korea.
It fetches real audience data from [kobis](http://www.kobis.or.kr/kobis/business/main/main.do) and naver search data from [naver datalab](https://datalab.naver.com/)

## Use yourself

1. get api key from naver datalab
1. make `secret/secret.txt` and put naver datalab secret key
1. change user key from `fetch_data.py`
1. make `data/conf.json`
1. run `fetch_data.py`

In terminal:

```shell script
mkdir -p secret data
echo "YOUR_SECRET_KEY" >> secret/secret.txt
echo "{}" >> data/conf.json
python3 fetch_data.py
```

## Use more further

Fetch data and view data by timeline and find fitting and r-squared value

```shell script
mkdir -p figure plot
# download data that you want to download
python3 fetch_data.py
python3 view_data.py
python3 find_fit.py
```

### Download your favorite movie

If it fails then check if movie came out after 2016

```shell script
python3 fetch_data.py --movie "MOVIE_NAME"
python3 view_data.py --movie "MOVIE_NAME"
python3 find_fit.py --movie "MOVIE_NAME"
```

## License

```
MIT License

Copyright (c) 2019 Jaeyong Sung

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```