from django.shortcuts import render
from django.shortcuts import HttpResponse,HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from sign.models import Event,Guest
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.shortcuts import get_object_or_404

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
    paginator = Paginator(guest_list,5)# 创建每页3条数据的分页器
    page = request.GET.get('page') # 通过get请求得到当前要显示第几页数据
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # 如果page不是整数，显示第一页的数据
        contacts = paginator.page(1)
    except EmptyPage:
        # 如果page不在范围内，显示最后一页数据
        contacts = paginator.page(paginator.num_pages)
    return render(request,'guest_manage.html',{'user':username,'guests':contacts})
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
# 签到页面
@login_required
def sign_index(request,eid):
    event = get_object_or_404(Event,id=eid)
    return render(request,'sign_index.html',{'event':event})
# 签到动作
@login_required
def sign_index_action(request,eid):
    # 默认调用django的table.objects.get()
    # 方法，如果查询的对象不存在，则会抛出一个Http404异常。省了对table.objects.get()方法的断言。
    event = get_object_or_404(Guest,id=eid)
    phone = request.POST.get('phone','') # 通过获取用户输入的phone或直接点击签到按钮的空值
    print(phone)
    # 手机号码不存在的情况
    result = Guest.objects.filter(phone=phone)
    if not result:
        return render(request,'sign_index.html',{'event':event,'hint':'手机号码不存在，请重新输入'})

    result = Guest.objects.filter(phone=phone,event_id=eid)
    if not result:
        return render(request,'sign_index.html',{'event':event,'hint':'发布会id或者手机号码错误'})
    # 手机号码和发布会id对的上的情况：签到或未签到
    result = Guest.objects.get(phone=phone,event_id=eid)
    if result.sign:
        return render(request,'sign_index.html',{'event':event,'hint':'您已经签到'})
    else:
        Guest.objects.filter(phone=phone,event_id=eid).update(sign='1')
        return render(request,'sign_index.html',{'event':event,'hint':'签到成功','guest':result})
