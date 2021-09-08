'''用来创建交易策略，生成交易策略'''

import data.stock as st
import numpy as np
import datetime
import matplotlib.pyplot as plt
import pandas as pd

def compose_signal(data):
    '''
    整合信号：排除错误的 买入 和 卖出信息
    :param data:
    :return data: 返回整合好的信号
    '''
    data['buy_signal'] = np.where((data['buy_signal'] == 1) &
                                  (data['buy_signal'].shift(1) == 1),
                                  0,
                                  data['buy_signal'])
    data['sell_signal'] = np.where((data['sell_signal'] == -1) &
                                   (data['sell_signal'].shift(1) == -1),
                                   0,
                                   data['sell_signal'])

    # 合并买入、卖出信号
    data['signal'] = data['buy_signal'] + data['sell_signal']
    return data

def calculate_profit_percent(data):
    '''
    计算单次收益率：开仓、平仓（开仓的全部股数）
    :param data:
    :return:
    '''
    # 筛选信号 不为 0 的部分，并且计算涨跌幅
    # 由于会报错，再调用之前进行
    # data = data[data['signal'] != 0]
    data['profit_pct'] = data['close'].pct_change()
    data = data[data['signal'] == -1]

    # data.loc[data['signal'] == 0, 'profit_pct'] = data['close'].pct_change()
    # data = data[data['signal'] == -1]
    return data


def week_period_strategy(code, time_freq, start_date, end_date):
    '''生成买入卖出信号'''
    data = st.get_single_price(code,
                               time_freq=time_freq,
                               start_date=start_date,
                               end_date=end_date)
    # 新建收起字段
    data['weekday'] = data.index.weekday
    # 周四买入: 1 就是买入，0 就是不买入
    data['buy_signal'] = np.where((data['weekday'] == 3), 1, 0)
    # 周一卖出： -1 就是卖出，0 就是不卖出
    data['sell_signal'] = np.where((data['weekday'] == 0), -1, 0)
    # 整合信号：排除错误的 买入 和 卖出信息
    data = compose_signal(data)
    # 删除 0 信号
    data = data[data['signal'] != 0]
    # 计算单次收益率：开仓、平仓（开仓的全部股数）
    data = calculate_profit_percent(data)
    # 计算累积收益率
    data = calculate_accumulation_profit_percent(data)
    # 最大回撤
    data = calculate_max_drawdown(data)
    return data

def calculate_accumulation_profit_percent(data):
    '''
    计算累积收益率
    :param data:
    :return:
    '''
    data['cum_profit'] = pd.DataFrame(1 + data['profit_pct']).cumprod() - 1
    return data


def calculate_max_drawdown(data):
    '''
    计算最大回撤比
    :param data:
    :return:
    '''
    # 选取时间周期（时间窗口）
    window = 252
    # 选取时间周期中的最大净值
    data['roll_max'] = data['close'].rolling(window=252, min_periods=1).max()
    # 计算当天的回撤比 = (谷值 - 峰值）/ 峰值 = 谷值/峰值 - 1
    data['daily_drawdown'] = data['close'] / data['roll_max'] - 1
    # 计算选取时间周期的最大回撤比，即最大回撤
    data['max_drawdown'] = data['daily_drawdown'].rolling(window, min_periods=1).min()
    return data

def calculate_sharpe(data):
    '''
    计算夏普比率,返回年化的夏普比率
    公式 sharpe = （回报率的均值-无风险利率）/ 回报率的标准差
    回报率率的均值 = 日涨跌幅.mean()
    无风险利率 = 0
    回报率的标准差 = 日涨跌幅.stddeviation()
    :param data:
    :return: shaqpe, sharpe_year
    '''
    # 因子项
    daily_return = data['close'].pct_change()
    avg_return = daily_return.mean()
    sd_return = daily_return.std()
    # 计算夏普
    sharpe = avg_return / sd_return
    sharpe_year = sharpe * np.sqrt(252)
    return sharpe, sharpe_year


if __name__ == '__main__':
    data = st.get_single_price('000001.XSHE', 'daily', None, '2021-01-01')
    sharpe = calculate_sharpe(data)
    print(sharpe)

