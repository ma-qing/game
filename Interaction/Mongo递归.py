# -*- coding: utf-8 -*-
import pymongo
'''
任务： 将Json深层格式转为Monogodb数据， 规定每次上传数据和返回数据类型，以便下次查找数据
'''
data = [
    {
        "id": 1,
        "label": "第一章 捡了个姑娘",
        "children": [
            {
                "id": 2,
                "label": "酒吧街",
                "children": [
                    {
                        "id": 3,
                        "label": "出租车内"
                    },
                ]
            },
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
                "createId": id,
                "name": label,
                "childrenname": childrenname,
                "childrenid": i.get("id")
            }
            collection.insert_one(insert_dict)
            insert2mongo(i)
    else:
        insert_dict = {
            "createId": id,
            "name": label,
            "childrenname": "null",
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

# 章首页
data_insert1 = {
    "createId": 1,
    "chapter": 1,
    "commandType": "章首页",
    "背景图": "",
    "背景音乐": "",
    "背景音乐开始时间": 0,
    "背景音乐循环": False,
    "音效": "",
    "音效开始时间": 0,
    "音效结束时间": 0,
    "旁白": "",
    "旁白开始时间": 0,
    "头像": "",
    "头像位置": "",
    "动画效果": {
        "渐入": False,
        "渐出": False,
        "下雪": False,
        "下雨": False
    }
}
# 酒吧街背景页
data_insert2 = {
    "createId": 2,
    "chapter": 1,
    "commandType": "旁白",
    "背景图": "/酒吧街.jpg",
    "背景音乐": "/酒吧街背景音乐.mp3",
    "背景音乐开始时间": 0,
    "背景音乐循环": True,
    "音效": "",
    "音效开始时间": 0,
    "音效结束时间": 0,
    "旁白": "深秋, 晚上11点11分，酒吧街",
    "旁白开始时间": 0,
    "头像": "",
    "头像位置": "",
    "动画效果": {
        "场景渐入": False,
        "场景渐出": True,
        "下雪": False,
        "下雨": False
    },
    "场景持续时间": 2,
}
# 出租车内张连
data_insert3 = {
        "createId": 3,
        "chapter": 1,
        "commandType": "对话",
        "背景图": "/出租车内.jpg",
        "背景音乐": {
            "storage": "",
            "背景音乐开始时间": 0.0,
            "背景音乐结束时间": 0.0,
            "背景音乐循环": False,
        },
        "音效": {
            "storage": "停止接单.mp3",
            "音效开始时间": 1.2,
        },
        "旁白": {
            "旁白内容": "",
            "旁白开始时间": 0.0,
            "旁白持续时间": 0.0,
        },

        "头像": {
            "storage": "张连.png",
            "position": (0, 170),
        },
        "动画效果": {
            "背景音乐渐入": False,
            "背景音乐渐出": True,
            "下雪": True,
            "下雨": False,
        },
        "对话": {
            "对话开始时间": 0.0,
            "对话显示时间": 0,
            "对话内容": {
                "name": "张连",
                "speak": "呼~终于结束了，该回去了！结束接单！",
            }
        },
        "场景持续时间": 0.0,
    }
# 出租车内张连
data_insert4 = {
        "createId": 4,
        "chapter": 1,
        "commandType": "对话",
        "背景图": "/出租车内.jpg",
        "背景音乐": {
            "storage": "",
            "背景音乐开始时间": 0.0,
            "背景音乐结束时间": 0.0,
            "背景音乐循环": False,
        },
        "音效": {
            "storage": "拉开车门声",
            "音效开始时间": 1,
        },
        "旁白": {
            "旁白内容": "",
            "旁白开始时间": 0.0,
            "旁白持续时间": 0.0,
        },

        "头像": {
            "storage": "张连.png",
            "position": (0, 170),
        },
        "动画效果": {
            "背景音乐渐入": False,
            "背景音乐渐出": True,
            "下雪": False,
            "下雨": False,
        },
        "对话": {
            "对话开始时间": 0.0,
            "对话显示时间": 0,
            "对话内容": {
                "name": "张连",
                "speak": "！！是谁？？！！",
            }
        },
        "场景持续时间": 2,
    }

# 陌生女人
data_insert5 = {
        "createId": 5,
        "chapter": 1,
        "commandType": "对话",
        "背景图": "/酒吧背景.jpg",
        "背景音乐": {
            "storage": "",
            "背景音乐开始时间": 0.0,
            "背景音乐结束时间": 0.0,
            "背景音乐循环": False,
        },
        "音效": {
            "storage": "车门关闭声.mp3",
            "音效开始时间": 0.0,
        },
        "旁白": {
            "旁白内容": "",
            "旁白开始时间": 0.0,
            "旁白持续时间": 0.0,
        },

        "头像": {
            "storage": "陌生女人.png",
            "position": (0, 170),
        },
        "动画效果": {
            "背景音乐渐入": False,
            "背景音乐渐出": False,
            "下雪": False,
            "下雨": False,
        },
        "对话": {
            "对话开始时间": 0.0,
            "对话显示时间": 0,
            "对话内容": {
                "name": "陌生女人",
                "speak": "师…师傅，走哇！",
            }
        },
        "场景持续时间": 2,
    }
# 出租车内张连
data_insert6 = {
        "createId": 6,
        "chapter": 1,
        "commandType": "对话",
        "背景图": "/出租车内.jpg",
        "背景音乐": {
            "storage": "",
            "背景音乐开始时间": 0.0,
            "背景音乐结束时间": 0.0,
            "背景音乐循环": False,
        },
        "音效": {
            "storage": "",
            "音效开始时间": 0.0,
        },
        "旁白": {
            "旁白内容": "",
            "旁白开始时间": 0.0,
            "旁白持续时间": 0.0,
        },

        "头像": {
            "storage": "张连.png",
            "position": (0, 170),
        },
        "动画效果": {
            "背景音乐渐入": False,
            "背景音乐渐出": False,
            "下雪": False,
            "下雨": False,
        },
        "对话": {
            "对话开始时间": 0.0,
            "对话显示时间": 0,
            "对话内容": {
                "name": "张连",
                "speak": "收工了，您换车吧！",
            }
        },
        "场景持续时间": 2,
    }
if __name__ == '__main__':
    # insert2mongo(data[0])
    collection_data = db["JsonData"]
    collection_data.insert_one(data_insert1)
    collection_data.insert_one(data_insert2)
    collection_data.insert_one(data_insert3)
    collection_data.insert_one(data_insert4)
    collection_data.insert_one(data_insert5)
    collection_data.insert_one(data_insert6)


