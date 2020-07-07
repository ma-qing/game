import time

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
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
                        detailconfig["_id"] = str( detailconfig.get("_id"))
                    detail_list.append(detailconfig)

        return return_render_json(code=1000, data=detail_list)
    else:
        return return_render_json(code=1001, msg="Method error")


