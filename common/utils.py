# -*- coding: utf-8 -*-
import json

import pymongo
import redis
from django.http import JsonResponse
from pymysql import connect

from common.CONSSTANTS import STARTID
from game import settings
from lib.config import DBNAME, HOST, USER, PASSWORD, MONGOHOST, Redis_Host


class Mysqlpython:
    def __init__(self,database=DBNAME,host=HOST,user=USER,
                 password=PASSWORD,port=3306,charset="utf8mb4"):
        self.host=host
        self.user=user
        self.password=password
        self.port=port
        self.database=database
        self.charset=charset

# 数据库连接方法:
    def open(self):
        self.db=connect(host=self.host,user=self.user,
                        password=self.password,port=self.port,
                        database=self.database,
                        charset=self.charset)
#游标对象
        self.cur=self.db.cursor()
#数据库关闭方法:
    def close(self):
        self.cur.close()
        self.db.close()
#数据库执行操作方法:
    def zhixing(self,sql,L=[]):
        try:
            self.open()
            self.cur.execute(sql,L)
            self.db.commit()
            print("ok")
        except Exception as e:
            self.db.rollback()
            print("Failed", e)
            self.close()
            return False
        self.close()
        return True

# 数据库查询所有操作方法:
    def readall(self,sql,L=[]):
        try:
            self.open()
            self.cur.execute(sql,L)
            result=self.cur.fetchall()
            return result
        except Exception as e:
            print("Failed",e)
        self.close()


# Mongo 连接
client = pymongo.MongoClient(host=MONGOHOST, port=27017)
db = client['test']
collection = db['JsonInfo']
collection_data = db['JsonData']


# 递归查询Mongo数据，返回节点信息
def recursiveMongodata(collection, startfather, record_list):
    searchele = collection.find({"createId": startfather})
    count = collection.count_documents({"createId": startfather})
    print("查询条数:", count)
    record_list.append(startfather)
    # 如果查询条数是一条，则继续迭代到分支出现
    if count == 1:
        for member in searchele:
            childrenid = member.get('childrenid')
            if childrenid and childrenid != "null":
                # 再次调用结果可能是其它几种判断类型, 也可能是自己
                print("进行了递归调用")
                lists, record_list = recursiveMongodata(collection, childrenid, record_list)

                # 记录 递归调用路径

                return lists, record_list
            else:
                print("查到了最后一级")
                lists = []
                dicts = {}
                dicts["childrenid"] = member.get("childrenid")
                dicts["childrenname"] = member.get("childrenname")
                lists.append(dicts)
                return lists, record_list
    # 如果一条都没查到说明到了节点末尾
    elif count == 0:
        print("出错？")
        lists = []
        return lists, record_list
    # 如果查出两条以及以上, 说明出现分支，停止查询，返回节点的查询结果
    else:
        lists = []
        for member in searchele:
            dicts = {}
            dicts["childrenid"] = member.get("childrenid")
            dicts["childrenname"] = member.get("childrenname")
            lists.append(dicts)
        return lists, record_list


# 从Monogo中存储第二种查询方式
# mongo 存储的数据格式:  startid, chain, crossnode
def searchMongoIndex(collection, searchid=None):
    if searchid:
        search_dict = collection.find_one({"startid": searchid})
    else:
        search_dict = collection.find_one({"startid": STARTID})
    return search_dict


# 返回 数据
def return_render_listjson(code=1000, msg="", data=[], *args, **kwargs):
    return_data = {
        "code": code,
        "msg": msg if settings.DEBUG else "",
        "data": data,
    }
    return JsonResponse(return_data)


def return_render_dictjson(code=1000, msg="", data={}, *args, **kwargs):
    return_data = {
        "code": code,
        "msg": msg if settings.DEBUG else "",
        "data": data,
    }
    return JsonResponse(return_data)


# redis数据库信息
def set_redis(db=0):
    host = Redis_Host
    port = 6379
    pool = redis.ConnectionPool(host=host, port=port, db=db)
    r = redis.StrictRedis(connection_pool=pool)
    return r
