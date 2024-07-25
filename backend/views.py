from django.shortcuts import render
from django.views import View
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.models import User  # django封装好的验证功能
from django.contrib import auth

import os

from django.http import JsonResponse
from rest_framework.decorators import api_view
from backend.models import Stock, StockPriceSSE, StockPriceSZSE, StockPriceBJSE, Indicator
from backend.data.stock_data_processor import StockDataProcessor
from datetime import datetime, timedelta
import random

def index(request):
    return render(request, 'index.html')

class Login(View):
    def post(self,request):
        try:
            user = request.POST.get('username',None)
            pwd = request.POST.get('password',None)
            # 验证密码
            obj = auth.authenticate(request,username=user,password=pwd)
            if obj:
                return JsonResponse({'code':'ok','message':'账号密码验证成功'})
        except:
            return JsonResponse({'code':'no','message':'验证失败'})

class Register(View):
    def post(self, request):
        try:
            username = request.POST.get('username',None)
            password = request.POST.get('password',None)
            user = User.objects.create_user(username=username,password=password)
            user.save()
        except:
            return JsonResponse({'code':'no','message':'注册失败'})
        return JsonResponse({'code':'ok','message':'注册成功'})


@api_view(['GET'])
def get_stock_data(request, symbol):
    stock = Stock.objects.get(a_stock_code=symbol)
    if stock.market == 'SSE':
        prices = StockPriceSSE.objects.filter(stock=stock).order_by('date')
    elif stock.market == 'SZSE':
        prices = StockPriceSZSE.objects.filter(stock=stock).order_by('date')
    elif stock.market == 'BJSE':
        prices = StockPriceBJSE.objects.filter(stock=stock).order_by('date')
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid market'})

    data = {
        'name': stock.abbreviation,
        'stock_name': stock.abbreviation,
        'data': [
            {
                'date': price.date.strftime('%Y-%m-%d'),
                'open': price.open,
                'high': price.high,
                'low': price.low,
                'close': price.close,
                'ma5': price.ma5,
                'ma10': price.ma10,
                'ma20': price.ma20,
                'ma30': price.ma30,
                'nine_turn_signal_count': price.nine_turn_signal_count
            }
            for price in prices
        ]
    }
    return JsonResponse(data)

@api_view(['POST'])
def update_stock_data(request):
    # 在这里实现更新数据的逻辑
    # yesterday = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')
    today = datetime.now() .strftime('%Y-%m-%d')
    processor = StockDataProcessor()
    processor.import_all_stocks(today)
    processor.process_stocks()
    return JsonResponse({'status': 'success'})

@api_view(['GET'])
def get_all_stocks(request):
    stocks = Stock.objects.all().values('a_stock_code', 'abbreviation')
    return JsonResponse(list(stocks), safe=False)

@api_view(['GET'])
def get_indicators(request):
    indicators = Indicator.objects.all().values('name', 'description')
    return JsonResponse(list(indicators), safe=False)