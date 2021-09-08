'''用于调用股票行情数据的脚本'''
import data.stock as st
import pandas as pd
'''设置行列 不省略'''
pd.set_option('display.max_rows', 100000)
pd.set_option('display.max_columns', 10)



# 初始化变量
code = '000001.XSHG'
# 调用一只股票行情数据
data = st.get_single_price(code=code,
                           time_freq='daily',
                           start_date='2021-02-01',
                           end_date='2021-02-10')

# 存入csv
st.exprot_data(data, filename=code, type='price')

# 从csv 中获取数据
data = st.get_csv_data(filename='000001.XSHG', type='price')
print(data)

# 实时更新数据：假设每天更新日k数据，存到csv文件里面 （增量添加的方式 data.to_csv(apend)）
