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

def g_vehicle(data : list, type_data: list):
    """添加高铁信息"""
    if data:
        for g in data:
            if g[0].startswith('G'): # 判断车次首字母是不是高铁
                type_data.append(g)


def r_g_vehicle(data : list, type_data: list):
    """移除高铁信息"""
    if data and type_data:
        for g in data:
            if g[0].startswith('G'):
                type_data.remove(g)
def d_vehicle(data : list, type_data: list):
    """添加动车信息"""
    if data:
        for d in data:
            if d[0].startswith('D'):
                type_data.append(d)

def r_d_vehicle(data : list, type_data: list):
    """移除动车信息"""
    if data and type_data:
        for d in data:
            if d[0].startswith('D'):
                type_data.remove(d)

def z_vehicle(data : list, type_data: list):
    """添加直达车信息"""
    if data:
        for z in data:
            if z[0].startswith('Z'):
                type_data.append(z)

def r_z_vehicle(data : list, type_data: list):
    """移除直达车信息"""
    if data and type_data:
        for z in data:
            if z[0].startswith('Z'):
                type_data.remove(z)

def t_vehicle(data : list, type_data: list):
    """添加特快车信息"""
    if data:
        for t in data:
            if t[0].startswith('T'):
                type_data.append(t)

def r_t_vehicle(data : list, type_data: list):
    """移除特快车信息"""
    if data and type_data:
        for t in data:
            if t[0].startswith('T'):
                type_data.remove(t)

def k_vehicle(data: list, type_data: list):
    """添加快车信息"""
    if data:
        for k in data:
            if k[0].startswith('K'):
                type_data.append(k)
def r_k_vehicle(data : list, type_data: list):
    """移除快车信息"""
    if data and type_data:
        for k in data:
            if k[0].startswith('K'):
                type_data.remove(k)


