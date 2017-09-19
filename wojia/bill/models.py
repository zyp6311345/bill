from django.db import models


class BillManager(models.Manager):
    """管理器"""
    def all(self):
        return super().all().filter(is_delete=False)  # 返回未逻辑删除的所有

    def add_new(self, bdate, bcontent, bcomment, bmoney):
        """定义添加功能"""
        bill = self.model()  # 创建一个对象
        bill.bdate = bdate
        bill.bcontent = bcontent
        bill.bcomment = bcomment
        bill.bmoney = bmoney
        bill.save()
        return bill  # 添加保存后返回


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

