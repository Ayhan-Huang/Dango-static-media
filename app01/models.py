from django.db import models


class UserInfo(models.Model):
    username = models.CharField(verbose_name='用户名', max_length=32)
    avatar = models.FileField(verbose_name='头像', upload_to='upload/avatar/')

