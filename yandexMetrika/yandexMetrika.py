import json
import requests
import pandas as pd
import re

class yandexMetrika:
	"""
Class for get data from API into simple dataFrame or csv

Warning: there is no check is data sampled or not and also max num of recieved rows is 100k

Usage:
[1] a = yandexMetrika()
[2] a.set_token(Token="YOURTOKENHERE1234")
[3] a.get_data('123456', 'ym:s:visits,ym:s:ecommercePurchases',date1='2021-09-01', date2='yesterday', dimensions='ym:s:date', filters="ym:s:lastsignUTMMedium=~'cpc'")
a.data
	"""
	def __init__(self):
		pass
	
	def set_token(self, Token):
		"""
		yandexMetrika.set_token(Token)
		"""
		self.Token = Token
		self.__auth_headers__ = {"Authorization" : ("OAuth "+ self.Token)}

	def get_data(self, ids, metrics, date1, date2, dimensions, filters = None, rename_cols = None):
		if (filters == None):
			filters_str = ''
		else:
			filters_str = f'&filters={filters}'
		response = requests.get(url = f'https://api-metrika.yandex.net/stat/v1/data?ids={ids}&metrics={metrics}'+\
						f'&date1={date1}&date2={date2}&dimensions={dimensions}'+\
						f"{filters_str}&limit=100000", headers=self.__auth_headers__)
		self.response = response
		metrika = pd.DataFrame([[list(y.values())[0] for y in x.get('dimensions')]+x.get('metrics') for x in response.json()['data']] \
			 ,columns=response.json()['query'].get('dimensions')+response.json()['query'].get('metrics'))
		if (rename_cols == None):
			metrika.columns = [re.sub('ym:s:','',x) for x in metrika.columns]
		else:
			metrika.columns = rename_cols
		self.data = metrika

	def write_data_to_csv(self, *args, **kwargs):
		self.data.to_csv(args, kwargs)