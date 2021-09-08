import pandas as pd
import data.stock as st
import ma_strategy as ma
import matplotlib.pyplot as plt
from scipy import stats

def ttest(data_return):
    '''
    对策略进行 t 检验
    :param data_return: 要求传入数据,包含 卖出信号,且只包含卖出信号,还要包含 每次买入卖出的 收益率 和 累积收益率
    :return: float,t值和p值
    '''
    # 调用假设检验 ttest 函数：scipy
    # 获取 t、p
    t, p = stats.ttest_1samp(data_return, 0, nan_policy='omit')  # 忽略 nan值
    # 判断是否与理论值有显著性差异: α= 0.05
    # 获取单边 p值
    p_value = p / 2
    # 观察数据

    print("t_value", t)
    print("p_value", p_value)
    print("是否拒绝[H0]收益均值 = 0：", p_value < 0.05)
    # return t, p
    return t, p_value

def signals_solve(signals_data):
    return


if __name__ == '__main__':
    '''设置行列 不省略'''
    pd.set_option('display.max_rows', 100000)
    pd.set_option('display.max_columns', 10)
    # 股票列表
    stocks = ['000001.XSHE', '000858.XSHE', '002594.XSHE']
    for code in stocks:
        # print(code)
        data = st.get_single_price(code, 'daily', None, '2021-04-01')
        data = ma.ma_strategy(data)
        print(data.tail())
        # 策略的单次收益率
        returns = data['profit_pct']
        # print(returns)
        # 绘制一下分布图用于观察
        returns.plot()
        returns.hist(bins=30)

        plt.xlim('2016-01-01', '2021-04-01')
        plt.ylim(-0.25, 1)
        plt.show()
        # 对多个股票进行计算、测试
        ttest(returns)