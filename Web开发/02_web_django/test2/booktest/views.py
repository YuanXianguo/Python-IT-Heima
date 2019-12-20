from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.urls import reverse
from booktest.models import BookInfo


def index(request):
    books = BookInfo.objects.all()
    return render(request, 'booktest/index.html', {'books': books})


def create(request):
    book = BookInfo()
    book.title = "倚天屠龙记"
    book.save()
    return redirect('/index')


def delete(request, id):
    book = BookInfo.objects.get(id=id)
    book.delete()
    return redirect('/index')


def ajax_test(request):
    """显示ajax页面"""
    return render(request, 'booktest/ajax_test.html')


def ajax_handle(request):
    return JsonResponse({'res': 1})


def ajax_login(request):
    return render(request, 'booktest/ajax_login.html')


def ajax_login_check(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    if username == 'daguo' and password == '123':
        tmp = {'res': 1}
    else:
        tmp = {'res': 0}
    return JsonResponse(tmp)


def set_cookie(request):
    response = HttpResponse("设置cookie")
    response.set_cookie('num', 1, max_age=14*24*3600)  # 两周后过期
    return response


def get_cookie(request):
    num = request.COOKIES['num']
    return HttpResponse(num)


def set_session(request):
    request.session['username'] = 'daguo'
    request.session['age'] = 18
    return HttpResponse('设置session')


def get_session(request):
    username = request.session['username']
    age = request.session['age']
    return HttpResponse(username + ":" + str(age))


def url_reverse(request):
    return render(request, 'booktest/url_reverse.html')


def show_args(request, a, b):
    return render(request, 'booktest/url_reverse.html')


def show_kwargs(request, c, d):
    return render(request, 'booktest/url_reverse.html')


def redirect_reverse(request):
    # return redirect(reverse('booktest:index'))
    # return redirect(reverse('booktest:show_args', args=(1, 2)))
    return redirect(reverse('booktest:show_kwargs', kwargs={"c": 3, "d": 4}))
