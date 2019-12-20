from django.db import models


class AreaInfo(models.Model):
    title = models.CharField(verbose_name='标题', max_length=20)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def new_title(self):
        return self.title
    new_title.admin_order_field = 'title'  # 增加排序
    new_title.short_description = '地区名字'  # 自定义标题

    def new_parent(self):
        if not self.parent:
            return ""
        return self.parent.title
    new_parent.short_description = '父级地区名称'

    class Meta:
        db_table = 'areainfo'


class PicTest(models.Model):
    """后台上传图片"""
    picture = models.ImageField(upload_to='area')
