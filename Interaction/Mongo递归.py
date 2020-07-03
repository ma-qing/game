# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import pymongo
'''
任务： 将Json深层格式转为Monogodb数据， 规定每次上传数据和返回数据类型，以便下次查找数据
'''
data = [
    {
        "id": 1,
        "label": "一级 1",
        "children": [
            {
                "id": 4,
                "label": "二级 1-1",
                "children": [
                    {
                        "id": 9,
                        "label": "三级 1-1-1"
                    },
                    {
                        "id": 10,
                        "label": "三级 1-1-2"
                    }
                ]
            },
            {
                "id": 2,
                "label": "一级 2",
                "children": [
                    {
                        "id": 5,
                        "label": "二级 2-1"
                    },
                    {
                        "id": 6,
                        "label": "二级 2-2"
                    },
                    {
                        "id": 3,
                        "label": "一级 3",
                        "children": [
                            {
                                "id": 7,
                                "label": "二级 3-1"
                            },
                            {
                                "id": 8,
                                "label": "二级 3-2",
                                "children": [
                                    {
                                        "id": 11,
                                        "label": "三级 3-2-1"
                                    },
                                    {
                                        "id": 12,
                                        "label": "三级 3-2-2"
                                    },
                                    {
                                        "id": 13,
                                        "label": "三级 3-2-3"
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    }
]

client = pymongo.MongoClient(host="localhost", port=27017)
db = client['test']
collection = db['JsonInfo']


# Json 数据导入Mongo collection 中
def insert2mongo(dicts):
    id = dicts.get('id')
    label = dicts.get('label')
    children = dicts.get("children")
    if children != None:
        for i in children:
            childrenname = i.get('label')
            insert_dict = {
                "recordid": id,
                "name": label,
                "children": childrenname,
                "childrenid": i.get("id")
            }
            collection.insert_one(insert_dict)
            insert2mongo(i)
    else:
        insert_dict = {
            "recordid": id,
            "name": label,
            "children": "null",
            "childrenid": "null",
        }
        collection.insert_one(insert_dict)


# 递归查询Json数据
def recursiveJson(dicts):
    # list
    children = dicts.get("children")

    if len(children) == 0 or children == None:
        # 没有子节点在最后一层，取这层的id作为下一章的开始，或者整体结束
        get_chilren = []
    elif len(children) == 1:
        # 只有一个节点记录每层后继续调用first1search
        collection.insert()
        get_chilren = recursiveJson(children[0])
    else:
        # 节点分支，返回分支数据
        get_chilren = children
    return get_chilren


# 递归查询Mongo数据，返回节点信息
def recursiveMongodata(startfather, record_list):
    searchele = collection.find({"recordid": startfather})
    count = collection.count_documents({"recordid": startfather})
    print("查询条数:", count)
    record_list.append(startfather)
    # 如果查询条数是一条，则继续迭代到分支出现
    if count == 1:
        for member in searchele:
            childrenid = member.get('childrenid')
            if childrenid and childrenid != "null":
                # 再次调用结果可能是其它几种判断类型, 也可能是自己
                print("进行了递归调用")
                lists, record_list = recursiveMongodata(childrenid, record_list)

                # 记录 递归调用路径
                return lists, record_list
            else:
                print("查到了最后一级")
                lists = []
                lists.append(member)
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
            lists.append(member)
        return lists, record_list


data_insert = {
        "commandId": 2,
        "chapter": 1,
        "commandType": "对话",
        "targetid": 2,
        "背景图": "/cba.png",
        "背景音乐": "/abc.mp3",
        "背景音乐开始时间": 1,
        "音效": None,
        "音效开始时间": 0.3,
        "旁白": None,
        "旁白开始时间": 0.8,
        "头像": "null & path",
        "头像位置": "左&中&右",
        "动画效果": {
            "渐亮 - 淡入": True,
            "渐黑 - 淡出": False,
            "下雪": True,
            "下雨": False,
            "睁眼": True,
            "微放大": False,
            "抖动": True
        },

    "对话": [
        {
            'name': "张连",
            "speak": "巴啦啦能量！"
        },
        {
            "name": "陌生女人",
            "speak": "古娜拉黑暗之神",
        },

    ]

    }

if __name__ == '__main__':
    print(recursiveMongodata(3, []))
