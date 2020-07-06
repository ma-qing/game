from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from common.utils import recursiveMongodata, collection, collection_data, return_render_json


def showconfig(request):
    # 递归查询Mongo collection 中的分支节点与分支节点之间的ID
    choiceid = request.POST.get("choiceid")
    uid = request.POST.get('uid')
    if request.method == "POST":
        if choiceid:
            choiceid = int(choiceid)
            # 返回结果为 分支选择id, 记录单分支传递信息id
            branch_list, record_list = recursiveMongodata(collection, choiceid, [])
        else:
            branch_list, record_list = recursiveMongodata(collection, 1, [])
        detail_list = []
        # 查询单分支id的配置信息
        print(branch_list, record_list)
        for recordid in record_list:
            record = collection_data.find_one({"createId": recordid})
            if record:
                record["_id"] = str(record.get("_id"))
            detail_list.append(record)

        return return_render_json(code=1000, branch_list=branch_list, record_list=record_list, detail_list=detail_list)
    else:
        return return_render_json(code=1001, msg="Method error")

