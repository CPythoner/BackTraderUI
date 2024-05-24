from django.db import models


class Stock(models.Model):
    MARKET_CHOICES = [
        ('SSE', '上证'),
        ('SZSE', '深证'),
        ('BJSE', '北交所'),
    ]

    a_stock_code = models.CharField(max_length=10, unique=True, default='TEMP_CODE')  # 临时默认值
    b_stock_code = models.CharField(max_length=10, blank=True, null=True)
    abbreviation = models.CharField(max_length=100, default='TEMP_ABBR')  # 临时默认值
    full_abbreviation = models.CharField(max_length=100, blank=True, null=True)
    english_name = models.CharField(max_length=200, blank=True, null=True)
    list_date = models.DateField(blank=True, null=True)
    market = models.CharField(max_length=4, choices=MARKET_CHOICES, default='SSE')

    def __str__(self):
        return f"{self.abbreviation} ({self.a_stock_code}) - {self.get_market_display()}"


class StockPriceSSE(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='prices_sse')
    date = models.DateField()
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    volume = models.BigIntegerField()
    turnover = models.FloatField()  # 假设有成交额字段

    ma5 = models.FloatField(null=True, blank=True)
    ma10 = models.FloatField(null=True, blank=True)
    ma20 = models.FloatField(null=True, blank=True)
    ma30 = models.FloatField(null=True, blank=True)

    nine_turn_signal_count = models.IntegerField(null=True, blank=True)  # 新增九转信号数量字段

    class Meta:
        unique_together = ('stock', 'date')
        indexes = [
            models.Index(fields=['stock', 'date']),
            models.Index(fields=['date']),
        ]

    def __str__(self):
        return f"{self.stock.symbol} - {self.date}"


class StockPriceSZSE(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='prices_szse')
    date = models.DateField()
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    volume = models.BigIntegerField()
    turnover = models.FloatField()  # 假设有成交额字段

    ma5 = models.FloatField(null=True, blank=True)
    ma10 = models.FloatField(null=True, blank=True)
    ma20 = models.FloatField(null=True, blank=True)
    ma30 = models.FloatField(null=True, blank=True)

    nine_turn_signal_count = models.IntegerField(null=True, blank=True)  # 新增九转信号数量字段

    class Meta:
        unique_together = ('stock', 'date')
        indexes = [
            models.Index(fields=['stock', 'date']),
            models.Index(fields=['date']),
        ]

    def __str__(self):
        return f"{self.stock.symbol} - {self.date}"


class StockPriceBJSE(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='prices_bjse')
    date = models.DateField()
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    volume = models.BigIntegerField()
    turnover = models.FloatField()  # 假设有成交额字段

    ma5 = models.FloatField(null=True, blank=True)
    ma10 = models.FloatField(null=True, blank=True)
    ma20 = models.FloatField(null=True, blank=True)
    ma30 = models.FloatField(null=True, blank=True)

    nine_turn_signal_count = models.IntegerField(null=True, blank=True)  # 新增九转信号数量字段

    class Meta:
        unique_together = ('stock', 'date')
        indexes = [
            models.Index(fields=['stock', 'date']),
            models.Index(fields=['date']),
        ]

    def __str__(self):
        return f"{self.stock.symbol} - {self.date}"


class Indicator(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name