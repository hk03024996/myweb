from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from meblog.settings import MEDIA_URL
from django.contrib import auth
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from .forms import LoginForm, RegForm
from .models import Live, LiveType
from comment.models import Comment
from comment.forms import CommentForm

# Create your views here.
'''
#文章列表
class LiveList(View):
    def get(self, request, *args, **kwargs):
        all_lives = Live.objects.all()
        return render_to_response(request, "index.html", {
            "all_lives": all_lives,

        })

#文章详情

class LiveDetail(View):
    def get(self, request, live_id, *args, **kwargs):
        live_detail = LiveType.objects.filter(live_id)
        return render_to_response(request, "news.html", {
            "live_detail": live_detail
       })
       
'''

def live_list(request):

    lives_all_list = Live.objects.all()
    paginator = Paginator(lives_all_list, 8)
    page_num = request.GET.get('page', 1)
    page_of_blogs = paginator.get_page(page_num)
    currentr_page_num = page_of_blogs.number

    page_range = list(range(max(currentr_page_num - 2, 1), currentr_page_num)) + \
                 list(range(currentr_page_num, min(currentr_page_num + 2, paginator.num_pages) + 1))
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
        page_range.insert(0, '...')
    # 加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    context = {}
    context['lives'] = page_of_blogs.object_list
    context['page_of_blogs'] = page_of_blogs
    context['page_range'] = page_range
    context['live_types'] = LiveType.objects.all()
    context['hot_lives'] = Live.objects.order_by("readed_num")[0:3]
    return render(request,"index.html", context)

def live_type(request):
    context = {}
    context['lives'] = Live.objects.all()
    context['live_types'] = LiveType.objects.filter(live_type=live_type)
    return render(request,"index.html", context)


def live_detail(request, live_id):
    live = get_object_or_404(Live, pk=live_id)
    if not request.COOKIES.get("live_%s_readed" % live_id):
        live.readed_num += 1
        live.save()

    live_content_type = ContentType.objects.get_for_model(live)
    comments = Comment.objects.filter(content_type=live_content_type, object_id=live.pk, parent=None)

    #hot_lives = Live.objects.order_by("readed_num")

    context = {}
    context['live'] = live
    context['comment_form'] = CommentForm(initial={'content_type': live_content_type.model, "object_id": live_id, 'reply_comment_id': 0})
    context['hot_lives'] = Live.objects.order_by("readed_num")[0:3]
    context['MEDIA_URL'] = MEDIA_URL
    context['user'] = request.user
    context['comments'] = comments.order_by('-comment_time')
    response = render(request,"news.html", context)
    response.set_cookie("live_%s_readed" % live_id, "true")
    return response

def live_with_type(request, live_type_pk):
    lives_all_list = Live.objects.all()
    paginator = Paginator(lives_all_list, 8)
    page_num = request.GET.get('page', 1)
    page_of_blogs = paginator.get_page(page_num)
    currentr_page_num = page_of_blogs.number

    page_range = list(range(max(currentr_page_num - 2, 1), currentr_page_num)) + \
                 list(range(currentr_page_num, min(currentr_page_num + 2, paginator.num_pages) + 1))
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
        page_range.insert(0, '...')
    # 加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)


    context = {}
    live_type = get_object_or_404(LiveType, pk=live_type_pk)
    context['live_type'] = live_type
    context['page_of_blogs'] = page_of_blogs
    context['page_range'] = page_range
    context['lives'] = Live.objects.filter(live_type=live_type)
    context['hot_lives'] = Live.objects.order_by("readed_num")[0:3]
    context['live_types'] = LiveType.objects.all()
    return render(request, "live_with_type.html", context)


def login(request):
        if request.method == 'POST':
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                user = login_form.cleaned_data['user']
                auth.login(request, user)
                return redirect(request.GET.get('from', reverse('home')))
        else:
            login_form = LoginForm()

        context = {}
        context['login_form'] = login_form
        return render(request, 'login.html', context)


def register(request):
    if request.method == 'POST':
        reg_form = RegForm(request.POST)
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            #email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']
            password_again = reg_form.cleaned_data['password_again']
            # 创建用户
            user = User.objects.create_user(username, password, password_again)
            user.save()
            # 登录用户
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        reg_form = RegForm()

    context = {}
    context['reg_form'] = reg_form
    return render(request, 'register.html', context)

def logout(request):
    request.session.flush()
    return redirect("home")



'''
def login(request):
    
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(request, username=username, password=password)
    referer = request.META.get('HTTP_REFERER', reverse('home'))
    if user is not None:
        auth.login(request, user)
        return redirect(referer)
    else:
        return render(request, 'error.html', {'message':'用户名或密码不争取'})


    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = auth.authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect(request.GET.get('from', reverse('home')))
            else:
                login_form.add_error(None, '用户名或密码错误')
                context = {}
                context['login_form'] = login_form
                return render(request, 'login.html', context)
        else:
            pass
    else:
        login_form = LoginForm()
        context = {}
        context['login_form'] = login_form
        return render(request, 'login.html', context)
'''







