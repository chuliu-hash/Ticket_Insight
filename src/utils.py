import os
import re
import time
import datetime
from PyQt5.QtWidgets import QMessageBox

def write(stations: str, filename: str):
	"""写入文本文件"""
	with open(filename, 'w', encoding='utf-8') as f:
		f.write(stations)

def read(filename: str):
	"""读取文本文件"""
	with open(filename, 'r', encoding='utf-8') as f:
		return f.readline()

def exists_txt(filename: str):
	"""判断文本文件是否存在"""
	return os.path.exists(filename)


def messageDialog(message: str):
	"""显示消息提示框"""
	msg_box = QMessageBox(QMessageBox.Warning, "警告", message)
	msg_box.exec_()

def is_valid_date(date: str) :
	"""判断日期字符串是否有效"""
	if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date):
		return False
	try:
		time.strptime(date, "%Y-%m-%d")
		return True
	except:
		return False

def date_difference(start_date: str, end_date: str) -> datetime.timedelta:
	"""计算购票时间差"""
	start = datetime.datetime.strptime(start_date, "%Y-%m-%d")
	end = datetime.datetime.strptime(end_date, "%Y-%m-%d")
	return end - start

def get_date_now()-> str:
	"""获取系统当前时间并格式化为'YYYY-MM-DD'字符串"""
	return time.strftime("%Y-%m-%d", time.localtime())

def add_vehicle(data : list, type_data: list, mark :str):
	"""添加高铁信息"""
	if data:
		for g in data:
			if g[0].startswith(mark): # 判断车次首字母是不是高铁
				type_data.append(g)

def remove_vehicle(data : list, type_data: list, mark :str):
	"""移除高铁信息"""
	if data and type_data:
		for g in data:
			if g[0].startswith(mark):
				type_data.remove(g)

def is_ticket(tmp_list :list, from_station :str, to_station: str) ->list:
	"""判断某一车次是否有高级软卧、软卧、硬卧票
	Args:
	tmp_list (list): tmp_list[3]为车次号，8,9,10为时间，21，23，28为卧铺票信息
	"""
	if tmp_list[21] == '有' or tmp_list[23] == '有' or tmp_list[28] == '有':
		tem_tem = '有'
	else:
		if tmp_list[21].isdigit() or tmp_list[23].isdigit() or tmp_list[28].isdigit():
			tem_tem = '有'
		else:
			tem_tem = '无'
	# 将车票有无信息添加至新的列表
	newSeat = [tmp_list[3], from_station, to_station, tmp_list[8], tmp_list[9], tmp_list[10], tem_tem]

	return newSeat

def seat_analysis(info :list, train_list : list):
	"""分析三天中某一车次在当天的车次中卧铺有无情况
	Args:
		info (list):存放三天中的某一趟的车次信息
		train_list (list):某一天中的所有已判断车次信息
	"""
	is_seat = False   # 标记当天是否有该趟车次
	for i in train_list:
		if info[0] in i:
			is_seat = True
			info.append(i[6]) # 添加该车次卧铺有无的信息
			break
	if not is_seat:  # 当天没有该趟车次
		info.append('--')

def ticket_analysis(train_list :list, info: list, number_list : list):
	"""分析并统计
	Args:
		info (list):存放三天中的某一趟的车次信息
		train_list (list):某一天中的所有未判断车次信息
		number_list (list):某一车次三天的卧铺票数量列表
	"""
	is_train = False
	for train in train_list:
		# 判断某天的车次信息中是否有该车次
		if info[0] in train:
			is_train = True
			number = statistical_quantity(train[6:9])  # 调用统计车票数量的方法
			number_list.append(number)  # 将车票数量添加至临时列表中
			break
	if not is_train:  # 如果今天没有某一趟列车，说明该车次无票为0
		number_list.append(0)


def fraction_count(info_table :list, row : int, column: int) -> int:
	"""计算列车卧铺票的紧张程度"""
	fraction = 0
	if column == 6:  # 如果是某趟列车今天是无票
		if info_table[row][column] == '无' or info_table[row][column] == '--':
			fraction = 3  # 计3分
	if column == 7:  # 如果是某趟列车三天内是无票
		if info_table[row][column] == '无' or info_table[row][column] == '--':
			fraction = 2  # 计2分
	if column == 8:  # 如果是某趟列车五天内是无票
		if info_table[row][column] == '无' or info_table[row][column] == '--':
			fraction = 1  # 计1分

	return fraction

def statistical_quantity(msg :list) -> int:
	"""统计车票数量"""
	num = 0
	for i in msg:
		if i == '有':
			num += 20
		elif i.isdigit():
			num += int(i)
		else:
			num += 0

	return num
