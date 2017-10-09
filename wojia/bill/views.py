from django.shortcuts import render, redirect
from .models import BillInfo
from django.http import JsonResponse
from datetime import date
from django.db.models import Sum, Q, F
from .detorators import is_login
from django.views.decorators.http import require_GET, require_POST


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
    # 初始化空字典
    condition = {}

    # 先判断日期是否为空
    if start_date != '':
        start_date_list = start_date.split('-')  # 做字符串切割
        start_date_int = [int(x) for x in start_date_list]  # 转化成数字
        start_date = date(start_date_int[0], start_date_int[1], start_date_int[2])  # 转化日期格式
        condition["bdate__gte"] = start_date  # 将起始日期存入条件内

    if end_date != '':
        end_date_list = end_date.split('-')  # 做字符串切割
        end_date_int = [int(x) for x in end_date_list]  # 转化成数字
        end_date = date(end_date_int[0], end_date_int[1], end_date_int[2])  # 转化日期格式
        condition["bdate__lte"] = end_date  # 结束日期存入条件内

    if content != '':
        condition["bcontent__contains"] = content  # 查询内容存入条件内

    if comment != '':
        condition["bcomment__contains"] = comment  # 备注存入条件内

    # 判断金额是否为空,非空做类型转化
    if start_money != '':
        start_money = int(start_money)
        condition["bmoney__gte"] = start_money  # 起始金额存入条件内
    if end_moeny != '':
        end_moeny = int(end_moeny)
        condition["bmoney__lte"] = end_moeny  # 结束金额存入条件内
    bill_obj, res_sum = BillInfo.objects.find_query(condition)  # 获取结果集

    bills = []  # 定义一个空列表,用于存放所有数据信息
    for bill in bill_obj:  # 遍历出所有对象
        bill_list = [bill.bdate, bill.bcontent, bill.bcomment, bill.bmoney, bill.id]  # 组建数据
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


@require_POST
@is_login
def edit(request):
    """修改内容"""
    bdate = request.POST.get('date')  # 获取日期
    bcontent = request.POST.get('content')  # 获取内容
    bcomment = request.POST.get('comment')  # 获取备注
    bmoney = request.POST.get('money')  # 获取金额
    bill_id = request.POST.get('id')  # 获取id
    edit_dict = {
        "bdate": bdate,
        "bcontent": bcontent,
        "bcomment": bcomment,
        "bmoney": bmoney
    }
    res = BillInfo.objects.update_bill_info(bill_id, edit_dict)  # 调用更新方法
    res = "1" if res else "0"
    return JsonResponse({'res': res})  # 返回结果