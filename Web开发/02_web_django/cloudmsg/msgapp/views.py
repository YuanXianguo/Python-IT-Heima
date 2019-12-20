from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponse, JsonResponse, FileResponse
from django.template import Template, Context
import os

# Create your views here.
def msgproc(request):
    data_list = []
    txt = 'msgdata.txt'
    if request.method == 'POST':
        userA = request.POST.get('userA', None)
        userB = request.POST.get('userB', None)
        msg = request.POST.get('msg', None)
        time = datetime.now()
        with open(txt, 'a+') as f:
            f.write("{}--{}--{}--{}\n".format(userB, userA, msg, time.strftime("%Y-%m-%d %H:%M:%S")))

    if request.method == 'GET':
        userC = request.GET.get("userC", None)
        if userC != None:
            with open(txt, 'r') as f:
                count = 0
                for line in f:
                    line_data = line.split('--')
                    if line_data[0] == userC:
                        count += 1
                        dic = {'userA': line_data[1], 'msg': line_data[2], 'time': line_data[3]}
                        data_list.append(dic)
                    if count >= 10:
                        break
    return render(request, 'MsgSingleWeb.html', {'data': data_list})

def homegroc(request):
    # return HttpResponse("<h1>这是首页，具体功能请访问<a href='./msggate'>这里</a></h1>")
    response = HttpResponse()
    response.write("<h1>这是首页，具体功能请访问<a href='./msggate'>这里</a></h1>")
    response.write("<h1>这是第二行</h1>")
    return response

def homegroc1(request):
    response = JsonResponse({'key': 'value'})
    return response

def homegroc2(request):
    cwd = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    response = FileResponse(open(cwd + "/msgapp/templates/pangdi.jpg", 'rb'))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="pangdi.jpg"'
    return response

def pgproc(request):
    template = Template("<h1>这个程序的名字是{{ name }}</h1>")
    context = Context({'name': '实验平台'})
    return HttpResponse(template.render(context))
