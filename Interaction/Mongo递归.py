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
                        "label": "张连",
                        "children": [
                            {
                                "id": 4,
                                "label": "张连",
                                "children": [
                                        {
                                            "id": 5,
                                            "label": "陌生女人",
                                            "children": [
                                                {
                                                    "id": 6,
                                                    "label": "张连",
                                                    "children": [
                                                        {
                                                            "id": 7,
                                                            "label": "轻微鼾声",
                                                            "children": [
                                                                {
                                                                    "id": 8,
                                                                    "label": "张连",
                                                                    "children": [
                                                                        {
                                                                            "id": 9,
                                                                            "label": "张连",
                                                                            "children": [
                                                                                {
                                                                                    "id": 10,
                                                                                    "label": "节点选择",
                                                                                    "children": [
                                                                                        {
                                                                                            "id": 11,
                                                                                            "label": "陌生女人",
                                                                                            "children": [
                                                                                                {
                                                                                                    "id": 12,
                                                                                                    "label": "张连",
                                                                                                    "children": [
                                                                                                        {
                                                                                                            "id": 13,
                                                                                                            "label": "陌生女人",
                                                                                                            "children": [
                                                                                                                {
                                                                                                                    "id": 14,
                                                                                                                    "label": "旁白",
                                                                                                                    "children": [
                                                                                                                        {
                                                                                                                            "id": 15,
                                                                                                                            "label": "张连",
                                                                                                                            "children": [

                                                                                                                            ]
                                                                                                                        },
                                                                                                                    ]
                                                                                                                },
                                                                                                            ]
                                                                                                        },
                                                                                                    ]
                                                                                                },
                                                                                            ]
                                                                                        },
                                                                                        {
                                                                                            "id": 16,
                                                                                            "label": "陌生女人",
                                                                                            "children": [

                                                                                            ]
                                                                                        },
                                                                                    ]
                                                                                },
                                                                            ]
                                                                        },
                                                                    ]
                                                                },
                                                            ]
                                                        },
                                                    ]
                                                },
                                            ]
                                        },
                                ]
                            },
                        ]
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
# def insert2mongo(dicts):
#     id = dicts.get('id')
#     label = dicts.get('label')
#     children = dicts.get("children")
#     if children != None:
#         for i in children:
#             childrenname = i.get('label')
#             insert_dict = {
#                 "createId": id,
#                 "name": label,
#                 "childrenname": childrenname,
#                 "childrenid": i.get("id")
#             }
#             collection.insert_one(insert_dict)
#             insert2mongo(i)
#     else:
#         insert_dict = {
#             "createId": id,
#             "name": label,
#             "childrenname": "null",
#             "childrenid": "null",
#         }
#         collection.insert_one(insert_dict)

def insert2mongo(dicts, record_list):
    id = dicts.get('id')
    children = dicts.get("children")
    # 节点最后没有children
    record_list.append(id)
    # 当没有节点数据时候将其存入Monogo中
    if children == None or len(children) == 0:
        collection.insert_one({"startid": record_list[0], "chain": record_list})
    elif len(children) == 1:
        childrendicts = children[0]
        insert2mongo(childrendicts, record_list)
    else:
        # 如果遍历到交叉节点,那么把这个数据存入数据库
        collection.insert_one({"startid": record_list[0], "chain": record_list})
        record_list = []
        for dicts in children:
            # 这里相当于是多个进程处理每个分支下的数据
            insert2mongo(dicts, [])


# 递归查询Json数据
def recursiveJson(dicts):
    # list
    children = dicts.get("children")

    if len(children) == 0 or children == None:
        # 没有子节点在最后一层，取这层的id作为下一章的开始，或者整体结束
        get_chilren = []
    elif len(children) == 1:
        # 只有一个节点记录每层后继续调用first1search
        # collection.insert()
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
    "背景音乐": {
            "storage": "",
            "背景音乐开始时间": 0.0,
            "背景音乐结束时间": 0.0,
            "背景音乐循环": False,
        },
    "音效": [{
            "storage": "",
            "音效开始时间": 0.0,
            "音效结束时间": 0.0,
        }],
    "旁白": {
            "旁白内容": "",
            "旁白开始时间": 0.0,
            "旁白持续时间": 0.0,
        },

    "头像": {
            "storage": "",
            "position": (),
        },
    "过场效果": {
        "背景音乐渐入": False,
        "背景音乐渐出": False,
        "下雪": False,
        "下雨": False,
        "屏幕渐黑": False,
        "屏幕渐亮": False,
        "睁眼效果": False,
    },
    "特殊效果":{
            "下雪": False,
            "下雨": False,
            "画面放大": False,
        },
    "对话": {
        "对话开始时间": 0.0,
        "对话显示时间": 0,
        "对话内容": {
            "name": "",
            "speak": "",
        }
    },
    "节点选择": [
            {
                "createid": 0,
                # 文字大小颜色配置， 背景色配置
                'content': "",
                "position": (),

            },

        ],
    "场景持续时间": 2.0,
        "自动播放": True,

}

# 酒吧街背景页
data_insert2 = {
    "createId": 2,
    "chapter": 1,
    "commandType": "旁白",
    "背景图": "/酒吧街.jpg",
    "背景音乐": {
            "storage": "/酒吧街背景音乐.mp3",
            "背景音乐开始时间": 0.0,
            "背景音乐结束时间": 0.0,
            "背景音乐循环": True,
        },
    "音效": [{
            "storage": "",
            "音效开始时间": 0.0,
        },],
    "旁白": {
            "旁白内容": "深秋, 晚上11点11分，酒吧街",
            "旁白开始时间": 0.0,
            "旁白持续时间": 0.0,
        },

    "头像": {
            "storage": "",
            "position": (),
        },
    "过场效果": {
        "背景音乐渐入": False,
        "背景音乐渐出": False,
        "下雪": False,
        "下雨": False,
        "屏幕渐黑": False,
        "屏幕渐亮": False,
        "睁眼效果": False,
    },
    "特殊效果":{
            "下雪": False,
            "下雨": False,
            "画面放大": False,
        },
    "对话": {
        "对话开始时间": 0.0,
        "对话显示时间": 0,
        "对话内容": {
            "name": "",
            "speak": "",
        }
    },
    "节点选择": [
            {
                "createid": 0,
                # 文字大小颜色配置， 背景色配置
                'content': "",
                "position": (),

            },

        ],
    "场景持续时间": 2.0,
        "自动播放": True,
}
# 出租车内张连
data_insert3 = {
        "createId": 3,
        "chapter": 1,
        "commandType": "对话",
        "背景图": "/出租车内.jpg",
        "背景音乐": {
            "storage": "/酒吧街背景音乐.mp3",
            "背景音乐开始时间": 0.0,
            "背景音乐结束时间": 1.2,
            "背景音乐循环": False,
        },
        "音效": [{
            "storage": "停止接单.mp3",
            "音效开始时间": 1.2,
        },
        ],
        "旁白": {
            "旁白内容": "",
            "旁白开始时间": 0.0,
            "旁白持续时间": 0.0,
        },

        "头像": {
            "storage": "张连.png",
            "position": (0, 170),
        },
        "过场效果": {
            "背景音乐渐入": False,
            "背景音乐渐出": True,
            "下雪": True,
            "下雨": False,
            "屏幕渐黑": False,
            "屏幕渐亮": False,
            "睁眼效果": False,
        },
        "特殊效果":{
            "下雪": False,
            "下雨": False,
            "画面放大": False,
        },
    "对话": {
            "对话开始时间": 0.0,
            "对话显示时间": 0,
            "对话内容": {
                "name": "张连",
                "speak": "呼~终于结束了，该回去了！结束接单！",
            }
        },
        "节点选择": [
            {
                "createid": 0,
                # 文字大小颜色配置， 背景色配置
                'content': "",
                "position": (),

            },

        ],
        "场景持续时间": 2.0,
        "自动播放": True,
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
        "音效": [
        {
            "storage": "/拍门声.mp3",
            "音效开始时间": 0.0,
        },
            {
            "storage": "拉开车门声",
            "音效开始时间": 1.0,
        },
        ],
        "旁白": {
            "旁白内容": "",
            "旁白开始时间": 0.0,
            "旁白持续时间": 0.0,
        },

        "头像": {
            "storage": "张连.png",
            "position": (0, 170),
        },
        "过场效果": {
            "背景音乐渐入": False,
            "背景音乐渐出": True,
            "下雪": False,
            "下雨": False,
            "屏幕渐黑": False,
            "屏幕渐亮": False,
            "睁眼效果": False,
        },
        "特殊效果":{
            "下雪": False,
            "下雨": False,
            "画面放大": False,
        },
    "对话": {
            "对话开始时间": 0.5,
            "对话显示时间": 0,
            "对话内容": {
                "name": "张连",
                "speak": "！！是谁？？！！",
            }
        },
"节点选择": [
            {
                "createid": 0,
                # 文字大小颜色配置， 背景色配置
                'content': "",
                "position": (),

            },

        ],
        "场景持续时间": 2.0,
        "自动播放": True,
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
        "音效": [{
            "storage": "车门关闭声.mp3",
            "音效开始时间": 0.0,
        },],
        "旁白": {
            "旁白内容": "",
            "旁白开始时间": 0.0,
            "旁白持续时间": 0.0,
        },

        "头像": {
            "storage": "陌生女人.png",
            "position": (0, 170),
        },
        "过场效果": {
            "背景音乐渐入": False,
            "背景音乐渐出": False,
            "下雪": False,
            "下雨": False,
            "屏幕渐黑": False,
            "屏幕渐亮":False,
            "睁眼效果":False,
        },
        "特殊效果":{
            "下雪": False,
            "下雨": False,
            "画面放大": False,
        },
    "对话": {
            "对话开始时间": 0.0,
            "对话显示时间": 0,
            "对话内容": {
                "name": "陌生女人",
                "speak": "师…师傅，走哇！",
            }
        },
"节点选择": [
            {
                "createid": 0,
                # 文字大小颜色配置， 背景色配置
                'content': "",
                "position": (),

            }
        ],
        "场景持续时间": 2.0,
        "自动播放": True,
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
        "音效": [{
            "storage": "",
            "音效开始时间": 0.0,
        },],
        "旁白": {
            "旁白内容": "",
            "旁白开始时间": 0.0,
            "旁白持续时间": 0.0,
        },

        "头像": {
            "storage": "张连.png",
            "position": (0, 170),
        },
        "过场效果": {
            "背景音乐渐入": False,
            "背景音乐渐出": False,
            "下雪": False,
            "下雨": False,
            "屏幕渐黑": False,
            "屏幕渐亮":False,
            "睁眼效果":False,
        },
        "特殊效果":{
            "下雪": False,
            "下雨": False,
            "画面放大": False,
        },
    "对话": {
            "对话开始时间": 0.0,
            "对话显示时间": 0,
            "对话内容": {
                "name": "张连",
                "speak": "收工了，您换车吧！",
            }
        },
"节点选择": [
            {
                "createid": 0,
                # 文字大小颜色配置， 背景色配置
                'content': "",
                "position": (),

            }
        ],
        "场景持续时间": 2.0,
        "自动播放": True,
    }


# 陌生女人
data_insert7 = {
        "createId": 7,
        "chapter": 1,
        "commandType": "对话",
        "背景图": "/出租车内.jpg",
        "背景音乐": {
            "storage": "",
            "背景音乐开始时间": 0.0,
            "背景音乐结束时间": 0.0,
            "背景音乐循环": False,
        },
        "音效": [{
            "storage": "",
            "音效开始时间": 0.0,
        },],
        "旁白": {
            "旁白内容": "",
            "旁白开始时间": 0.0,
            "旁白持续时间": 0.0,
        },

        "头像": {
            "storage": "陌生女人.png",
            "position": (0, 170),
        },
        "过场效果": {
            "背景音乐渐入": False,
            "背景音乐渐出": False,
            "下雪": False,
            "下雨": False,
            "屏幕渐黑": False,
            "屏幕渐亮":False,
            "睁眼效果":False,
        },
        "特殊效果":{
            "下雪": False,
            "下雨": False,
            "画面放大": False,
        },
    "对话": {
            "对话开始时间": 0.0,
            "对话显示时间": 0,
            "对话内容": {
                "name": "陌生女人",
                "speak": "轻微的鼾声"
            }
        },
"节点选择": [
            {
                "createid": 0,
                # 文字大小颜色配置， 背景色配置
                'content': "",
                "position": (),

            }
        ],
        "场景持续时间": 2.0,
        "自动播放": True,
    }

# 出租车内张连
data_insert8 = {
        "createId": 8,
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
        "过场效果": {
            "背景音乐渐入": False,
            "背景音乐渐出": False,
            "下雪": False,
            "下雨": False,
            "屏幕渐黑": False,
            "屏幕渐亮":False,
            "睁眼效果":False,
        },
        "特殊效果":{
            "下雪": False,
            "下雨": False,
            "画面放大": False,
        },
    "对话": {
            "对话开始时间": 0.0,
            "对话显示时间": 0,
            "对话内容": {
                "name": "张连",
                "speak": "睡、睡着了？！喂，喂，醒醒！",
            }
        },
"节点选择": [
            {
                "createid": 0,
                # 文字大小颜色配置， 背景色配置
                'content': "",
                "position": (),

            }
        ],
        "场景持续时间": 2.0,
        "自动播放": True,
    }

# 出租车内张连
data_insert9 = {
        "createId": 9,
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
        "过场效果": {
            "背景音乐渐入": False,
            "背景音乐渐出": False,
            "下雪": False,
            "下雨": False,
            "屏幕渐黑": False,
            "屏幕渐亮":False,
            "睁眼效果":False,
        },
        "特殊效果":{
            "下雪": False,
            "下雨": False,
            "画面放大": False,
        },
    "对话": {
            "对话开始时间": 0.0,
            "对话显示时间": 0,
            "对话内容": {
                "name": "张连",
                "speak": "睡得真够死的！这人真是……至少说一声去哪儿呀！怎么办好呢？",
            }
        },
"节点选择": [
            {
                "createid": 0,
                # 文字大小颜色配置， 背景色配置
                'content': "",
                "position": (),

            },
        ],
        "场景持续时间": 2.0,
        "自动播放": True,
    }

# 出租车内选择
data_insert10 = {
        "createId": 10,
        "chapter": 1,
        "commandType": "选择",
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
            "storage": "",
            "position": "",
        },
        "过场效果": {
            "背景音乐渐入": False,
            "背景音乐渐出": False,
            "下雪": False,
            "下雨": False,
            "屏幕渐黑": False,
            "屏幕渐亮":False,
            "睁眼效果":False,
        },
        "特殊效果":{
            "下雪": False,
            "下雨": False,
            "画面放大": False,
        },
    "对话": {
            "对话开始时间": 0.0,
            "对话显示时间": 0,
            "对话内容": {
            }
        },
        "节点选择": [
            {
                "createid": 11,
                # 文字大小颜色配置， 背景色配置
                'content': "唉，我还是等她醒来再说吧！",
                "position": (250, 150),

            },
            {
                "createid": 16,
                'content': "算了，我先往家开吧！",
                "position": (250, 450),
            },
        ],
        "场景持续时间": 2.0,
        "自动播放": False,
}

# 出租车内张连
data_insert11 = {
        "createId": 11,
        "chapter": 1,
        "commandType": "对话",
        "背景图": "/出租车内.jpg",
        "背景音乐": {
            "storage": "车内音乐.mp3",
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
        "过场效果": {
            "场景渐入": False,
            "场景渐出": False,
            "下雪": False,
            "下雨": False,
            "屏幕渐黑": False,
            "屏幕渐亮":False,
            "睁眼效果":False,
        },
        "特殊效果":{
            "下雪": False,
            "下雨": False,
            "画面放大": False,
        },
    "对话": {
            "对话开始时间": 0.0,
            "对话显示时间": 0,
            "对话内容": {
                "name": "张连",
                "speak": "唉，我还是等她醒过来吧！这得等到什么时候去啊…唉…",
            }
        },
"节点选择": [
            {
                "createid": 0,
                # 文字大小颜色配置， 背景色配置
                'content': "",
                "position": (),

            },
        ],
        "场景持续时间": 2.0,
        "自动播放": True,
    }


# 陌生女人
data_insert12 = {
        "createId": 12,
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
            "storage": "陌生女人.png",
            "position": (0, 170),
        },
        "过场效果": {
            "场景渐入": False,
            "场景渐出": False,
            "下雪": False,
            "下雨": False,
            "屏幕渐黑": False,
            "屏幕渐亮":False,
            "睁眼效果":True,
        },
        "特殊效果":{
            "下雪": False,
            "下雨": False,
            "画面放大": False,
        },
    "对话": {
            "对话开始时间": 0.0,
            "对话显示时间": 0,
            "对话内容": {
                "name": "陌生女人",
                "speak": "这…我在哪儿？",
            }
        },
"节点选择": [
            {
                "createid": 0,
                # 文字大小颜色配置， 背景色配置
                'content': "",
                "position": (),

            }
        ],
        "场景持续时间": 2.0,
        "自动播放": True,
    }


# 酒吧街背景页
# 酒吧街背景页
data_insert13 = {
    "createId": 13,
    "chapter": 1,
    "commandType": "旁白",
    "背景图": "/酒吧街.jpg",
    "背景音乐": {
            "storage": "/酒吧街背景音乐.mp3",
            "背景音乐开始时间": 0.0,
            "背景音乐结束时间": 0.0,
            "背景音乐循环": True,
        },
    "音效": [{
            "storage": "",
            "音效开始时间": 0.0,
        },],
    "旁白": {
            "旁白内容": "车窗外，深夜的酒吧街还是灯红酒绿。但是下起了雨。",
            "旁白开始时间": 0.0,
            "旁白持续时间": 0.0,
        },

    "头像": {
            "storage": "",
            "position": (),
        },
    "过场效果": {
        "背景音乐渐入": False,
        "背景音乐渐出": False,
        "下雪": False,
        "下雨": False,
        "屏幕渐黑": False,
        "屏幕渐亮": False,
        "睁眼效果": False,
    },
    
    "特殊效果":{
            "下雪": False,
            "下雨": False,
            "画面放大": False,
        },
    "对话": {
        "对话开始时间": 0.0,
        "对话显示时间": 0,
        "对话内容": {
            "name": "",
            "speak": "",
        }
    },
    "节点选择": [
            {
                "createid": 0,
                # 文字大小颜色配置， 背景色配置
                'content': "",
                "position": (),

            },

        ],
    "场景持续时间": 2.0,
        "自动播放": True,
}

# 出租车内张连
data_insert14 = {
        "createId": 14,
        "chapter": 1,
        "commandType": "对话",
        "背景图": "/出租车内.jpg",
        "背景音乐": {
            "storage": "车内音乐.mp3",
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
        "过场效果": {
            "场景渐入": False,
            "场景渐出": False,
            "下雪": False,
            "下雨": False,
            "屏幕渐黑": False,
            "屏幕渐亮":False,
            "睁眼效果":False,
        },
        

"特殊效果":{
            "下雪": False,
            "下雨": False,
            "画面放大": False,
        },
    "对话": {
            "对话开始时间": 0.0,
            "对话显示时间": 0,
            "对话内容": {
                "name": "张连",
                "speak": "唉，你总算是醒了！",
            }
        },
"节点选择": [
            {
                "createid": 0,
                # 文字大小颜色配置， 背景色配置
                'content': "",
                "position": (),

            },
        ],
        "场景持续时间": 2.0,
        "自动播放": True,
    }

# 陌生女人
data_insert15 = {
        "createId": 15,
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
            "storage": "陌生女人.png",
            "position": (0, 170),
        },
        "过场效果": {
            "场景渐入": False,
            "场景渐出": False,
            "下雪": False,
            "下雨": False,
            "睁眼效果": True,
        },
        "特殊效果":{
            "下雪": False,
            "下雨": False,
            "画面放大": False,
        },
    "对话": {
            "对话开始时间": 0.0,
            "对话显示时间": 0,
            "对话内容": {
                "name": "陌生女人",
                "speak": "那个，请问你是…?",
            }
        },
"节点选择": [
            {
                "createid": 0,
                # 文字大小颜色配置， 背景色配置
                'content': "",
                "position": (),

            },
        ],
        "场景持续时间": 2.0,
        "自动播放": True,
    }

# 出租车内张连
data_insert16 = {
        "createId": 16,
        "chapter": 1,
        "commandType": "对话",
        "背景图": "/出租车内.jpg",
        "背景音乐": {
            "storage": "车内音乐.mp3",
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
        "过场效果": {
            "场景渐入": False,
            "场景渐出": False,
            "下雪": False,
            "下雨": False,
            "睁眼效果": False,
            "屏幕渐黑": True,

        },
        "特殊效果":{
            "下雪": False,
            "下雨": False,
            "画面放大": False,
        },
    "对话": {
            "对话开始时间": 0.0,
            "对话显示时间": 0,
            "对话内容": {
                "name": "张连",
                "speak": "算了，我还是先往家开吧！",
            }
        },
"节点选择": [
            {
                "createid": 0,
                # 文字大小颜色配置， 背景色配置
                'content': "",
                "position": (),

            },
        ],
        "场景持续时间": 2.0,
        "自动播放": True,
    }


if __name__ == '__main__':
    insert2mongo(data[0], [])
    # collection_data = db["JsonData"]
    # collection_data.insert_one(data_insert1)
    # collection_data.insert_one(data_insert2)
    # collection_data.insert_one(data_insert3)
    # collection_data.insert_one(data_insert4)
    # collection_data.insert_one(data_insert5)
    # collection_data.insert_one(data_insert6)
    # collection_data.insert_one(data_insert7)
    # collection_data.insert_one(data_insert8)
    # collection_data.insert_one(data_insert9)
    # collection_data.insert_one(data_insert10)
    # collection_data.insert_one(data_insert11)
    # collection_data.insert_one(data_insert12)
    # collection_data.insert_one(data_insert13)
    # collection_data.insert_one(data_insert14)
    # collection_data.insert_one(data_insert15)
    # collection_data.insert_one(data_insert16)


