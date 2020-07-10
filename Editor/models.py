from django.db import models

# Create your models here.


# 后台用户信息
class AdminUsers(models.Model):
    account = models.CharField(max_length=32, verbose_name="账户名(email号)")
    password = models.CharField(max_length=64, verbose_name="密码")
    username = models.CharField(max_length=32, verbose_name="真实用户名")


# 故事配置  ---Mongo or Mysql
class Story(models.Model):
    name = models.CharField(max_length=32, verbose_name="故事名")
    storytype = models.CharField(verbose_name="")
    storyimg = models.CharField(max_length=64, verbose_name="游戏封面")
    descrip = models.CharField(max_length=1024, verbose_name="游戏介绍")
    editor = models.ForeignKey(AdminUsers, db_constraint=False, on_delete=models.DO_NOTHING,verbose_name="后台用户id", db_column="editorid")
    status = models.BooleanField(default=False, verbose_name="是否发布")

