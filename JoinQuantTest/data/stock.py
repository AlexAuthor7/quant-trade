from jqdatasdk import *
import pandas as pd
import os
import datetime
# auth('','')
auth('', '')
# auth('','')
data_root = 'F:/quantitative trading/JoinQuantTest/data/'

def init_db():
    '''
    初始化股票数据库
    :return:
    '''
    # 1.获取所有股票代码
    stocks = list(get_stock_list())
    # 2.存储到 csv文件 中
    for code in stocks:
        # 获取 code 的股票数据
        data = get_single_price(code, 'daily', None, None)
        # 存入 csv 中
        export_data(data=data,
                    filename=code,
                    type='price')
        print(data)
        print(data.head())

def get_stock_list():
    '''
    获取所有 A 股股票列表
    :return: stock_list
    '''
    stock_list = list(get_all_securities(['stock']).index)
    return stock_list

def get_single_price(code, time_freq, start_date=None, end_date=None):
    '''
    获取单个股票数据
    :param code: 股票数据
    :param time_freq: 时间间隔
    :param start_date: 开始日期
    :param end_date: 结束日期
    :return: data
    '''
    # 如果 start_date 为 None，默认从上市时间开始
    if start_date is None:
        start_date = get_security_info(code).start_date
    if end_date is None:
        end_date = datetime.datetime.today()
    data = get_price(code,
                     start_date=start_date,
                     end_date=end_date,
                     frequency=time_freq,
                     panel=False)
    return data

def export_data(data, filename, type, mode=None):
    '''
    导出股票行情数据
    :param data: 传入数据
    :param filename: 创建的文件名
    :param type: 表示股票的数据类型， 可以是： price, finance
    :param mode: a 代表追加， none代表默认写入
    :return:
    '''
    file_root = data_root + type + '/' + filename + '.csv'
    # 对索引进行重命名
    data.index.names = ['date']
    if mode == 'a':
        data.to_csv(file_root, mdoe=mode, header=False)
        # 删除重复值
        # 读取数据
        data = pd.read_csv(file_root)
        # 以日期为准
        data = data.drop_duplicates(subset=['date'])
        # 重新写入
        data.to_csv(file_root)
    else:
        data.to_csv(file_root)
    print('已成功存储至', filename)

def transfer_price_freq(data, time_freq):
    '''
    将数据转化为指定周期: 开盘价、收盘价、最高价、最低价
    :param data:
    :param time_freq:
    :return:
    '''
    df_trans = pd.DataFrame()
    df_trans['open'] = data['open'].resample(time_freq).first()
    df_trans['close'] = data['close'].resample(time_freq).last()
    df_trans['high'] = data['high'].resample(time_freq).max()
    df_trans['low'] = data['low'].resample(time_freq).min()
    df_trans['volume(sum)'] = data['money'].resample(time_freq).sum()
    df_trans['money(sum)'] = data['money'].resample(time_freq).sum()
    return df_trans


def get_single_fiance(code, date,statDate):
    '''
    获取单个股票财务数据
    :param code: 股票代码
    :param date: 日期
    :param statDate:
    :return:
    '''
    data = get_fundamentals(query(indicator).fileter(indicator.code == code), date=date, statDate=statDate)
    return data

def get_single_valuation(code, data, statDate):
    '''
    获取单个股票估值数据
    :param code:
    :param data:
    :param statDate:
    :return:
    '''
    data = get_fundamentals(query(valuation).filter(valuation.code == code), data=data, statDate=statDate)
    return data

def get_csv_price(code, start_date=None, end_date=None, columns=None, type='price'):
    '''
    获取本地数据，并进行数据更新
    :param code: str,股票代码
    :param type: str,类型
    :param start_date: str,起始日期,默认该股票上市时间
    :param end_date: str,结束日期,默认今天
    :param columns: list, 选取的字段
    :return: dataframe
    '''
    # # 如果 start_date 为 None，默认从上市时间开始
    # if start_date is None:
    #     start_date = get_security_info(code).start_date
    # # 如果 end_date 为 None, 默认为最新时间
    # if end_date is None:
    #     end_date = datetime.datetime.today()
    # 如果有，直接获取(与update_daily_price逻辑一致，不需要重复书写逻辑)


    # update_daily_price(code, type)
    # 文件目录
    file_root = data_root + type + '/' + code + '.csv'
    # 读取 csv 文件， 并把 date 标签 设置为 索引（index_col参数）
    if columns is None:
        data = pd.read_csv(file_root, index_col='date')
    else:
        data = pd.read_csv(file_root, usecols=columns, index_col='date')

    # 根据日期参数筛选数据
    data = data[(data.index < end_date) & (data.index > start_date)]
    return data

def caculate_change_pct(data):
    '''
    涨跌幅 = （当期收盘价 - 前期收盘价） / 当期收盘价
    :param data: 带有收盘价
    :return dataframe: 带有涨跌幅
    '''
    data['close_pct'] = (data['close'] - data['close'].shift(1)) / data['close'].shift(1)
    return data

def update_daily_price(stock_code, type='price'):
    '''
    更新本地数据
    :param stock_code:
    :param type:
    :return:
    '''
    # 3.1. 是否存在文件：不存在-重新获取，存在->3.2.
    file_root = data_root + type + '/' + stock_code + '.csv'
    if os.path.exists('file_root'):
        # 3.2. 获取增量数据（code, startsdate=对应股票csv中最新日期， enddate=今天）
        # 获取csv 中的最后一个日期,即 startdate
        start_date = pd.read_csv(file_root, useclos=['date'])['date'].iloc[-1]
        df = get_single_price(stock_code, 'daily', start_date, datetime.datetime.today())
        # 3.3. 追加到已有文件中
        df.to_csv(file_root, mode='a', header=False)
    else:
        # 重新获取该股票行情数据
        df = get_single_price(stock_code, 'daily', None, None)
        export_data(df, stock_code, 'price')
    print(stock_code, ":股票数据已更新！")

def get_index_list(index_symbol='000300.XSHG'):
    '''
    获取指数成分股，指数代码查询：https://www.joinquant.com/indexData
    :param index_symbol: 指数的代码，默认沪深300
    :return: list, 成分股代码
    '''
    stocks = get_index_stocks(index_symbol)
    return stocks


def get_csv_no_update(code, start_date=None, end_date=None, columns=None, type='price'):
    '''
    直接获取 csv 数据，不更新
    :param code:
    :param start_date:
    :param end_date:
    :param columns:
    :param type:
    :return:
    '''
    # 文件目录
    file_root = data_root + type + '/' + code + '.csv'
    # 读取 csv 文件， 并把 date 标签 设置为 索引（index_col参数）
    if columns is None:
        data = pd.read_csv(file_root, index_col='date')
    else:
        data = pd.read_csv(file_root, usecols=columns, index_col='date')
    # 根据日期参数筛选数据
    data = data[(data.index < end_date) & (data.index > start_date)]

    return data

if __name__ == '__main__':
    # 获取赎身300 指数成分股代码
    # print(get_index_list('000001.XSHG'))
    # print(len(get_index_list('000001.XSHG')))

    stocks = get_stock_list()
    for code in stocks:
        update_daily_price(code)
    exit()
    data = get_csv_price('000001.XSHE', '2020-01-01', '2021-01-01')

    print(data.tail())
