import data.stock as st
import pandas as pd
import numpy as np
import statistical_test as stt
import datetime


'''选股策略'''

def get_data(index_symbol='000300.XSHG', start_date=None, end_date=None, use_cols=['date', 'close']):
    '''
    获取股票收盘价数据，并拼接为一个 dataframe
    :param index_symbol: str
    :param start_date: str
    :param end_date: list
    :param use_cols: str
    :return data_concat: dataframe, 拼接后的数据表
    '''
    # 获取股票列表代码：沪深300持有个股、创业板、上证
    stocks = st.get_index_list(index_symbol)
    # 拼接收盘价数据
    data_concat = pd.DataFrame()
    # 获取股票数据
    for code in stocks:
        data = st.get_csv_price(code, start_date, end_date, use_cols)
        # 预览股票数据
        print("==========已获取 ", code, " 数据==========")
        # 对 data 的名称进行修改，便于拼接后的区分
        data.columns = [code]
        # 拼接多个股票的收盘价：日期 股票A收盘价 股票B收盘价 ...
        data_concat = pd.concat([data_concat, data], axis=1)
    # 预览股票数据
    # print(data_concat.tail())
    return data_concat

def momentum(data_concat, shift_n=1, top_n=3, index_stock='000300.XSHG', relu='M'):
    '''
    计算时间窗口内的收益率率
    :param data_concat: dataframe
    :param shift_n: int, 表示业绩统计周期（单位：月）
    :param top_n: int, 表示收益率排前(后) top_n 会被买入(卖出)
    :param top_n: str, 表示转换频率, 默认转化为 月
    :return:
    '''
    # 转换时间频率：日->月
    data_concat.index = pd.to_datetime(data_concat.index)
    data_month = data_concat.resample(relu).last()
    # 计算过去N个月的收益率 = 期末值/期初值 - 1 =（期末-期初）/ 期初
    # optional：对数收益率 = log（期末值 / 期初值）
    shift_return = data_month / data_month.shift(shift_n) - 1
    print(shift_return)
    # 生成交易信号：收益率排前n的 > 赢家组合 > 买入 1 , 排最后n个 > 输家组合 > 卖出 -1
    buy_signals = get_top_stocks(shift_return, top_n)
    # 将 shift_return * -1 后，顺序颠倒
    sell_signals = get_top_stocks(-1 * shift_return, top_n)
    # 整合信号，合并卖出，买入信号
    signals = buy_signals - sell_signals

    # 数据预览
    # print(shift_return)
    # 打印 赢家 和 输家 组合的 shift_return
    cols_victory = [x for i, x in enumerate(signals.columns) if signals.iat[-1, i] != 1]
    cols_fail = [x for i, x in enumerate(signals.columns) if signals.iat[-1, i] != -1]


    print("==== 赢家组合 ====")
    # 赢家列表
    victory_cols = shift_return.drop(cols_victory, axis=1)
    print(victory_cols)

    print("==== 输家组合 ====")
    fail_cols = shift_return.drop(cols_fail, axis=1)
    print(fail_cols)
    # signals = signals.drop(cols, axis=1)

    # 赢家列表，输家列表
    return victory_cols.columns, fail_cols.columns

def get_top_stocks(data, top_n):
    '''
    找到前 n 位的极值，并转换位信号返回
    :param data: datafrme
    :param top_n: int,表示要产生信号的个数
    :return signals: dataframe, 返回0-1信号数据表
    '''
    # 定义一个 signals 容器，用于保存 交易信号
    signals = pd.DataFrame(index=data.index, columns=data.columns)
    # 对 data 的每一行进行遍历，找到里面的最大值，并利用 bool 函数标注为 0 或 1 信号
    for index, row in data.iterrows():
        # 获取最大的 top_n 位
        signals.loc[index] = row.isin(row.nlargest(top_n)).astype(np.int)
    return signals

def get_data_no_update(index_symbol='000300.XSHG', start_date=None, end_date=None, use_cols=['date', 'close']):
    '''
    不更新，直接获取数据
    :param index_symbol: str, 默认值为 沪深300, 可以输入 all 来获取所有股票的列表
    :param start_date:
    :param end_date:
    :param use_cols: list, 需要合并的 数据, 默认 包含 时间 和 收盘价
    :return:
    '''
    if index_symbol == 'all':
        # 如果 为 None,直接获取所有 股票列表
        stocks = st.get_stock_list()
    else:
        # 获取股票列表代码：沪深300持有个股、创业板、上证
        stocks = st.get_index_list(index_symbol)
    # 拼接收盘价数据
    data_concat = pd.DataFrame()
    # 获取股票数据
    for code in stocks:
        data = st.get_csv_no_update(code, start_date, end_date, use_cols)
        # 显示过程
        print("==========已获取 ", code, " 数据==========")
        # 对 data 的名称进行修改，便于拼接后的区分
        data.columns = [code]
        # 拼接多个股票的收盘价：日期 股票A收盘价 股票B收盘价 ...
        data_concat = pd.concat([data_concat, data], axis=1)

    # 预览股票数据
    # print(data_concat.tail())
    return data_concat





if __name__ == '__main__':
    '''设置行列 不省略'''
    pd.set_option('display.max_rows', 100000)
    pd.set_option('display.max_columns', 10000)


    '''获取赢家组合 和 暑假组合 ，并打印收益率'''
    # 沪深300、上证、上证180
    stocks = ['000300.XSHG', '000001.XSHG']

    '''不更新数据的函数'''
    # # for codes in stocks:
    # # 测试:获取沪深300 个股数据
    # data_concat = get_data_no_update('000300.XSHG', '2021-01-01', '2021-04-23')
    #
    # # 测试，动量策略
    # victory_cols, fail_cols = momentum(data_concat, top_n=10, relu='30d')

    '''更新数据的函数'''
    data_concat = get_data('000300.XSHG', '2021-04-10', '2021-05-13')
    victory_cols, fail_cols = momentum(data_concat, top_n=10, relu='30d')


    print(victory_cols)
    print(fail_cols)








