import os
import time
import zipfile

import requests
from django.http import HttpResponse, JsonResponse, FileResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.views.decorators.gzip import gzip_page

from common.utils import recursiveMongodata, collection, collection_data, return_render_json, searchMongoIndex


# 两种存在问题: 如何更新数据， Json数据块写入Mongo中
# 第一种数据存储方式: 存父子节点


# def showconfig(request):
#     startime = time.time()
#     # 递归查询Mongo collection 中的分支节点与分支节点之间的ID
#     choiceid = request.POST.get("choiceid")
#     uid = request.POST.get('uid')
#     if request.method == "POST":
#         if choiceid:
#             choiceid = int(choiceid)
#             # 返回结果为 分支选择id, 记录单分支传递信息id
#             branch_list, record_list = recursiveMongodata(collection, choiceid, [])
#         else:
#             branch_list, record_list = recursiveMongodata(collection, 1, [])
#         detail_list = []
#         # 查询单分支id的配置信息
#         print(branch_list, record_list)
#         for recordid in record_list:
#             record = collection_data.find_one({"createId": recordid})
#             if record:
#                 record["_id"] = str(record.get("_id"))
#             detail_list.append(record)
#         endtime = time.time()
#
#         print("执行时间:", endtime-startime)
#         return return_render_json(code=1000, branch_list=branch_list, record_list=record_list, detail_list=detail_list)
#     else:
#         return return_render_json(code=1001, msg="Method error")

# 第二种、思路：存放链式和交叉节点
from game import settings
from game.settings import BASE_DIR


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
        detail_list = []
        if search_dict:
            chain_list = search_dict.get("chain")
            if chain_list:
                for chainid in chain_list:
                    # chainid = int(chainid)
                    detailconfig = collection_data.find_one({"createId": chainid})
                    if detailconfig:
                        detailconfig["_id"] = str(detailconfig.get("_id"))

                    detail_list.append(detailconfig)

        return return_render_json(code=1000, data=detail_list)
    else:
        return return_render_json(code=1001, msg="Method error")


# def compress_string(s):
#     import io, gzip
#     zbuf = io.StringIO()
#     zfile = gzip.GzipFile(mode='wb', compresslevel=6, fileobj=zbuf)
#     zfile.write(s)
#     zfile.close()
#     return zbuf.getvalue()

def zip_yasuo(start_dir, end_dir):

    z = zipfile.ZipFile(end_dir, 'w', zipfile.ZIP_DEFLATED)
    for dir_path, dir_names, file_names in os.walk(start_dir):
        file_path = dir_path.replace(start_dir, '')
        file_path = file_path and file_path + os.sep or ''
        for filename in file_names:
            z.write(os.path.join(dir_path, filename), file_path+filename)
    z.close()
    return end_dir


def viewGzip(request):
    x1 = "static.tar.gz"
    gzip_dir = os.path.join(settings.BASE_DIR, x1)
    sdata = "/data/project/media/static/game"
    import tarfile
    tar = tarfile.open(gzip_dir, "w:gz")
    tar.add(sdata, arcname="static")
    tar.close()

    file = open(gzip_dir, 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="%s"' % (x1)
    return response


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
