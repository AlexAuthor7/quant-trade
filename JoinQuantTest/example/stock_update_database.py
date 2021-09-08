import os, sys, json
import pandas as pd
import data.stock as st
import datetime
'''设置行列 不省略'''
pd.set_option('display.max_rows', 100000)
pd.set_option('display.max_columns', 10)

# 初始化变量
# code = '000002.XSHG'
#
# # 调用一致股票的行情数据
# data = st.get_single_price(code=code,
#                             time_freq='daily',
#                             start_date='2021-02-01',
#                             end_date='2021-03-01')
#
#
# # 存入 csv
# st.export_data(data=data,
#                filename=code,
#                type='price')


'''读取股票数据库'''
#


'''初始化股票数据库'''
# st.init_db()

'''更新股票数据库'''
# 实时更新数据：假设每天更新 日k 数据 > 存到csv文件里面 > data.to_csv(mode='a)
# 3.每日更新数据
st.update_daily_price(code, 'price')
# 3.1. 获取增量数据 （code, start_date ）


'''股票总数'''
# stocks = st.get_stock_list()
# print(len(stocks))

'''获取 price 文件下 文件数量'''
# path = 'F:/quantitative trading/JoinQuantTest/data/price'
# print('dirnum:', len([lists for lists in os.listdir(path) if os.path.isdir(os.path.join(path, lists))]))
# print('filenum:', len([lists for lists in os.listdir(path) if os.path.isfile(os.path.join(path, lists))]))