# 图形画布
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib
import matplotlib.pyplot as plt


class PlotCanvas(FigureCanvas):

	def __init__(self, parent=None, width=0, height=0, dpi=100):
		# 避免中文乱码
		matplotlib.rcParams['font.sans-serif'] = ['SimHei']
		matplotlib.rcParams['axes.unicode_minus'] = False
		# 创建图形
		fig = plt.figure(figsize=(width, height), dpi=dpi)
		# 初始化图形画布
		FigureCanvas.__init__(self, fig)
		self.setParent(parent)  # 设置父类

	def broken_line(self,ticket_number_list :list, train_name_list :list):
		"""绘制折线图"""
		day_x = ['今天', '三天内', '五天内']
		for index, ticket_numer in enumerate(ticket_number_list):
			plt.plot(day_x, ticket_numer, linewidth=1, marker='o',
					 markerfacecolor='blue', markersize=8, label= train_name_list[index])
		plt.legend()
		plt.title('卧铺车票数量走势图')