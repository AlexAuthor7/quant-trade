import data.stock as st
import pandas as pd
import numpy as np
import base as stb
import matplotlib.pyplot as plt
'''择时策略'''

def ma_strategy_singal(data, short_window=5, long_window=20):
    '''
    双均线策略
    :param data: dataframe,投资标的行情数据（必须包含收盘价）
    :param short_window: 短期n日移动平均线,默认5
    :param long_window: 长期n日移动平均线,默认20
    :return: dataframe
    '''
    # 计算技术指标： ma短期、ma长期
    data = pd.DataFrame(data)
    data['short_ma'] = data['close'].rolling(window=short_window).mean()
    data['long_ma'] = data['close'].rolling(window=long_window).mean()
    # 生成信号：金叉买入、死叉卖出
    data['buy_signal'] = np.where(data['short_ma'] > data['long_ma'], 1, 0)
    data['sell_signal'] = np.where(data['short_ma'] < data['long_ma'], -1, 0)
    # 过滤信号： st.compose_signal
    data = stb.compose_signal(data)
    data['signal'] = data['buy_signal'] + data['sell_signal']
    # 删除 0 信号
    # data = data[data['signal'] != 0]
    return data

def ma_strategy(data, short_window=5, long_window=20):
    '''
    双均线策略
    :param data: dataframe,投资标的行情数据（必须包含收盘价）
    :param short_window: 短期n日移动平均线,默认5
    :param long_window: 长期n日移动平均线,默认20
    :return: dataframe
    '''
    # 计算技术指标： ma短期、ma长期
    data = pd.DataFrame(data)
    data['short_ma'] = data['close'].rolling(window=short_window).mean()
    data['long_ma'] = data['close'].rolling(window=long_window).mean()
    # 生成信号：金叉买入、死叉卖出
    data['buy_signal'] = np.where(data['short_ma'] > data['long_ma'], 1, 0)
    data['sell_signal'] = np.where(data['short_ma'] < data['long_ma'], -1, 0)
    # 过滤信号： st.compose_signal
    data = stb.compose_signal(data)
    data['signal'] = data['buy_signal'] + data['sell_signal']
    # 删除 0 信号
    data = data[data['signal'] != 0]
    # 数据预览
    # print(data[['close', 'short_ma', 'long_ma', 'signal']])
    # 计算单次收益率
    data = stb.calculate_profit_percent(data)
    # 计算累次收益率
    data = stb.calculate_accumulation_profit_percent(data)
    # 删除 列
    data.drop(labels=['buy_signal', 'sell_signal'], axis=1)
    # 开仓次数
    # print("开仓次数", int(len(data)))
    return data

if __name__ == '__main__':
    '''设置行列 不省略'''
    pd.set_option('display.max_rows', 100000)
    pd.set_option('display.max_columns', 10)
    # 股票列表
    stocks = ['000001.XSHE', '000858.XSHE', '002594.XSHE']
    # 存放累积收益率
    cum_profits = pd.DataFrame()
    # 循环获取数据
    for code in stocks:
        data = st.get_single_price(code, 'daily', '2020-01-01', '2021-01-01')
        data = ma_strategy(data)
        print(data)

        cum_profits[code] = data['cum_profit'].reset_index(drop=True)
        # 折线图
        data['cum_profit'].plot(label=code)

    # 数据预览
    print("开仓次数", int(len(data)))
    print(cum_profits)
    # 可视化
    cum_profits.plot()
    plt.title("Comparison of Ma Strategy Profits")
    plt.show()