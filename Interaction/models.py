from django.db import models

# Create your models here.


# 用户表
from Editor.models import Story


# 用户信息
class Users(models.Model):
    username = models.CharField(max_length=32, verbose_name="用户名")
    email = models.CharField(max_length=32, verbose_name="邮箱号")
    password = models.CharField(max_length=64, verbose_name="用户密码")
    phonenum = models.CharField(max_length=16, verbose_name="手机号")
    bgmSound = models.IntegerField(default=20, verbose_name="背景音乐音量")
    soundEffects = models.IntegerField(default=20, verbose_name="游戏音效音量")
    dubbingSound = models.IntegerField(default=20, verbose_name="配音音量")

    class Meta:
        db_table = "users"


# 操作记录表
class UserChoice(models.Model):
    user = models.ForeignKey(Users,  db_constraint=False, on_delete=models.DO_NOTHING, verbose_name="user外键", db_column="userid")
    stroy = models.ForeignKey(Story, db_constraint=False, on_delete=models.DO_NOTHING, verbose_name="故事外键", db_column="storyid")
    chapterid = models.IntegerField(verbose_name="选择的章节")
    choiceid = models.IntegerField(verbose_name="具体id选择")
    fatherid = models.IntegerField(verbose_name="父节点")

    class Meta:
        db_table = "userchoice"


