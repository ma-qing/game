from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from common.utils import recursiveMongodata, collection, collection_data


def showconfig(request):
    branch_list, record_list = recursiveMongodata(collection, 1, [])
    detail_list = []
    for recordid in record_list:
        record = collection_data.find_one({"commandId": recordid})
        detail_list.append(record)
    data = {
        'code': 200,
        'branch_list': branch_list,
        'record_list': record_list,
        'detail': detail_list,
    }
    return JsonResponse(data)

