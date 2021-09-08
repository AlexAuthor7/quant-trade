'''用来创建交易策略，生成交易策略'''

import data.stock as st
import numpy as np
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
    data = data[data['signal'] != 0]
    data['profit_pct'] = data['close'].pct_change()
    data = data[data['signal'] == -1]

    # data.loc[data['signal'] == 0, 'profit_pct'] = data['close'].pct_change()
    # data = data[data['signal'] == -1]
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

