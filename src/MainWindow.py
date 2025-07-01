from src.chart import PlotCanvas
from ui.window_ui import Ui_MainWindow
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtWidgets import QMainWindow, QHeaderView, QAbstractItemView, QTableWidgetItem, QWidget, QLabel
from PyQt5.QtGui import QStandardItem, QStandardItemModel, QFont, QColor
from src.utils import *
from src.query_request import query_ticket, query_ticket_analysis, query_time


class MainWindow(QMainWindow, Ui_MainWindow):
	def __init__(self):
		self.data = []  # 存放车次信息
		self.type_data = [] # 存放选中类型车次的信息
		self.today_list = []  # 存放今天的未判断车次座位信息（包含三类卧铺有无信息）
		self.today_train_list = []  # 存放今天的判断后车次座位信息（统一卧铺有无信息）
		self.three_list = []        # 存放三天后的未判断车次座位信息
		self.three_train_list = []  # 存放三天后的已判断车次座位信息
		self.five_list = []         # 存放五天后的未判断车次座位信息
		self.five_train_list = []   # 存放五天后的已判断车次座位信息

		super().__init__()  # 初始化窗口
		self.setupUi(self)  # 设置窗口UI

		self.info_table = []  # 保存三天中的所有不重复车次信息

		self.textEdit_date.setText(get_date_now())
		self.textEdit_from.setText("合肥")
		self.textEdit_to.setText("杭州")
		self.textEdit_from_2.setText("合肥")
		self.textEdit_to_2.setText("杭州")

		self.tabWidget.setCurrentIndex(0)  # 默认显示车票查询

		self.model = QStandardItemModel()  # 创建存储数据的模式

		# 设置车票查询区域的表格
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

		# 设置卧铺售票区域的表格
		self.tableWidget.setColumnCount(9)  # 设置表格列数
		# 设置表格内容文字大小
		font = QFont()
		font.setPointSize(12)
		self.tableWidget.setFont(font)
		# 根据窗体大小拉伸表格
		self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
		# 设置表格内容不可编辑
		self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

		self.pushButton_query.clicked.connect(self.on_click_query_display)
		self.checkBox_G.stateChanged.connect(self.on_change_G_display)
		self.checkBox_D.stateChanged.connect(self.on_change_D_display)
		self.checkBox_T.stateChanged.connect(self.on_change_T_display)
		self.checkBox_Z.stateChanged.connect(self.on_change_Z_display)
		self.checkBox_K.stateChanged.connect(self.on_change_K_display)
		self.pushButton_query_2.clicked.connect(self.on_click_query_analysis)
		self.pushButton_query_3.clicked.connect(self.on_click_query_time)


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
			add_vehicle(self.data, self.type_data, "G")
			# 通过表格显示该车型数据
			self.displayTable(len(self.type_data), 16, self.type_data)
		else:
			# 取消选中状态将移除该数据
			remove_vehicle(self.data, self.type_data, "G")
			self.displayTable(len(self.type_data), 16, self.type_data)


	def on_change_D_display(self, state):
		"""选中将动车信息添加到表格并显示，取消选中则将动车信息移出表格"""
		if state == Qt.Checked:
			add_vehicle(self.data, self.type_data, "D")
			self.displayTable(len(self.type_data), 16, self.type_data)
		else:
			remove_vehicle(self.data, self.type_data, "D")
			self.displayTable(len(self.type_data), 16, self.type_data)

	def on_change_Z_display(self, state):
		"""选中将直达车信息添加到表格并显示，取消选中则将直达车信息移出表格"""
		if state == Qt.Checked:
			add_vehicle(self.data, self.type_data, "Z")
			self.displayTable(len(self.type_data), 16, self.type_data)
		else:
			remove_vehicle(self.data, self.type_data, "Z")
			self.displayTable(len(self.type_data), 16, self.type_data)
	def on_change_T_display(self, state):
		"""选中将特快车信息添加到表格并显示，取消选中则将特快车信息移出表格"""
		if state == Qt.Checked:
			add_vehicle(self.data, self.type_data, "T")
			self.displayTable(len(self.type_data), 16, self.type_data)
		else:
			remove_vehicle(self.data, self.type_data, "T")
			self.displayTable(len(self.type_data), 16, self.type_data)

	def on_change_K_display(self, state):
		"""选中将快车信息添加到表格并显示，取消选中则将快车信息移出表格"""
		if state == Qt.Checked:
			add_vehicle(self.data, self.type_data, "K")
			self.displayTable(len(self.type_data), 16, self.type_data)
		else:
			remove_vehicle(self.data, self.type_data, "K")
			self.displayTable(len(self.type_data), 16, self.type_data)

	def on_click_query_analysis(self):
		"""点击按钮发送查询请求，并进行卧铺票售票情况分析"""
		self.today_list.clear()
		self.today_train_list.clear()
		self.three_list.clear()
		self.three_train_list.clear()
		self.five_list.clear()
		self.five_train_list.clear()
		self.info_table.clear()

		get_from = self.textEdit_from_2.toPlainText()
		get_to = self.textEdit_to_2.toPlainText()
		stations = eval(read('station_name.txt'))

		if get_from and get_to:
			if get_from in stations and get_to in stations.keys():
				from_station = stations[get_from]  # 获取站名对应英文代号
				to_station = stations[get_to]
				today = datetime.datetime.now()  # 获取今天日期
				three_day = (today + datetime.timedelta(days=2)).strftime('%Y-%m-%d')  # 三天格式化后的日期
				five_day = (today + datetime.timedelta(days=4)).strftime('%Y-%m-%d')  # 五天格式化后的日期
				today = today.strftime('%Y-%m-%d')  # 今天格式化后的日期
				# 发送查询今天，三天后，五天后的卧铺票信息的网络请求,并获取返回的信息
				query_ticket_analysis(today, from_station, to_station, self.today_list, self.today_train_list)
				query_ticket_analysis(three_day, from_station, to_station, self.three_list, self.three_train_list)
				query_ticket_analysis(five_day, from_station, to_station, self.five_list, self.five_train_list)


				info_set = set()  # 创建筛选车次集合，将三天中相同的车次进行整合去重
				for i in self.today_train_list + self.three_train_list + self.five_train_list:
					# 因为在集合中必须是字符串才能进行整合，所以将车次信息转换为字符串类型，方便车次整合
					info_set.add(str(i[0:6])) # 去掉每一车次的卧铺有无信息再添加到集合中
				for info in info_set:
					info = eval(info)  # 将车次信息再次转换成列表
					# 分析每一车次info的卧铺有无情况
					seat_analysis(info, self.today_train_list)
					seat_analysis(info, self.three_train_list)
					seat_analysis(info, self.five_train_list)
					self.info_table.append(info)

				self.tableWidget.setRowCount(len(self.info_table))  # 设置表格行数

				# 计算每趟车次的卧铺票紧张程度并以不同颜色显示
				for row in range(len(self.info_table)):
					fraction = 0  # 分数，根据该分数判断列车的紧张程度
					fraction += fraction_count(self.info_table, row, 6)
					fraction += fraction_count(self.info_table, row, 7)
					fraction += fraction_count(self.info_table, row, 8)

					# 判断分数大于等于5分的车次为红色，说明该车次卧铺非常紧张
					if fraction >= 5:
						# 填充该行的每个单元格数据并将背景颜色设置为红色
						for col in range(9):
							item = QTableWidgetItem(self.info_table[row][col])
							item.setBackground(QColor(255, 0, 0)) # 设置该车次背景颜色
							self.tableWidget.setItem(row, col, item)  # 设置表格显示的内容
					# 判断分数大于1与分数小于等于4的车次为橙色，说明该车次卧铺紧张
					if 1 <= fraction <= 4:
						for col in range(9):
							item = QTableWidgetItem(self.info_table[row][col])
							item.setBackground(QColor(255, 170, 0))
							self.tableWidget.setItem(row, col, item)  # 设置表格显示的内容
					# 判断分数等于0的车次为绿色，说明该车次卧铺不紧张
					if fraction == 0:
						for col in range(9):
							item = QTableWidgetItem(self.info_table[row][col])
							item.setBackground(QColor(85, 170, 0))
							self.tableWidget.setItem(row, col, item)  # 设置表格显示的内容

				self.show_broken_line()

			else:
				messageDialog("输入的站名不存在")
		else:
			messageDialog('请填写车站名称！')

	def show_broken_line(self):
		"""显示卧铺车票数量折线图"""
		train_name_list = []  # 保存所有车次的车次号
		tickets_number_list = []  # 保存今天，三天后，五天后所有车次的卧铺票数量

		# 遍历车次信息
		for info in self.info_table:
			number_list = []  # 临时保存车票数量

			# 统计该车次三天的卧铺票数量
			ticket_analysis(self.today_list, info, number_list)
			ticket_analysis(self.three_list, info, number_list)
			ticket_analysis(self.five_list, info, number_list)

			tickets_number_list.append(number_list)  # 添加车票数量列表
			train_name_list.append(info[0])  # 添加车次列表

		# 如果有，则删除水平布局中的折线图
		if self.horizontalLayout.count() != 0:
			item = self.horizontalLayout.takeAt(0)
			widget = item.widget()
			widget.deleteLater()

		# 创建画布对象
		line = PlotCanvas()
		line.broken_line(tickets_number_list, train_name_list)  # 调用折线图方法
		self.horizontalLayout.addWidget(line)  # 将折线图添加至底部水平布局当中

	def on_click_query_time(self):
		"""点击按钮发送查询请求，查询车票起售时间"""

		if self.gridLayout.count() != 0:
			# 循环删除网格布局的所有控件
			while self.gridLayout.count():
				# 获取第一个控件
				item = self.gridLayout.takeAt(0)
				# 删除控件
				widget = item.widget()
				widget.deleteLater()

		station = self.lineEdit_from.text()
		station_time_dict = eval(read('selling_time.txt'))
		station_name_dict = eval(read('station_name.txt'))

		if station in station_time_dict.keys():
			station_name_list, station_time_list = query_time(station_name_dict.get(station))

			# 行数标记
			i = -1
			for n in range(len(station_name_list)):
				# 每4个车站换一行
				x = n % 4
				# 当x为0的时候设置换行 行数+1
				if x == 0:
					i += 1
				# 创建布局
				self.widget = QWidget()
				# 给布局命名
				self.widget.setObjectName("widget" + str(n))
				# 设置布局样式
				self.widget.setStyleSheet('QWidget#' + "widget" + str(n) +
				"{border:2px solid rgb(175, 175, 175);background-color: rgb(255, 255, 255);}")

				# 创建Qlabel控件用于显示图片 设置控件在QWidget中
				self.label = QLabel(self.widget)
				self.label.setAlignment(Qt.AlignCenter)
				# 设置大小
				self.label.setGeometry(QRect(10, 10, 210, 65))
				font = QFont()  # 创建字体对象
				font.setPointSize(11)  # 设置字体大小
				font.setBold(True)  # 开启粗体属性
				font.setWeight(75)  # 设置文字粗细
				self.label.setFont(font)  # 设置字体
				self.label.setText(station_name_list[n] + '      ' + station_time_list[n])  # 设置显示站名与起售时间
				# 把动态创建的widegt布局添加到gridLayout中 i，x分别代表：行数以及每行的第几列
				self.gridLayout.addWidget(self.widget, i, x)

			# 设置高度为动态高度根据行数确定高度 每行100
			self.scrollAreaWidgetContents_2.setMinimumHeight((i + 1) * 100)
			# 设置网格布局控件动态高度
			self.gridLayoutWidget.setGeometry(QRect(0, 0, 950, ((i + 1) * 100)))

		else:
			messageDialog('起售车站中没有该车站名称！')







