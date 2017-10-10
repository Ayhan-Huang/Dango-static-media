static & media

在Django应用的文件夹下，经常会发现这两个文件夹：static, media; static称为静态文件夹，用于存放CSS, JavaScript, 网站logo等不变的文件；相对的，把media称为媒体文件夹，用于存放用户上传的图片。

static 配置和使用

-   配置项目的settings.py:

    STATIC_URL = '/static/'  # 静态文件别名（相对路径） 和 绝对路径
    STATIC_ROOT = (
        os.path.join(BASE_DIR, 'app01/static'),
    )

-   使用：

    {% load static %}
    <img src="{% static 'img/default.jpg' %}" alt="default_photo"/>

media 配置和使用

如果需要保存用户上传的图片或文件，需要作如下配置：

-   配置项目的settings.py:

    MEDIA_URL = "/media/"   # 媒体文件别名(相对路径) 和 绝对路径
    MEDIA_ROOT = (
        os.path.join(BASE_DIR, 'app01/media')
    )

-   配置路由：

    from django.conf.urls import url
    from django.views.static import serve
    from . import settings
    
    urlpatterns = [
      	# ... the rest of your URLconf goes here ...
        url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT})
    ]

-   models.py中设置上传图片/文件字段：

    from django.db import models
    
    
    class UserInfo(models.Model):
        username = models.CharField(verbose_name='用户名', max_length=32)
        avatar = models.FileField(verbose_name='头像', upload_to='upload/avatar/')
        

upload_to相当于上传到app01/media/upload/avatar/目录下。

注意：

FileField或ImageField字段适用于存储文件/图片，出于性能考虑，文件并不直接保存到数据库，而是保存在文件系统里，因此该字段只是记录一个路径而已。

这个路径是相对于MEDIA_ROOT的，要想得到文件/图片的绝对路径，需要用.url方法。比如，要在页面中显示用户user_obj的头像，那么在模板中可以这样写：

    <img src="{{ user_obj.avatar.url }}" alt="user_avatar">

其它参考：

http://blog.csdn.net/java2king/article/details/5334303

http://blog.csdn.net/junli_chen/article/details/47335919

用户上传头像实践

准备工作

-   新建一个项目，创建应用app01，如上配置好static和media，配置路由如下：

    from django.conf.urls import url
    from app01 import views
    from django.views.static import serve
    from . import settings
    
    urlpatterns = [
        url(r'^register/$', views.register),
        url(r'^upload/$', views.upload),
        url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]

-   定义register视图函数，处理用户注册请求：

    def register(request):
        if request.method == 'GET':
            return render(request, 'register.html')

-   register.html如下：

    {% load static %}
    
    <style>
        div.custom-avatar {
            position: relative;
            width: 60px;
            height: 60px;
        }
    
        .sol {
            position: absolute;
            top: 0;
            left: 50px;
            width: 60px;
            height: 60px;
        }
    
        div.custom-avatar input {
            opacity: 0;
        }
    
    </style>
    
    <form>
        <p><label for="username">用户名：</label></p>
        <p><input type="text" id="username" name="username"></p>
        <div class="custom-avatar">
            <label for="avatar">头像：</label>
            <img src="{% static 'img/default.jpg' %}" id="avatar" class="sol">
            <input type="file" id="file-choose" class="sol">
        </div>
        <p><button>提交</button></p>
    </form>

说明：

这里通过<img src="{% static 'img/default.jpg' %}"...从server请求一张默认头像；

定义CSS，令选择文件按钮和默认头像重合；

-   浏览器访问http://127.0.0.1:8000/register/，页面如下：
    2.png

说明：浏览器查看默认头像地址为：http://127.0.0.1:8000/static/img/default.jpg；如果在调试过程中无法显示来自server的图像，可以通过在浏览器中查看图像地址是否正确。

图像预览

要求：用户每次选择一张图片，页面中即时显示该图片的预览

要点：JS onchange事件，每次用户选择了新图片，生成新的预览；FileReader文件阅读器，将文件对象转化为路径对象

    <script>
        //头像预览
        var fileChoose = document.getElementById("file-choose");
    
        fileChoose.onchange = function() {
            var file = this.files[0]; //files[0] 通过DOM对象拿到文件对象；如果是使用jQuery: $(this)[0].files[0], 要通过$(this)[0] 索引，先从JQ对象集合中拿到DOM对象
            var reader = new FileReader(); //实例化FileReader
            reader.readAsDataURL(file); //将文件对象转化为路径对象
    
            reader.onload = function () { //FileReader.onload 属性
                var imgEle = document.getElementById("avatar");
                imgEle.src = this.result //这里的this指reader对象
            }
        }
    </script>

说明：

1.  var file = this.files[0]files[0] 通过DOM对象拿到文件对象；如果是使用jQuery: $(this)[0].files[0], 要通过$(this)[0]索引，先从JQ对象集合中拿到DOM对象
2.  FileReader.onload属性：当FileReader对象调用readAsDataURL 方法后，会触发load事件，执行后面的函数。
3.  FileReader用法参考

图像上传

要点：FormDate对象发送二进制数据

-   前端上传数据

    <script>
        //上传图片，这里选择通过Ajax提交
        var form = document.getElementsByTagName('form')[0];
        form.onsubmit = function (e) {
            e.preventDefault(); //阻止默认提交
            var username = document.getElementById('username').value;
            var fileObject = document.getElementById("file-choose").files[0]; //拿到图片文件对象
    
            //实例化FormData对象，添加数据 data.append(key, value)
            var data = new FormData();
            data.append('username', username);
            data.append('img', fileObject);
    
            //XMLHttpRequest对象发送Ajax请求
            var url = '/register/';
            var xmlHttp = new XMLHttpRequest();
            xmlHttp.open('POST', url, true);
            xmlHttp.send(data);
        }
    </script>

-   后端处理，改写register视图函数，处理POST请求：

    def register(request):
        if request.method == 'GET':
            return render(request, 'register.html')
    	
        username = request.POST.get('username')
        avatar = request.FILES.get('img')
        print(avatar)  # 会打印出文件名'XXX.jpg'
        models.UserInfo.objects.create(username=username, avatar=avatar)
    
        return HttpResponse('ok')

-   测试，输入用户名，选择一张图片，点击提交



说明：为了方便测试，settings.py中注释掉了csrf中间件。

查看数据库，用户创建成功：

2.png

查看media目录，图片上传成功：

3.png



以上测试项目完整源码：https://github.com/Ayhan-Huang/Dango-static-media
