from django.shortcuts import render
# Create your views here.

def index(request):
    return render(request,'Tblog/index.html',locals())


def detail(request,blog_id):
    return render(request,'Tblog/detail.html',locals())