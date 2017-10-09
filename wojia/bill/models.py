from django.db import models


class BillManager(models.Manager):
    """管理器"""
    def all(self):
        return super().all().filter(is_delete=False).order_by('-bdate', '-pk')  # 返回未逻辑删除的所有

    def add_new(self, bdate, bcontent, bcomment, bmoney):
        """定义添加功能"""
        bill = self.model()  # 创建一个对象
        bill.bdate = bdate
        bill.bcontent = bcontent
        bill.bcomment = bcomment
        bill.bmoney = bmoney
        bill.save()
        return bill  # 添加保存后返回

    def delete(self, uid):
        """删除功能"""
        try:
            obj = self.get(id=uid)  # 获取对象
        except self.model.DoesNotExist:  # 如果对象不存在
            return False
        else:
            obj.delete()  # 删除对象
            return True  # 返回执行成功的结果

    def get_one_object(self, bill_id):
        """获取一个有效对象"""
        try:
            obj = self.get(id=bill_id)
        except self.model.DoesNotExist:
            obj = None
        return obj  # 返回结果

    def find_query(self, filters={}, order_bys=("-bdate", "-pk")):
        """根据条件查询结果并求和"""
        bills = self.filter(**filters).order_by(*order_bys)  # 根据条件查询结果并进行排序
        try:
            price = bills.aggregate(models.Sum('bmoney'))
            price = float(price['bmoney__sum'])  # 做类型转化
        except TypeError:
            price = 0
        return bills, price  # 返回结果集和总金额

    def get_fields(self):
        """获取有效字段"""
        fields_list = []  # 初始化空列表
        fields_tuple = self.model._meta.get_fields()  # 获取所有的字段名
        for field in fields_tuple:  # 遍历元组
            if isinstance(field, models.ForeignKey):  # 如果是外键
                field_name = field.name + "_id"  # 拼接外键名
            else:
                field_name = field.name  # 否则正常获取名字
            fields_list.append(field_name)  # 加入列表
        return fields_list  # 返回

    def update_bill_info(self, bill_id, fields_dict={}):
        """更新账单信息"""
        fields_list = self.get_fields()  # 先获取有效字段
        bill = self.get_one_object(bill_id=bill_id)  # 获取对象
        if bill:  # 如果对象存在
            try:
                for key, val in fields_dict.items():  # 遍历字典
                    if (key in fields_list) and (val is not ''):  # 如果键为有效字段,并且值不是None
                        setattr(bill, key, val)  # 将该属性的值改变
                bill.save()  # 保存修改
                return True  # 返回
            except:
                return False
        return False  # 报错和对象不存在都返回False


# Create your models here.
class BillInfo(models.Model):
    """账单信息"""
    bdate = models.DateField()  # 消费日期
    bcontent = models.CharField(max_length=10)  # 消费内容
    bcomment = models.CharField(max_length=50)  # 备注
    bmoney = models.DecimalField(max_digits=7, decimal_places=2)  # 消费金额,最大7位数,小数点保留2位
    is_delete = models.BooleanField(default=0)  # 逻辑删除

    objects = BillManager()

    class Meta:
        db_table = 'bill'  # 指定表名

