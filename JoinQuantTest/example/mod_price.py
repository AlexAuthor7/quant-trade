import os
import data.stock as st
import pandas as pd
'''设置行列 不省略'''
pd.set_option('display.max_rows', 100000)
pd.set_option('display.max_columns', 10)



data_root = 'F:/quantitative trading/JoinQuantTest/data/price/'
# 获取目录下所有文件的问价名
codes = list(os.walk(data_root))
# 获取文件数
print(len(codes[0][2]))
print(codes[0][2][0])
# 对文件进行批量修改
# for code in codes[0][2]:
#     # 读取文件
#     data = pd.read_csv(data_root+code,index_col='data')
#     data.index.names = ['date']
#     data.to_csv(data_root+code)
#     print("成功！")
# print(codes)