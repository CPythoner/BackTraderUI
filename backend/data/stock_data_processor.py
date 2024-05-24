import pandas as pd
from datetime import datetime, timedelta
import baostock as bs
from django.db import transaction
from backend.models import Stock, StockPriceSSE, StockPriceSZSE, StockPriceBJSE


class StockDataProcessor:
    def __init__(self, file_path=None):
        self.file_path = file_path
        lg = bs.login()
        if lg.error_code != '0':
            raise Exception(f"Login failed: {lg.error_msg}")
        print("Login successful")

    def __del__(self):
        bs.logout()
        print("Logout successful")

    def read_stock_codes(self):
        """从数据库中获取所有股票代码。"""
        return Stock.objects.all().values_list('a_stock_code', 'market')

    def save_data(self, data, fields, stock, market):
        """将数据保存到数据库中。"""
        stock_instance = Stock.objects.get(a_stock_code=stock)

        if market == 'SSE':
            StockPrice = StockPriceSSE
        elif market == 'SZSE':
            StockPrice = StockPriceSZSE
        elif market == 'BJSE':
            StockPrice = StockPriceBJSE
        else:
            print(f"Unknown market for stock: {stock}")
            return

        stock_prices = []
        for entry in data:
            stock_prices.append(StockPrice(
                stock=stock_instance,
                date=entry[0],
                open=float(entry[2]) if entry[2] else None,
                high=float(entry[3]) if entry[3] else None,
                low=float(entry[4]) if entry[4] else None,
                close=float(entry[5]) if entry[5] else None,
                volume=int(entry[9]) if entry[9] else 0,
                turnover=float(entry[10]) if entry[10] else 0.0
            ))

        with transaction.atomic():
            StockPrice.objects.bulk_create(stock_prices, ignore_conflicts=True)

        print(f"Data saved for stock: {stock}")

    def get_last_date(self, stock):
        """获取股票数据文件中的最后一个日期。"""
        try:
            stock_instance = Stock.objects.get(a_stock_code=stock)
        except Stock.DoesNotExist:
            print(f"Stock with code {stock} does not exist.")
            return "1990-12-19"

        try:
            if stock_instance.market == 'SSE':
                StockPrice = StockPriceSSE
            elif stock_instance.market == 'SZSE':
                StockPrice = StockPriceSZSE
            elif stock_instance.market == 'BJSE':
                StockPrice = StockPriceBJSE
            else:
                print(f"Unknown market for stock: {stock_instance.market}")
                return "1990-12-19"

            last_record = StockPrice.objects.filter(stock=stock_instance).order_by('-date').first()
            if last_record:
                return last_record.date.strftime("%Y-%m-%d")
            else:
                return "1990-12-19"  # 如果没有数据，从1990-12-19开始获取数据
        except Exception as e:
            print(f"Error retrieving last date for stock {stock}: {e}")
            return "1990-12-19"

    def get_stock_data(self, stock, market):
        """获取单只股票的数据，并根据现有文件进行增量更新。 """
        if market == 'BJSE':
            return [], []

        market_prefix = {
            'SSE': 'sh',
            'SZSE': 'sz'
        }.get(market, 'sh')
        full_stock_code = f"{market_prefix}.{stock}"

        print(f"Processing stock: {full_stock_code}")
        start_date = self.get_last_date(stock)
        end_date = datetime.now().strftime("%Y-%m-%d")  # 获取当前日期

        # 检查最新日期和今天日期是否一致
        if start_date == end_date:
            print(f"No need to update data for {full_stock_code}, as the latest date is today.")
            return [], []

        rs = bs.query_history_k_data_plus(
            full_stock_code,
            "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST",
            start_date=start_date,
            end_date=end_date,
            frequency="d",
            adjustflag="3",
        )

        if rs.error_code != "0":
            print(f"query_history_k_data_plus respond error_code: {rs.error_code}")
            print(f"query_history_k_data_plus respond error_msg: {rs.error_msg}")
            return None, None

        data_list = []
        while rs.next():
            data_list.append(rs.get_row_data())
        return data_list, rs.fields

    def process_stocks(self):
        stocks = self.read_stock_codes()
        for stock, market in stocks:
            data, fields = self.get_stock_data(stock, market)
            if data:
                self.save_data(data, fields, stock, market)

    def import_all_stocks(self, day):
        """从 BaoStock 导入所有股票到数据库中。"""
        rs = bs.query_all_stock(day=day)
        if rs.error_code != '0':
            print(f"query_all_stock respond error_code: {rs.error_code}")
            print(f"query_all_stock respond error_msg: {rs.error_msg}")
            return

        data_list = []
        while rs.next():
            data_list.append(rs.get_row_data())
        result = pd.DataFrame(data_list, columns=rs.fields)

        for index, row in result.iterrows():
            code = row['code']
            trade_status = row['tradeStatus']
            name = row['code_name']

            if code.startswith('sh'):
                market = 'SSE'
            elif code.startswith('sz'):
                market = 'SZSE'
            elif code.startswith('bj'):
                market = 'BJSE'
            else:
                print(f"Unknown market for stock code: {code}")
                continue

            a_stock_code = code[3:]

            stock, created = Stock.objects.update_or_create(
                a_stock_code=a_stock_code,
                defaults={
                    'abbreviation': name,
                    'market': market,
                    # 'trade_status': trade_status
                }
            )

            if created:
                print(f'Created new stock: {a_stock_code} - {name}')
            else:
                print(f'Updated existing stock: {a_stock_code} - {name}')

        print('Import completed successfully')


# 使用示例
if __name__ == '__main__':
    yesterday = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')
    processor = StockDataProcessor()
    processor.import_all_stocks(day=yesterday)
    processor.process_stocks()
