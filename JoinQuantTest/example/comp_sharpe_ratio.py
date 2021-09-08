import data.stock as st
import strategy.base as stb
import pandas as pd
import matplotlib.pyplot as plt
'''设置行列 不省略'''
pd.set_option('display.max_rows', 100000)
pd.set_option('display.max_columns', 10)




# 获取 3 只股票的数据: 比亚迪、宁德时代、隆基
codes = ['002594.XSHE', '300750.XSHE', '601012.XSHG']
# 容器存放夏普
sharpes = []
for code in codes:
    data = st.get_single_price(code,
                               'daily',
                               '2018-10-01',
                               '2021-01-01')
    print(data.head())

    # 计算每只股票的夏普比率
    daily_sharpe, annual_sharpe = stb.calculate_sharpe(data)
    # 存放夏普 [[c1, s1], [c2, s2], [c3, s3]]
    sharpes.append([code, annual_sharpe])
    print(sharpes)

# 可视化 3只股票 并比较
sharpes = pd.DataFrame(sharpes, columns=['code', 'sharpe']).set_index('code')
print(sharpes)

# .bar(): 化柱状图
sharpes.plot.bar(title='Compare Annual Sharpe Ratio')
plt.xticks(rotation=30)
plt.show()