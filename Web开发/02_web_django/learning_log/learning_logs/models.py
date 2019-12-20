from django.db import models
from django.contrib.auth.models import User

class Topic(models.Model):
    """用户学习的主题"""
    # 创建一个外键实例，将每个主题关联到特定用户
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    # CharField()由文本或字符组成的数据，预留空间200个字符
    text = models.CharField(max_length=200)
    # DateTimeField()记录日期和时间的数据，auto_now_add=True，自动设置成当前日期和时间
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """返回模型的字符串表示"""
        return self.text


class Entry(models.Model):
    """学到的有关某个主题的具体知识"""
    # 创建一个外键实例，将每个条目关联到特定的主题； on_delete=models.CASCADE级联删除
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        """存储管理模型的额外信息，设置一个额外属性：让Django在需要时使用Entries来表示多个条目"""
        verbose_name_plural = 'entries'

    def __str__(self):
        """返回模型的字符串表示：前50个字符+..."""
        return self.text[:50] + "..."

