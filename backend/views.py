from django.shortcuts import render
from django.views import View
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.models import User  # django封装好的验证功能
from django.contrib import auth

from django.http import JsonResponse
from rest_framework.decorators import api_view
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
    # 生成示例数据
    start_date = datetime(2022, 1, 1)
    dates = [(start_date + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(100)]
    prices = [[random.uniform(200, 300), random.uniform(200, 300), random.uniform(200, 300), random.uniform(200, 300)]
              for _ in dates]

    data = {
        'dates': dates,
        'prices': prices
    }
    return JsonResponse(data)


@api_view(['POST'])
def update_stock_data(request):
    # 在这里实现更新数据的逻辑
    return JsonResponse({'status': 'success'})

