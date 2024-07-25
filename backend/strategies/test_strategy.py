# backend/backtrader_test.py
import backtrader as bt
import pandas as pd
from backend.utils.data_reader import get_stock_data


# 定义回测策略
class TestStrategy(bt.Strategy):
    def __init__(self):
        self.dataclose = self.datas[0].close

    def next(self):
        if self.dataclose[0] > self.dataclose[-1]:
            if self.dataclose[-1] > self.dataclose[-2]:
                self.buy()

        elif self.dataclose[0] < self.dataclose[-1]:
            if self.dataclose[-1] < self.dataclose[-2]:
                self.sell()

if __name__ == '__main__':
    # 获取股票数据
    symbol = '600000'  # 示例股票代码
    df = get_stock_data(symbol)

    # 创建 Backtrader Cerebro 引擎
    cerebro = bt.Cerebro()

    # 将 DataFrame 转换为 Backtrader 的数据格式
    data = bt.feeds.PandasData(dataname=df)

    # 将数据添加到引擎中
    cerebro.adddata(data)

    # 添加策略
    cerebro.addstrategy(TestStrategy)

    # 设置初始资金
    cerebro.broker.setcash(100000.0)

    # 设置佣金
    cerebro.broker.setcommission(commission=0.001)

    # 打印初始市值
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # 运行回测
    cerebro.run()

    # 打印最终市值
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # 绘制结果
    cerebro.plot()
