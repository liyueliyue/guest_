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
    return render(request,"event_manage.html",{'user':username}) # 使用render把session返回前端页面
@login_required
# 发布会页面处理函数，将event的列名、session中的user通过render函数返回到前端页面
def event_manage(request):
    event_list = Event.objects.all()
    username = request.session.get('user','')
    return render(request,'event_manage.html',{'user':username,'events':event_list})

# 嘉宾页面处理函数
@login_required
def guest_manage(request):
    guest_list = Guest.objects.all() # 获得table中所有对象
    username = request.session.get('user','') # 从浏览器中获取session
    return render(request,'guest_manage.html',{'user':username,'guests':guest_list})
# 退出系统
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/index/')
# 名称搜索
@login_required
def search_name(request):
    username = request.session.get('user','')
    search_name = request.GET.get('searchName','')
    event_list = Event.objects.filter(name__contains=search_name)
    return render(request,'event_manage.html',{'user':username,'events':event_list})
# 用户真实姓名搜索
@login_required
def search_realname(request):
    username = request.session.get('user','')
    search_Realname = request.GET.get('searchRealname','')# 通过表单的name属性获取用户输入
    guest_list = Guest.objects.filter(realname__contains=search_Realname)
    return render(request,"guest_manage.html",{'user':username,'guests':guest_list})
