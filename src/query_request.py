import requests
import json
from src.utils import exists_txt, read, is_ticket


def query_12306(date: str, from_station: str, to_station: str):
	""""查询12306的余票信息并返回原始数据"""
	
	# 创建会话对象，自动管理Cookie和连接池
	session = requests.Session()

	init_url = "https://kyfw.12306.cn/otn/leftTicket/init"
	# 访问首页，获取必要的Cookie
	session.get(url = init_url)

	# 设置查询参数
	params = {
		"leftTicketDTO.train_date": date,
		"leftTicketDTO.from_station": from_station,
		"leftTicketDTO.to_station": to_station,
		"purpose_codes": "ADULT"
	}
	
	try:
		# 查询余票
		query_url = "https://kyfw.12306.cn/otn/leftTicket/query"
		response = session.get(url = query_url, params=params)
		
		if response.status_code == 200:
			try:
				result = response.json()['data']['result']
				return result
			except:
				print(params)
				print(response.url)
				print("json解析失败")
				print(f"响应内容:\n{response.text}")
		else:
			print(f"请求失败，状态码: {response.status_code}")
		
	except Exception as e:
		print(f"请求异常: {type(e).__name__}: {str(e)}")
	

"""
result中保存的某一车次的原始数据信息ori:
%2FpzBFMv1nC%0Ahj%2BEMx1mFt2mVvgs59aetipQqx8SrinzQcjGP2eVfzeQI7TQnodGvIb1kZmeuZAfR%2Bj7nUHqr0sy%0A6aK7VML1TOiPlBb0sXDWIBK%2F3vWmG9MIFr%2FPlHQJNEg%3D|预订|2400000G190Q|G19|VNP|AOH|VNP|AOH|16:00|20:28|04:28|N|uAWTjGjz5yxiej7XrXHmUy5RLe0k4C9xhU0hsoiPj6SUVNIK|20250627|3|P4|01|04|1|0|||||||||||无|无|无||90M0O0|9MO|0|1||9231800000M106000000O066200000|0|||||1|5#1#0#S#z#0#z#z||7|CHN,CHN|||N#N#|||202506131245|Y
"""
def query_ticket(date: str, from_station: str, to_station: str)-> list:
	"""向12306发出查询，从返回的原始数据中筛查有用信息"""
	result = query_12306(date, from_station, to_station)
	data = []
	if exists_txt('station_name.txt'):
		stations = eval(read('station_name.txt'))
		if result:
			# result中的每一元素即为某一车次的原始数据信息
			for ori in result:
				tmp_list = ori.split('|') # 分割原始数据
				# 通过value_list的对应车站代码下标，从key_list中获取与其对应的车站名
				from_station = list(stations.keys())[list(stations.values()).index(tmp_list[6])]
				to_station = list(stations.keys())[list(stations.values()).index(tmp_list[7])]
				
				# 从原始数据中获取车次号，站名，时间，座位余量等信息组成列表
				train = [tmp_list[3], from_station, to_station, tmp_list[8], tmp_list[9], tmp_list[10]
					, tmp_list[32], tmp_list[31], tmp_list[30], tmp_list[21]
					, tmp_list[23], tmp_list[33], tmp_list[28], tmp_list[24], tmp_list[29], tmp_list[26]]
				
				newTrain = []
				# 将信息中的空("")改成--
				for t in train:
					if t == "":
						t = "--"
					else:
						t = t
					newTrain.append(t) 
				data.append(newTrain)
			
	else:
		print("Can't find station_name.txt")

	return data


def query_ticket_analysis(date :str, from_station: str, to_station :str, ori_list :list, pro_list: list):
	"""查询卧铺卧铺售票数据并分析处理"""
	result = query_12306(date, from_station, to_station)

	if exists_txt('station_name.txt'):
		stations = eval(read('station_name.txt'))  
		if result:  
			for i in result:
				tmp_list = i.split('|') 
				from_station = list(stations.keys())[list(stations.values()).index(tmp_list[6])]
				to_station = list(stations.keys())[list(stations.values()).index(tmp_list[7])]
				# 从tmp_list中筛查数据，创建车次座位信息列表
				seat = [tmp_list[3], from_station, to_station, tmp_list[8], tmp_list[9], tmp_list[10]
					, tmp_list[21], tmp_list[23], tmp_list[28]]
					# 将高铁(G)、动(D)、C开头的车次，排除
				if not seat[0].startswith('G') and not seat[0].startswith('D') and not seat[0].startswith('C') :
					ori_list.append(seat)    # 将未判断车次座位信息添加至列表
					new_seat = is_ticket(tmp_list, from_station, to_station) # 判断某车次是否有票
					pro_list.append(new_seat)  # 将判断后的车次座位信息添加至列表


def query_time(station :str) -> tuple[list, list]:
	"""查询车票起售时间"""
	station_name_list = []  # 存放站名
	station_time_list = []  # 存放站名对应的起售时间
	station_time_dict = eval(read('selling_time.txt'))
	url = 'https://www.12306.cn/index/otn/index12306/queryScSname'
	form_data = {"station_telecode": station}
	response = requests.post(url, data = form_data)
	response.eoncoding = 'utf-8'
	json_data = json.loads(response.text)
	data = json_data.get('data')

	for name in data:  # 遍历查询车站所对应的所有站名
		name = name[4:]   # 获取中文站名
		if name in station_time_dict.keys():  # 在站名时间文件中，判断是否存在该站名
			station_name_list.append(name)  # 有该站名就将站名添加至列表中
	for name in station_name_list:  # 遍历筛选后的站名
		time = station_time_dict.get(name)  # 通过站名获取对应的起售时间
		station_time_list.append(time)  # 将时间保存至列表
	return station_name_list, station_time_list 

