from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator

from areas import settings
from area.models import PicTest, AreaInfo


def index(request):
    return render(request, 'areas/index.html')


def upload_pic(request):
    return render(request, 'areas/upload_pic.html')


def upload_handle(request):
    """上传图片处理"""
    # 获取上传文件的处理对象
    pic = request.FILES['pic']
    # 创建一个文件
    save_path = "{}/area/{}".format(settings.MEDIA_ROOT, pic.name)
    with open(save_path, 'wb') as f:
        # 获取上传文件的内容并写到创建的文件
        for c in pic.chunks():  # pic.chunks()是一个生成器对象
            f.write(c)

    # 保存到数据库
    PicTest.objects.create(picture='area/%s' % pic.name)
    return HttpResponse('ok')


def show_area(request, index):
    """分页"""
    areas = AreaInfo.objects.filter(parent__isnull=True)
    # 分页，每页显示5条
    paginator = Paginator(areas, 5)
    if not index:
        index = '1'
    page = paginator.page(int(index))
    return render(request, 'areas/show_area.html', {'page': page})


def areas(request):
    return render(request, 'areas/areas.html')


def prov(request):
    areas = AreaInfo.objects.filter(parent__isnull=True)
    areas_list = list()
    for area in areas:
        areas_list.append((area.id, area.title))
    return JsonResponse({'data': areas_list})


def city(request, id):
    # area = AreaInfo.objects.get(id=id)
    # areas = area.areainfo_set.all()
    areas = AreaInfo.objects.filter(parent__id=id)

    areas_list = list()
    for area in areas:
        areas_list.append((area.id, area.title))
    return JsonResponse({'data': areas_list})
