from django.db import models


# Create your models here.
class Fund(models.Model):
    symbol = models.CharField(
        max_length=10, unique=True, db_comment="基金代码"
    )
    pinyin_abbreviation = models.CharField(
        max_length=20, db_comment="拼音缩写"
    )
    fund_short_name = models.CharField(
        max_length=100, db_comment="基金简称"
    )
    fund_type = models.CharField(max_length=50, db_comment="基金类型")  # 基金类型
    pinyin_full_name = models.CharField(
        max_length=200, db_comment="拼音全称"
    )

    class Meta:
        db_table = 'fund'
        db_table_comment = '存储基金信息的表，包括基金代码、拼音缩写、基金简称、基金类型和拼音全称'


    def __str__(self):
        return self.fund_short_name
