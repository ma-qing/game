import os
import time
import zipfile

import requests
from django.db.models import Count
from django.http import HttpResponse, JsonResponse, FileResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.views.decorators.gzip import gzip_page

from Interaction.models import UserChoice
from Interaction.serializerdata import serializermongodata
from common.CONSSTANTS import CHAPTERCHOICE, CHAPTERPAGE
from common.CodeStatus import CHAPTERID_ERR, REMEEBERCHAPTER_ERR, STORYID_ERR, METHOD_ERR
from common.utils import recursiveMongodata, collection, collection_data, return_render_listjson, searchMongoIndex, \
    return_render_dictjson, set_redis
from game.settings import BASE_DIR
redis_r = set_redis(1)


def startgame(request):
    if request.method == "POST":
        uid = request.POST.get('uid')
        storyid = request.POST.get("storyid")
        # 去redis中查找storyid对应的用户信息
        if not (storyid and uid):
            return return_render_dictjson(code=STORYID_ERR, msg="没有storyid or uid ")
        story_key = storyid + "story"
        story_hkey = uid + "chapter"
        remeberdata = redis_r.hget(story_key, story_hkey)
        if remeberdata:
            remeberdata_str = remeberdata.decode()
            remeberid = remeberdata_str.split("#")[1]
        else:
            remeberid = ""
        data = {
            "remeberid": remeberid,
        }
        return return_render_dictjson(data)
    else:
        return return_render_dictjson(code=METHOD_ERR, msg="Method error")


# 章节选择
def showchapter(request):
    if request.method == "POST":
        # 类型选择
        uid = request.POST.get("uid")
        storyid = request.POST.get("storyid")
        chapters = collection_data.find({"commandType": CHAPTERPAGE})
        # 在游戏进度保存数据库中查看是否存在 保存格式 chapter1-chapter2-chapter3#createId
        story_key = storyid + "story"
        story_hkey = uid + "chapter"
        remeberdata = redis_r.hget(story_key, story_hkey)
        if remeberdata:
            remeberdata_str = remeberdata.decode()
            # 所有章节的id
            remember_chapterid_str = remeberdata_str.split("#")[0]
            # 记录点的id
            remebercreateId = remeberdata_str.split("#")[1]
            # 记录点所在的章节
            remeberchapterid = collection_data.find_one({"createId": int(remebercreateId)}).get("chapter")

            remember_chapterid_list = remember_chapterid_str.split("-")
        else:
            remember_chapterid_list = []
            remeberchapterid = ""
            remebercreateId = ""

        detaillist = []
        for chapter in chapters:
            chapter["_id"] = str(chapter.get("_id"))
            # 进行过的章节状态为1， 否者为0
            if str(chapter.get("chapter")) in remember_chapterid_list:
                # 进行过的章节 中找正在进行的章节中的CreateID
                if chapter.get("chapter") == remeberchapterid:
                    chapter['remeberid'] = remebercreateId
            else:
                # 如果记录选择节点的数据库中查不到
                chapter['status'] = 0

            detaillist.append(chapter)
        return return_render_listjson(data=detaillist)
    else:
        return return_render_listjson(code=METHOD_ERR, msg="Method error")


# 章节选择页
def chapterchoice(request):
    if request.method == 'POST':
        remeberid = request.POST.get("remeberid")
        chapterid = request.POST.get("createId")
        uid = request.POST.get("uid")
        # 如果客户端记录了退出之前的id
        if remeberid:
            remeberid = int(remeberid)
            search_dict = searchMongoIndex(collection, remeberid)
            detail_list = serializermongodata(search_dict, collection_data)
            return return_render_listjson(data=detail_list)
        # 如果客户端没有记id, 则从该章节的第一页开始
        else:
            if not chapterid:
                return return_render_dictjson(code=CHAPTERID_ERR, msg="没有章节ID!")
            search_dict = searchMongoIndex(collection, chapterid)
            detail_list = serializermongodata(search_dict, collection_data)
            return return_render_listjson(data=detail_list)


# 详情页
def showconfig(request):
    # 递归查询Mongo collection 中的分支节点与分支节点之间的ID
    choiceid = request.POST.get("choiceid")
    uid = request.POST.get('uid')
    if request.method == "POST":
        if choiceid:
            choiceid = int(choiceid)
            # 返回结果为 分支选择id, 记录单分支传递信息id
        else:
            choiceid = None
        search_dict = searchMongoIndex(collection, choiceid)
        detail_list = serializermongodata(search_dict, collection_data)

        return return_render_listjson(code=1000, data=detail_list)
    else:
        return return_render_listjson(code=1001, msg="Method error")


def zip_yasuo(start_dir, end_dir):
    z = zipfile.ZipFile(end_dir, 'w', zipfile.ZIP_DEFLATED)
    for dir_path, dir_names, file_names in os.walk(start_dir):
        file_path = dir_path.replace(start_dir, '')
        file_path = file_path and file_path + os.sep or ''
        for filename in file_names:
            z.write(os.path.join(dir_path, filename), file_path+filename)
    z.close()
    return end_dir


def viewZip(request):
    x1 = "static.tar.gz"
    gzip_dir = "/data/project/media/static/yasuo/static.zip"
    sdata = "/data/project/media/static/game"
    # static_dir = "/static/yasuo/static.zip"
    zip_yasuo(sdata, gzip_dir)
    data = {
        'code': 200,
        "data": "http://192.168.1.254:8080/static/yasuo/static.zip"
    }
    # url = "http://192.168.1.254:8080/static/yasuo/static.zip"
    # return HttpResponseRedirect(reverse(url))
    return JsonResponse(data)


# 游戏设置
def gamesettings(request):
    if request.method == "POST":
        uid = request.POST.get('uid')
        bgm = request.POST.get('bgm')
        soundEffect = request.POST.get('soundEffect')
        dubbing = request.POST.get("dubbing")
        pass

# 保存记录，构造redis  chapter1-chapter2-chaper3-chapter4#节点id的hash 数据结构 KEY: idstory  HKEY: uidchapter
def saverecord(request):
    if request.method == "POST":
        uid = request.POST.get("uid")
        chapterid = request.POST.get("chapterid")
        createId = request.POST.get("createId")
        storyid = request.POST.get("storyid")
        story_key = storyid + "story"
        story_hkey = uid + "chapter"
        remeberdata = redis_r.hget(story_key, story_hkey)
        if remeberdata:
            remeberdata_str = remeberdata.decode()
            # remeberid = remeberdata_str.split("#")[1]
            remember_chapterid_str = remeberdata_str.split("#")[0]
            chapter_set = set(remember_chapterid_str.split("-"))
            chapter_set.add(str(chapterid))
            chapter_str = "-".join(chapter_set)
            newdata = chapter_str + "#" + str(createId)
            redis_r.hset(story_key, story_hkey, newdata)
        return return_render_dictjson(code=1000)

