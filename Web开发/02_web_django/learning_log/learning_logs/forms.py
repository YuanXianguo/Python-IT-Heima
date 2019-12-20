from django import forms

from .models import Topic, Entry


class TopicForm(forms.ModelForm):
    class Meta:
        """告诉Django根据哪个模型创建表单，以及在表单中包含哪些字段"""
        model = Topic  # 根据模型Topic创建一个表单

        fields = ['text']  # 该表单只包含字段text
        labels = {'text': ''}  # 不要为字段text生成标签


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': ''}
        # 小部件(widgets)是一个HTML表单元素，如单行文本框、多行文本区域或下拉列表
        # 通过设置属性widgets，可覆盖Django选择的默认小部件
        # forms.Textarea，定制了字段'text'的输入小部件，将文本区域宽度设置为80，而不是默认的40
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}


