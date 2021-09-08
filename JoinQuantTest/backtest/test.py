import requests
import backtrader as bt
import pandas as pd
import json
import datetime as dt
import matplotlib.pyplot as plt
import backtrader as bt
import tushare as ts
ts.set_token("")

# 获取数据
def aquire_data(stock, start_date, end_date):
    df = ts.pro_bar(ts_code=stock, adj='qfq', start_date=start_date, end_date=end_date)
    dates = pd.to_datetime(df['trade_date'])
    df = df[['open', 'high', 'low', 'close', 'vol']]
    df.columns = ['open', 'high', 'low', 'close', 'volume']
    df.index = dates
    df.sort_index(ascending=True, inplace=True)
    return df



# 策略
class MaCrossStragy(bt.Strategy):
    def log(self, txt, dt=None):
        """策略的日志功能"""
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))
    def __init__(self):
        self.close = self.data.close # 保留对 data[0] 数据序列中“close”行的引用

    def next(self):
        # 只需从参考资料中记录该系列的收盘价
        self.log('Close, %.2f' % self.dataclose[0])

        # 检查订单是否挂起...如果是，我们不能发送第二个
        if self.order:
            return

        # Check if we are in the market
        if not self.position:

            # Not yet ... we MIGHT BUY if ...
            if self.dataclose[0] < self.dataclose[-1]:
                    # current close less than previous close

                    if self.dataclose[-1] < self.dataclose[-2]:
                        # previous close less than the previous close

                        # BUY, BUY, BUY!!! (with default parameters)
                        self.log('BUY CREATE, %.2f' % self.dataclose[0])

                        # Keep track of the created order to avoid a 2nd order
                        self.order = self.buy()

        else:

            # Already in the market ... we might sell
            if len(self) >= (self.bar_executed + 5):
                # SELL, SELL, SELL!!! (with all possible default parameters)
                self.log('SELL CREATE, %.2f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()
    def notify_order(self, order):
        """侦听订单状态通知"""
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell 订单已提交/接受/被经纪商接受 - 无事可做, 返回
            return

            # 检查订单是否已完
            # 注意: 没有足够的现金,broker 可能会拒绝订单
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED, %.2f' % order.executed.price)
            elif order.issell():
                self.log('SELL EXECUTED, %.2f' % order.executed.price)

            self.bar_executed = len(self)
        # 订单被取消
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

            # Write down: no pending order
        self.order = None





if __name__ == '__main__':
    # 创建一个 cerebro 实体
    cerebro = bt.Cerebro()
    # 读取数据
    data = aquire_data("0000001", "2000-1-1", "2020-1-1")
    # 将数据 添加到 Cerebro
    cerebro.adddata(data)
    # 将策略添加到 cerebro
    cerebro.addstrategy(MaCrossStragy)


    # 设置初始金额
    cerebro.broker.setcash(100000.0)
    # 打印初始起始条件
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # 打印最终结果
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
