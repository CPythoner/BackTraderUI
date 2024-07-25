# backend/management/commands/import_stocks.py
import pandas as pd
from django.core.management.base import BaseCommand
from backend.models import Stock
from datetime import datetime

class Command(BaseCommand):
    help = 'Import stocks from an Excel file into the Stock table'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='The path to the Excel file')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        self.stdout.write(self.style.SUCCESS(f'Reading data from {file_path}'))

        # 读取 Excel 文件
        df = pd.read_excel(file_path, header=1)

        for index, row in df.iterrows():
            a_stock_code = row['A股代码']
            b_stock_code = row['B股代码'] if 'B股代码' in row and not pd.isna(row['B股代码']) else None
            abbreviation = row['证券简称']
            full_abbreviation = row['扩位证券简称'] if '扩位证券简称' in row else ''
            english_name = row['公司英文全称'] if '公司英文全称' in row else ''
            list_date = datetime.strptime(str(row['上市日期']), '%Y%m%d') if '上市日期' in row else None

            # 直接将市场类别设置为 'SSE'
            market = 'SSE'

            # 创建或更新 Stock 对象
            stock, created = Stock.objects.update_or_create(
                a_stock_code=a_stock_code,
                defaults={
                    'b_stock_code': b_stock_code,
                    'abbreviation': abbreviation,
                    'full_abbreviation': full_abbreviation,
                    'english_name': english_name,
                    'list_date': list_date,
                    'market': market
                }
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f'Created new stock: {a_stock_code} - {abbreviation}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Updated existing stock: {a_stock_code} - {abbreviation}'))

        self.stdout.write(self.style.SUCCESS('Import completed successfully'))
