# from django.core.management.base import BaseCommand
# from django.db import transaction, OperationalError
# from backend.models import Stock, StockPriceSSE, StockPriceSZSE, StockPriceBJSE
# import concurrent.futures
# import time
#
# class Command(BaseCommand):
#     help = 'Update nine turn signal count fields for all stock prices'
#
#     def handle(self, *args, **kwargs):
#         self.update_market_nine_turn_signal_count(StockPriceSSE, 'SSE')
#         self.update_market_nine_turn_signal_count(StockPriceSZSE, 'SZSE')
#         self.update_market_nine_turn_signal_count(StockPriceBJSE, 'BJSE')
#
#     def update_market_nine_turn_signal_count(self, StockPriceModel, market):
#         stocks = Stock.objects.filter(market=market)
#         with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:  # 降低并发度
#             futures = [executor.submit(self.update_stock_nine_turn_signal_count, StockPriceModel, stock) for stock in stocks]
#             for future in concurrent.futures.as_completed(futures):
#                 try:
#                     future.result()
#                 except Exception as e:
#                     self.stdout.write(self.style.ERROR(f"Error updating stock: {e}"))
#
#     def update_stock_nine_turn_signal_count(self, StockPriceModel, stock):
#         prices = StockPriceModel.objects.filter(stock=stock).order_by('date')
#         close_prices = [price.close for price in prices]
#
#         nine_turn_signal_counts = self.calculate_nine_turn_signal_count(close_prices)
#
#         retries = 5
#         while retries > 0:
#             try:
#                 with transaction.atomic():
#                     for i, price in enumerate(prices):
#                         price.nine_turn_signal_count = nine_turn_signal_counts[i]
#                     StockPriceModel.objects.bulk_update(prices, ['nine_turn_signal_count'])
#                 self.stdout.write(self.style.SUCCESS(f'Updated nine turn signal count for stock: {stock.a_stock_code}'))
#                 break
#             except OperationalError:
#                 retries -= 1
#                 self.stdout.write(self.style.WARNING(f"Database is locked, retrying... ({5 - retries}/5)"))
#                 time.sleep(1)  # 等待1秒后重试
#
#     def calculate_nine_turn_signal_count(self, prices):
#         counts = []
#         for i in range(len(prices)):
#             if i < 8:
#                 counts.append(None)
#             else:
#                 if prices[i] > prices[i - 4] and prices[i - 4] > prices[i - 8]:
#                     count = (counts[-1] + 1) if counts[-1] and counts[-1] < 9 else 1
#                 elif prices[i] < prices[i - 4] and prices[i - 4] < prices[i - 8]:
#                     count = (counts[-1] - 1) if counts[-1] and counts[-1] > -9 else -1
#                 else:
#                     count = 0
#                 counts.append(count)
#         return counts


from django.core.management.base import BaseCommand
from django.db import transaction, OperationalError
from backend.models import Stock, StockPriceSSE, StockPriceSZSE, StockPriceBJSE
import concurrent.futures
import time

class Command(BaseCommand):
    help = 'Update nine turn signal count fields for all stock prices'

    def handle(self, *args, **kwargs):
        self.update_market_nine_turn_signal_count(StockPriceSSE, 'SSE')
        self.update_market_nine_turn_signal_count(StockPriceSZSE, 'SZSE')
        self.update_market_nine_turn_signal_count(StockPriceBJSE, 'BJSE')

    def update_market_nine_turn_signal_count(self, StockPriceModel, market):
        stocks = Stock.objects.filter(market=market)
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:  # 降低并发度
            futures = [executor.submit(self.update_stock_nine_turn_signal_count, StockPriceModel, stock) for stock in stocks]
            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error updating stock: {e}"))

    def update_stock_nine_turn_signal_count(self, StockPriceModel, stock):
        prices = StockPriceModel.objects.filter(stock=stock).order_by('date')
        close_prices = [price.close for price in prices]

        nine_turn_signal_counts = self.calculate_nine_turn_signal_count(close_prices)

        retries = 5
        while retries > 0:
            try:
                with transaction.atomic():
                    for i, price in enumerate(prices):
                        price.nine_turn_signal_count = nine_turn_signal_counts[i]
                    StockPriceModel.objects.bulk_update(prices, ['nine_turn_signal_count'])
                self.stdout.write(self.style.SUCCESS(f'Updated nine turn signal count for stock: {stock.a_stock_code}'))
                break
            except OperationalError:
                retries -= 1
                self.stdout.write(self.style.WARNING(f"Database is locked, retrying... ({5 - retries}/5)"))
                time.sleep(1)  # 等待1秒后重试

    def calculate_nine_turn_signal_count(self, prices):
        counts = []
        n = len(prices)

        for i in range(n):
            if i < 8:
                counts.append(0)  # 前8个数据无法计算九转信号
            else:
                count = 0
                if prices[i] > prices[i - 4] and prices[i - 4] > prices[i - 8]:
                    count = (counts[-1] + 1) if counts and counts[-1] < 9 else 1
                elif prices[i] < prices[i - 4] and prices[i - 4] < prices[i - 8]:
                    count = (counts[-1] - 1) if counts and counts[-1] > -9 else -1
                else:
                    count = 0
                counts.append(count)

        return counts
