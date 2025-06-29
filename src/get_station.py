import re
import requests
import json
from src.utils import write

def get_station_name():
	"""获取车站名称和对应的字母代码"""
	url = "https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9345"
	response = requests.get(url)
	if response.status_code != 200:
		print("Error fetching station data")
		return None
	stations = re.findall('([\u4e00-\u9fa5]+)\|([A-Z]+)', response.text) # 匹配中文站名和对应的字母代码
	stations = dict(stations)
	stations = str(stations)
	write(stations,'station_name.txt')


def get_station_time():
	"""获取车票起售时间"""
	url = "https://www.12306.cn/index/script/core/common/qss.js"
	response = requests.get(url)
	if response.status_code != 200:
		print("Error fetching selling time data")
		return None
	json_str = re.findall('{[^}]+}',response.text)
	time_js = json.loads(json_str[0])
	write(str(time_js), 'selling_time.txt')





