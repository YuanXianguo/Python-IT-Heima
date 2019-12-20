from django.shortcuts import render


def hello(request):
    # render()是一个打包函数，第一个参数是request,第二个参数是页面
    return render(request, '05HTMLJSDemo.html')
