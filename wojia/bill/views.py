from django.shortcuts import render, redirect
from .models import BillInfo
from django.http import JsonResponse
from datetime import date
from django.db.models import Sum, Q, F
from .detorators import is_login
from django.views.decorators.http import require_GET


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
    bmoney = float(bmoney)  # 转换数字格式

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
        bill_info = [bill.bdate, bill.bcontent, bill.bcomment, bill.bmoney, bill.id]  # 定义用于装bill详细信息的列表,一个列表就是一个Bill
        bills_list.append(bill_info)  # 存入大列表内

    return JsonResponse({'res': bills_list, 'sum': sum_money})


@is_login
def find_query(request):
    """根据条件查询"""
    start_date = request.POST.get('start_date')  # 获取起始日期
    end_date = request.POST.get('end_date')  # 获取结束日期
    content = request.POST.get('find_content')  # 获取查询内容
    comment = request.POST.get('find_comment')  # 获取查询备注
    start_money = request.POST.get('start_money')  # 获取起始金额
    end_moeny = request.POST.get('end_money')  # 获取结束金额
    # 获取的都是字符串,如果空就是空字符串
    body_str = ''

    # 先判断日期是否为空
    if start_date != '':
        start_date_list = start_date.split('-')  # 做字符串切割
        start_date_int = [int(x) for x in start_date_list]  # 转化成数字
        start_date = date(start_date_int[0], start_date_int[1], start_date_int[2])  # 转化日期格式
        bill_obj = BillInfo.objects.filter(bdate__gte=start_date)  # 对起始日期进行筛选
    else:
        bill_obj = BillInfo.objects.all()  # 如果没选定起始日期就查询所有

    if end_date != '':
        end_date_list = end_date.split('-')  # 做字符串切割
        end_date_int = [int(x) for x in end_date_list]  # 转化成数字
        end_date = date(end_date_int[0], end_date_int[1], end_date_int[2])  # 转化日期格式
        bill_obj = bill_obj.filter(bdate__lte=end_date)  # 对结束时间进行过滤

    if content != '':
        bill_obj = bill_obj.filter(bcontent__contains=content)  # 对内容进行过滤

    if comment != '':
        bill_obj = bill_obj.filter(bcomment__contains=comment)  # 对备注进行过滤

    # 判断金额是否为空,非空做类型转化
    if start_money != '':
        start_money = int(start_money)
        bill_obj = bill_obj.filter(bmoney__gte=start_money)  # 对起始金额过滤
    if end_moeny != '':
        end_moeny = int(end_moeny)
        bill_obj = bill_obj.filter(bmoney__lte=end_moeny)  # 对结束金额过滤

    try:  # 查询时可能会出现没有结果的情况
        res_sum = bill_obj.aggregate(Sum('bmoney'))  # 计算总金额
        res_sum = int(res_sum['bmoney__sum'])  # 做类型转化
    except TypeError:
        res_sum = 0
    bills = []  # 定义一个空列表,用于存放所有数据信息
    for bill in bill_obj:  # 遍历出所有对象
        bill_list = [bill.bdate, bill.bcontent, bill.bcomment, bill.bmoney]  # 组建数据
        bills.append(bill_list)  # 添加进列表组

    return JsonResponse({'res': bills, 'sum': res_sum})


@require_GET
@is_login
def delete(request):
    """删除"""
    uid = request.GET.get('id')  # 获取id
    res = BillInfo.objects.delete(uid)  # 获取返回结果
    res = '1' if res else '0'  # 如果返回True则res为1,否则为0
    return JsonResponse({'res': res})
