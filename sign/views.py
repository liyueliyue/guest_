from django.shortcuts import render
from django.shortcuts import HttpResponse,HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from sign.models import Event,Guest
# Create your views here.
def index(request):
    return render(request,"index.html")
# 登录动作
def login_action(request):
    if request.method == "POST":
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        # if username == 'admin' and password == 'li123456':
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user) # 登录
            request.session['user'] = username # 将session信息记录在浏览器
            response = HttpResponseRedirect('/event_manage/') # 重定向到/event_manage/路径
            # response.set_cookie('user',username,3600) # 添加浏览器cookie
            return response
        else:
            return render(request,"index.html",{'error':'username or password error!'})
@login_required
def event_manage(request):
    # username = request.COOKIES.get('user','')  # 读取浏览器cookie
    username = request.session.get('user','') # 读取浏览器sessoin
    return render(request,"event_manage.html",{'user':username}) # 使用render把cookie返回前端页面
@login_required
# 将event的列名、session中的user通过render函数返回到前端页面
def event_manage(request):
    event_list = Event.objects.all()
    username = request.session.get('user','')
    return render(request,'event_manage.html',{'user':username,'events':event_list})