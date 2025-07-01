from src.MainWindow import MainWindow
from src.utils import exists_txt, messageDialog
from src.get_station import get_station_name, get_station_time
from PyQt5.QtWidgets import QApplication
import sys
import os


def main():
	if not exists_txt('station_name.txt') or not exists_txt('selling_time.txt'):
		get_station_name()
		get_station_time()
	
	os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"  # 启用自动高 DPI 缩放
	app = QApplication(sys.argv)  # 创建应用程序实例

	# 检查站名文件和车票起售时间文件是否存在
	if not exists_txt('station_name.txt') or not exists_txt('selling_time.txt'):
		messageDialog("站名文件或车票起售时间文件不存在。")
		sys.exit(1)

	window = MainWindow()         # 创建主窗口实例
	window.show()                 # 显示主窗口
	sys.exit(app.exec_())		  # 启动事件循环

if __name__ == "__main__":
	main()