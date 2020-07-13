# -*- coding: utf-8 -*-
from django.conf.urls import url

from Interaction import views

urlpatterns = [
    # 节点到节点的一个分支
    url("^showconfig$", views.showconfig),
    # 返回游戏资源包
    url("^viewZip$", views.viewZip),
    # 开始界面确定是否要继续游戏
    url("^startgame$", views.startgame),
    # 章节返回展示
    url("^chaptershow$", views.showchapter),
    # 章节选择
    url("^chapterchoice$", views.chapterchoice),
    # 游戏音量设置
    url("^settings$", views.gamesettings),
    # 保存记录
    url("^saverecord$", views.saverecord),
]
