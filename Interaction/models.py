from django.db import models

# Create your models here.


# 用户表
class Users(models.Model):
    username = models.CharField(max_length=32, verbose_name="用户名")
    bgmSound = models.IntegerField(verbose_name="背景音乐音量")
    soundEffects = models.IntegerField(verbose_name="游戏音效音量")
    dubbingSound = models.IntegerField(verbose_name="配音音量")


# 操作记录表
class UserChoice(models.Model):
    user = models.ForeignKey(Users,  db_constraint=False, on_delete=models.DO_NOTHING, verbose_name="user外键")
    chapter = models.IntegerField(verbose_name="选择的章节")
    choiceid = models.IntegerField(verbose_name="具体id选择")
    fatherid = models.IntegerField(verbose_name="父节点")

