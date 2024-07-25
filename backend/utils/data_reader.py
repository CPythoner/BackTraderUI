import pandas as pd
from backend.models import Stock, StockPriceSSE, StockPriceSZSE, StockPriceBJSE


def get_stock_data(symbol):
    # 根据股票代码获取股票对象
    try:
        stock = Stock.objects.get(a_stock_code=symbol)
    except Stock.DoesNotExist:
        raise ValueError(f"Stock with code {symbol} does not exist.")

    # 根据市场类型从相应的表中获取数据
    if stock.market == 'SSE':
        stock_prices = StockPriceSSE.objects.filter(stock=stock).order_by('date')
    elif stock.market == 'SZSE':
        stock_prices = StockPriceSZSE.objects.filter(stock=stock).order_by('date')
    elif stock.market == 'BJSE':
        stock_prices = StockPriceBJSE.objects.filter(stock=stock).order_by('date')
    else:
        raise ValueError(f"Unknown market type for stock {symbol}")

    data = []
    for price in stock_prices:
        data.append([
            price.date,
            price.open,
            price.high,
            price.low,
            price.close,
            price.volume
        ])

    # 转换为 DataFrame 格式
    df = pd.DataFrame(data, columns=['date', 'open', 'high', 'low', 'close', 'volume'])
    df.set_index('date', inplace=True)
    return df
