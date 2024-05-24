from django.core.management.base import BaseCommand
from django.db import transaction, OperationalError
from backend.models import Stock, StockPriceSSE, StockPriceSZSE, StockPriceBJSE
import concurrent.futures
import time

class Command(BaseCommand):
    help = 'Update MA5, MA10, MA20, MA30 fields for all stock prices'

    def handle(self, *args, **kwargs):
        self.update_market_ma(StockPriceSSE, 'SSE')
        self.update_market_ma(StockPriceSZSE, 'SZSE')
        self.update_market_ma(StockPriceBJSE, 'BJSE')

    def update_market_ma(self, StockPriceModel, market):
        stocks = Stock.objects.filter(market=market)
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:  # 降低并发度
            futures = [executor.submit(self.update_stock_ma, StockPriceModel, stock) for stock in stocks]
            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error updating stock: {e}"))

    def update_stock_ma(self, StockPriceModel, stock):
        prices = StockPriceModel.objects.filter(stock=stock).order_by('date')
        close_prices = [price.close for price in prices]

        ma5 = self.calculate_ma(close_prices, 5)
        ma10 = self.calculate_ma(close_prices, 10)
        ma20 = self.calculate_ma(close_prices, 20)
        ma30 = self.calculate_ma(close_prices, 30)

        retries = 5
        while retries > 0:
            try:
                with transaction.atomic():
                    for i, price in enumerate(prices):
                        price.ma5 = ma5[i]
                        price.ma10 = ma10[i]
                        price.ma20 = ma20[i]
                        price.ma30 = ma30[i]
                    StockPriceModel.objects.bulk_update(prices, ['ma5', 'ma10', 'ma20', 'ma30'])
                self.stdout.write(self.style.SUCCESS(f'Updated MA for stock: {stock.a_stock_code}'))
                break
            except OperationalError:
                retries -= 1
                self.stdout.write(self.style.WARNING(f"Database is locked, retrying... ({5 - retries}/5)"))
                time.sleep(1)  # 等待1秒后重试

    def calculate_ma(self, prices, window):
        ma = []
        for i in range(len(prices)):
            if i < window - 1:
                ma.append(None)
            else:
                ma_value = round(sum(prices[i - window + 1:i + 1]) / window, 2)
                ma.append(ma_value)
        return ma
