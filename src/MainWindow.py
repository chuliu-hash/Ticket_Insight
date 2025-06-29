

from ui.window_ui import Ui_MainWindow
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QHeaderView, QAbstractItemView
from PyQt5.QtGui import QStandardItem, QStandardItemModel, QFont
from src.utils import *
from src.query_request import query_ticket


class MainWindow(QMainWindow, Ui_MainWindow):
	def __init__(self):
		self.data = []  # 存放车次信息
		self.type_data = [] # 存放选中类型车次的信息

		super().__init__()  # 初始化窗口
		self.setupUi(self)  # 设置窗口UI

		self.textEdit_date.setText(get_date_now())
		self.textEdit_from.setText("合肥")
		self.textEdit_to.setText("杭州")
		self.model = QStandardItemModel()  # 创建存储数据的模式
		# 根据空间自动改变列宽度并且不可修改列宽度
		self.tableView_ticket.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
		# 设置表头不可见
		self.tableView_ticket.horizontalHeader().setVisible(False)
		# 纵向表头不可见
		self.tableView_ticket.verticalHeader().setVisible(False)
		# 设置表格内容文字大小
		font = QFont()
		font.setPointSize(10)
		self.tableView_ticket.setFont(font)
		# 设置表格内容不可编辑
		self.tableView_ticket.setEditTriggers(QAbstractItemView.NoEditTriggers)
		# 垂直滚动条始终开启
		self.tableView_ticket.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

		self.pushButton_query.clicked.connect(self.on_click_query_display)
		self.checkBox_G.stateChanged.connect(self.on_change_G_display)
		self.checkBox_D.stateChanged.connect(self.on_change_D_display)
		self.checkBox_T.stateChanged.connect(self.on_change_T_display)
		self.checkBox_Z.stateChanged.connect(self.on_change_Z_display)
		self.checkBox_K.stateChanged.connect(self.on_change_K_display)


	def on_click_query_display(self):
		"""点击按钮发送查询请求，显示余票信息"""
		self.data.clear()
		self.type_data.clear()

		get_from = self.textEdit_from.toPlainText()  # 获取出发地
		get_to = self.textEdit_to.toPlainText()  # 获取到达地
		get_date = self.textEdit_date.toPlainText()  # 获取出发时间

		if exists_txt("station_name.txt"):
			stations = eval(read('station_name.txt')) 

			if get_from  and get_to  and get_date:
				if get_from in stations and get_to in stations and is_valid_date(get_date):
					# 计算时间差
					time_difference = date_difference(get_date_now(), get_date).days
					# 时间差为0到29。12306官方要求只能查询30天以内的车票
					if time_difference >= 0 and time_difference <= 29:
						# 获取车站名对应英文代码
						from_station = stations[get_from]  
						to_station = stations[get_to]  
						self.data = query_ticket(get_date, from_station, to_station)  # 发送查询请求,并获取返回的信息
						self.checkBox_default()
						if self.data:
							# 将车票信息显示在表格中
							self.displayTable(len(self.data), 16, self.data)
						else:
							messageDialog('没有返回的网络数据！')
					else:
						messageDialog('超出查询日期的范围内,'
												 '不可查询昨天的车票信息,以及29天以后的车票信息！')
				else:
					messageDialog('输入的站名不存在(例：北京，上海),\n或日期格式不正确(例：2025-06-03)')
			else:
				messageDialog('请填写车站名称！')
		else:
			messageDialog('未下载车站查询文件！')


	# train参数为共有多少趟列车，该参数作为表格的行。
	# info参数为每趟列车的具体信息，例如有座、无座卧铺等。该参数作为表格的列
	def displayTable(self, train: int, info: int, data :list):
		""""显示车次信息的表格"""
		self.model.clear()
		for row in range(train):
			for column in range(info):
				# 填充表格项内容
				item = QStandardItem(data[row][column])
				# 向表格存储模式中添加表格项
				self.model.setItem(row, column, item)
		# 设置表格存储数据的模式
		self.tableView_ticket.setModel(self.model)
	
	def checkBox_default(self):
		"""将所有车次分类复选框取消勾选"""
		self.checkBox_G.setChecked(False)
		self.checkBox_D.setChecked(False)
		self.checkBox_Z.setChecked(False)
		self.checkBox_T.setChecked(False)
		self.checkBox_K.setChecked(False)

	def on_change_G_display(self, state):
		"""选中将高铁信息添加到表格并显示，取消选中则将高铁信息移出表格"""
		if state == Qt.Checked:
			# 获取高铁信息
			g_vehicle(self.data, self.type_data)
			# 通过表格显示该车型数据
			self.displayTable(len(self.type_data), 16, self.type_data)
		else:
			# 取消选中状态将移除该数据
			r_g_vehicle(self.data, self.type_data)
			self.displayTable(len(self.type_data), 16, self.type_data)


	def on_change_D_display(self, state):
		"""选中将动车信息添加到表格并显示，取消选中则将动车信息移出表格"""
		if state == Qt.Checked:
			d_vehicle(self.data, self.type_data)
			self.displayTable(len(self.type_data), 16, self.type_data)
		else:
			r_d_vehicle(self.data, self.type_data)
			self.displayTable(len(self.type_data), 16, self.type_data)

	def on_change_Z_display(self, state):
		"""选中将直达车信息添加到表格并显示，取消选中则将直达车信息移出表格"""
		if state == Qt.Checked:
			z_vehicle(self.data, self.type_data)
			self.displayTable(len(self.type_data), 16, self.type_data)
		else:
			r_z_vehicle(self.data, self.type_data)
			self.displayTable(len(self.type_data), 16, self.type_data)
	def on_change_T_display(self, state):
		"""选中将特快车信息添加到表格并显示，取消选中则将特快车信息移出表格"""
		if state == Qt.Checked:
			t_vehicle(self.data, self.type_data)
			self.displayTable(len(self.type_data), 16, self.type_data)
		else:
			r_t_vehicle(self.data, self.type_data)
			self.displayTable(len(self.type_data), 16, self.type_data)

	def on_change_K_display(self, state):
		"""选中将快车信息添加到表格并显示，取消选中则将快车信息移出表格"""
		if state == Qt.Checked:
			k_vehicle(self.data, self.type_data)
			self.displayTable(len(self.type_data), 16, self.type_data)
		else:
			r_k_vehicle(self.data, self.type_data)
			self.displayTable(len(self.type_data), 16, self.type_data)


