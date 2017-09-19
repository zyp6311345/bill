from django.shortcuts import render, redirect
from .models import BillInfo
from django.http import JsonResponse
from datetime import date
from django.db.models import Sum
from .detorators import is_login


# Create your views here.
@is_login
def index(request):
    """主页"""
    return render(request, 'bill/index.html')


def login(request):
    """登录页"""
    return render(request, 'bill/login.html')


def login_check(request):
    """登录验证页"""
    username = request.POST.get('username')  # 获取用户名
    password = request.POST.get('password')  # 获取密码
    request.session['is_login'] = True  # 设置记住登录状态
    if (username == '530133120') and (password == 'c481def9923c44dbb97636b5e492ee36855357123932c14578da93dc0f9817d0'):
        return JsonResponse({'res': '1'})
    else:
        return JsonResponse({'res': '0'})


@is_login
def add_new(request):
    """添加新内容"""
    # 1.获取前端传入数据,获取到的都是字符串
    bdate = request.POST.get('date')  # 读取日期
    bcontent = request.POST.get('content')  # 读取内容
    bcomment = request.POST.get('ps')  # 读取备注
    bmoney = request.POST.get('money')  # 读取金额
    bdate_list_str = bdate.split('-')  # 做字符串切割,获得的是字符串
    bdate_list = [int(x) for x in bdate_list_str]  # 做整数转化
    bdate = date(bdate_list[0], bdate_list[1], bdate_list[2])  # 转化日期格式
    bmoney = int(bmoney)  # 转换数字格式

    # 2.添加进数据库
    try:
        BillInfo.objects.add_new(bdate, bcontent, bcomment, bmoney)  # 添加并获取返回结果
        return JsonResponse({'res': '1'})
    except:
        return JsonResponse({'res': '0'})


@is_login
def find_all(request):
    """查询所有"""
    dict_money = BillInfo.objects.aggregate(Sum('bmoney'))  # 查询金额总和
    sum_money = int(dict_money['bmoney__sum'])  # 取值后做整数转化

    bills = BillInfo.objects.all()  # 查询所有内容
    bills_list = []  # 定义用于装bill的列表
    for bill in bills:
        bill_info = [bill.bdate, bill.bcontent, bill.bcomment, bill.bmoney]  # 定义用于装bill详细信息的列表,一个列表就是一个Bill
        bills_list.append(bill_info)  # 存入大列表内

    return JsonResponse({'res': bills_list, 'sum': sum_money})
