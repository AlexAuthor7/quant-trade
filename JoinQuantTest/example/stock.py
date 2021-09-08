import data.stock as st
import pandas as pd
import os, sys, json
'''设置行列 不省略'''
pd.set_option('display.max_rows', 100000)
pd.set_option('display.max_columns', 10)


'''获取价格，并且计算涨跌幅'''
'''初始化数据'''
code = '000002.XSHE'
data_root = 'F:/quantitative trading/JoinQuantTest/data/'

'''读取股票数据库中的数据'''

data = st.get_csv_price(code, 'price', '2020-01-01', '2021-02-01')

'''获取平安银行的行情数据 （日k）'''
# data = st.get_single_price(code,
#                            'daily',
#                            '2021-01-01',
#                            '2021-02-01')
# print(data)

'''计算涨跌幅，验证准确性'''
# data = st.caculate_change_pct(data)
# print(data)  # 多了一条 close_pct

'''获取周K: 把日k 变为 周k'''
# data_weekday = st.transfer_price_freq(data, 'W')


'''计算涨跌幅，验证准确性'''
# data_weekday = st.caculate_change_pct(data_weekday)
# print(data_weekday)



'''获取 price 目录下，文件个数'''
# path = 'F:/quantitative trading/JoinQuantTest/data/price'
# print('dirnum:', len([lists for lists in os.listdir(path) if os.path.isdir(os.path.join(path, lists))]))
# print('filenum:', len([lists for lists in os.listdir(path) if os.path.isfile(os.path.join(path, lists))]))