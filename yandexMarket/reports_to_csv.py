import pandas as pd
import os
import re

def reports_to_csv(dir_path, csv_path = 'total_stats.csv'):
	"""
		Convert reports created via GUI of yandex market https://partner.market.yandex.ru/shop/{campaign_id}/stat/placement?fromDate=2021-06-01&toDate=2021-06-30&detalization=day&entity=costs
		into one csv file. Columns in final csv file is id (campaign id), date, clicks, show, spending
		Args:
			dir_path : path to directory where reports
			csv_path : path where to save final report with actual file name
	"""
	files = []
	#Collect necessary files into array named files
	with os.scandir(dir_path) as list_dir:
	    for entry in list_dir:
	        if re.match(r'\d+-day-report', entry.name):
	            files += [entry.name]
	fin_table = pd.DataFrame()
	#Read and transform all files into one DataFrame
	for file in files:
	    temp_table = pd.read_excel(dir_path+file)
	    temp_table['id'] = re.match(r'\d+',file)[0]
	    temp_table['total_val'] = [round(sum(np.where(temp_table.iloc[n,2:-1].values == '-',0,temp_table.iloc[n,2:-1].values)),2) for n in range(len(temp_table))]
	    temp_table = pd.pivot_table(temp_table, values = 'total_val', columns='Показатель', aggfunc=np.sum, index = ['id','Дата']).reset_index()
	    fin_table = fin_table.append(temp_table)
	    fin_table = fin_table.rename(columns={'Дата':'date', 'Клики': 'clicks', 'Показы':'shows', 'Расходы':'spending'})
	#Write this DataFrame into csv file
	fin_table.to_csv('total_stats.csv', index = False)