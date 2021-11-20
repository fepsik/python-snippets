import pandas as pd
import requests
import json

class yandexMarket:
	"""
	There is func getCosts that will be decapricated in 2022 because it applied only for ADV model.
	Yandex Market will disable this model in 2022
	"""
	def __init__(self):
		pass

	def set_credentials(self, Token, clientId='8943390a15784189a8538ce5c4d57dfb'):
		"""
		I've set default client ID but you always can set your own

		USAGE:
		yam = yandexMarket.yandexMarket()
		yam.set_credentials('your token here', 'your client id here')
		"""
		self.__token__ = Token
		self.__client_id__ = clientId
		self.__auth_headers__ = {"Authorization" : ("OAuth oauth_token="+ self.__token__ +
															   f",oauth_client_id={self.__client_id__}")}
		#Need something to validate token

	def	getCampaigns(self):
		"""
		Return pandas DataFrame with all avaible campaigns for this token
		
		USAGE:
		yam = yandexMarket.yandexMarket()
		yam.set_credentials('your token here', 'your client id here')
		camps = yam.getCampaigns()
		"""
		response = requests.get(url='https://api.partner.market.yandex.ru/v2/campaigns.json', headers = self.__auth_headers__)
		self.response = response
		campaigns = pd.DataFrame(response.json()['campaigns'])
		#map state and stateReason, drop clientId column
		stateReason_dict = {5:"проверяется",
						 6:  "требуется проверка" ,
						 7:  "выключен или выключается менеджером",
						 9:  "выключен или выключается из-за финансовых проблем",
						 11: "выключен или выключается из-за ошибок в прайс-листе магазина",
						 12: "выключен или выключается пользователем",
						 13: "выключен или выключается за неприемлемое качество",
						 15: "выключен или выключается из-за обнаружения дублирующих витрин",
						 16: "выключен или выключается из-за прочих проблем качества",
						 20: "выключен или выключается по расписанию",
						 21: "выключен или выключается, так как сайт магазина временно недоступен",
						 24: "выключен или выключается за недостаток информации о магазине",
						 25: "выключен или выключается из-за неактуальной информации"}
		campaigns.state = campaigns.state.map({1:"включен",2:"выключен",3:"включается",4:"выключается"})
		campaigns.stateReasons[campaigns.state == 'выключен'] = [', '.join(filter(None,list(map(lambda y: stateReason_dict.get(y),x)))) \
															 for x in campaigns.stateReasons[campaigns.state == 'выключен']]
		campaigns = campaigns.drop(columns='clientId')
		return(campaigns)
		#Need something to do if there is no campaigns

	def getCosts(self, fromDate, toDate, campaigns):
		"""
		Return pandas DataFrame with cost (in UA with VAT), clicks, shows for campaigns
		fromDate and toDate must be in following format: '%d-%m-%Y'
		For convert cost into RUB /w VAT you must multiply spending for 30
		stats['Ad Cost, RUB with VAT'] = stats['spending'] * 30
		
		campaigns must be DataFrame or dict with column 'id', because there is a loop that collect data for each campaign
		in campaigns.id

		USAGE:
		yam = yandexMarket.yandexMarket()
		yam.set_credentials('your token here', 'your client id here')
		camps = yam.getCampaigns()
		stats = yam.getCosts(campaigns = camps, fromDate = '15-01-2021', toDate = '25-02-2021')
		"""
		data = []
		#Need something to validate args
		for campaignId in campaigns.id:
			url = f'https://api.partner.market.yandex.ru/v2/campaigns/{campaignId}/stats/main.json?fromDate={fromDate}&toDate={toDate}&fields=shows'
			response = requests.get(url=url, headers = self.__auth_headers__)
			data_temp = response.json()['mainStats']
			[x.update({'id':campaignId}) for x in data_temp][0:0]
			data += data_temp
		stats = pd.DataFrame(data)
		stats = stats.merge(campaigns, on = 'id')
		return(stats)