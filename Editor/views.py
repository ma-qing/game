from django.shortcuts import render

# Create your views here.

def login(request):
    account = request.POST.get("account")
    # password使用rsa 非对称加密
    password = request.POST.get("password")
    pass
