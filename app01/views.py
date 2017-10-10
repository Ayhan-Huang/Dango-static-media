from django.shortcuts import render, HttpResponse
from . import models


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')

    username = request.POST.get('username')
    avatar = request.FILES.get('img')
    print(avatar)  # 打印出文件名'1_ayhan_huang.jpg'
    models.UserInfo.objects.create(username=username, avatar=avatar)

    return HttpResponse('ok')

