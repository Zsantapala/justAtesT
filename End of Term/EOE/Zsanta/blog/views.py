from django.shortcuts import render,redirect
from django.http import Http404
from .models import User, Article, hashID
from .forms import UserForm, RegisterForm, ArticleForm
import hashlib, string, random, time
# Create your views here.
def randomstr():                                 #产生随机数
    Words = string.ascii_letters+string.digits
    s = ''
    for num in range(8):
        s += random.choice(Words)
    return s

def hash_code(s):           #hash检查表
    h = hashlib.sha256()
    salt = randomstr()
    s += salt
    h.update(s.encode())
    final_h = h.hexdigest()
    return final_h, salt                 #返回hash和随机数''

def get_hash(s,username):
    h = hashlib.sha256()
    user = User.objects.get(name=username)
    salt = hashID.objects.get(u_id=user)
    s += salt.UhashID
    h.update(s.encode())
    final_h = h.hexdigest()
    return final_h  # 返回hash值
def index(request):
    articles = Article.objects.all()[:10]
    return render(request, 'blog/index.html', {'articles': articles})

def login(request):
    if request.session.get('is_login', None):
        return redirect('index')
    if request.method == 'POST':
        login_form = UserForm(request.POST)
        message = '请检查填写内容！'
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = User.objects.get(name=username)
                if user.password == get_hash(password, username):
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    return redirect('index')
                else:
                    message = '密码错误！'
                    return render(request, 'blog/login.html', {'message': message, 'login_form': login_form})
            except:
                message = '用户不存在！'
                return render(request, 'blog/login.html', {'message': message, 'login_form': login_form})
    login_form = UserForm()
    return render(request, 'blog/login.html', locals())

def logout(request):
    if not request.session.get('is_login', None):
        return redirect('index')
    request.session.flush()
    return redirect('index')

def register(request):
    if request.session.get('is_login', None):  # 登录状态不允许注册。你可以修改这条原则！
        return redirect("index")
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            sex = register_form.cleaned_data['sex']
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'blog/register.html', locals())
            else:
                same_name_user = User.objects.filter(name=username)
                same_email_user = User.objects.filter(email=email)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'blog/register.html', locals())
                elif same_email_user:  # 邮箱地址唯一
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, 'blog/register.html', locals())  # 当一切都OK的情况下，创建新用户
                new_user = User.objects.create()
                new_user.name = username
                new_user.password, salt = hash_code(password1)
                new_user.email = email
                new_user.sex = sex
                new_user.save()
                time.sleep(3)
                uid = User.objects.get(name=username)                           #查询新创建用户
                hashID.objects.create(u_id=uid, UhashID=salt)                   #关联数据库hashID外链
                return redirect('login')  # 自动跳转到登录页面
    register_form = RegisterForm()
    return render(request, 'blog/register.html', locals())

def edit_page(request):
    if not request.session.get('is_login', None):
        return redirect('index')
    if request.method == 'POST':
        artiform = ArticleForm(request.POST)
        message = "请输入有效内容！"
        if artiform.is_valid():
            u_id = request.session.get('user_id', None)
            user = User.objects.get(pk=u_id)
            headline = artiform.cleaned_data['headline']
            text_body = artiform.cleaned_data['text_body']
            user.article_set.create(headline=headline, text_body=text_body)
            user.save()
            return redirect('index')
        else:
            return render(request, 'blog/edit_page.html', locals())
    artiform = ArticleForm()
    return render(request, 'blog/edit_page.html', locals())

def article(request,article_id):
    article_p = Article.objects.get(pk=article_id)
    edit = False
    if request.session.get('is_login', None):
        u_id = request.session.get('user_id', None)
        if u_id == article_p.u_id.id:
            edit = True
            return render(request, 'blog/article.html', {'article': article_p, 'edit': edit})
    return render(request, 'blog/article.html', {'article': article_p, 'edit':edit})

def edit_article(request,article_id):
    if not request.session.get('is_login', None):
        return redirect('index')
    article_p = Article.objects.get(pk=article_id)
    u_id = request.session.get('user_id', None)
    if request.method == 'POST':
        headline = request.POST.get('headline')
        text_body = request.POST.get('text_body')
        article_p.headline = headline
        article_p.text_body = text_body
        article_p.save()
        return redirect('index')
    elif u_id == article_p.u_id.id:
        arti_date ={
            'headline': article_p.headline,
            'text_body': article_p.text_body,
        }
        artiform = ArticleForm(initial=arti_date)
        return render(request, 'blog/edit_article.html', {'artiform': artiform, 'article': article_p})
    return redirect('index')

def arti_list(request,page=1):
    total = len(Article.objects.all())
    if total < 10:
        total_page = 1
        Articles = Article.objects.all()
        return render(request, 'blog/article_list.html', {'articles': Articles, 'total_page': total_page, 'page': page})
    else:
        if total % 10 == 0:
            total_page = total
        else:
            total_page = total+1
        if page > total_page:
            return redirect('index')
        else:
            Articles = Article.objects.all()[(page - 1) * 10:10]
            return render(request, 'blog/article_list.html', {'articles': Articles,'total_page': total_page, 'page': page})
