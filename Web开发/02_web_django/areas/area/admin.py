from django.contrib import admin

from area.models import AreaInfo, PicTest


class AreaStackedInline(admin.StackedInline):
    """以块的形式嵌入多端对象"""
    # 写多类的名字
    model = AreaInfo
    extra = 2


class AreaTabularInline(admin.TabularInline):
    """以表格的形式嵌入多端对象"""
    # 写多类的名字
    model = AreaInfo
    extra = 2


class AreaInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'parent', 'new_title']
    list_per_page = 10
    actions_on_bottom = True  # 底部管理框
    actions_on_top = True
    list_filter = ['title']  # 列表页右侧过滤栏
    search_fields = ['title']  # 列表页上方搜索框

    # fields = ['parent', 'title']
    fieldsets = (
        ('基本', {'fields': ['title']}),
        ('高级', {'fields': ['parent']})
    )

    # inlines = [AreaStackedInline]
    inlines = [AreaTabularInline]


admin.site.register(AreaInfo, AreaInfoAdmin)
admin.site.register(PicTest)
