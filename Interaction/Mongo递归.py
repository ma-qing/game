# -*- coding: utf-8 -*-
import json

import pymongo
'''
任务： 将Json深层格式转为Monogodb数据， 规定每次上传数据和返回数据类型，以便下次查找数据
'''
data = [
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
                                                                                    "label": "nodeChoice",
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
                                                                                                                    "label": "narrator",
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
{
                                                                                            "id": 17,
                                                                                            "label": "视频页",
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
            },
]

client = pymongo.MongoClient(host="localhost", port=27017)
db = client['test']
collection = db['JsonInfo']
collection_data = db["JsonData"]

Intranet_client = pymongo.MongoClient(host="192.168.1.254", port=27017)
Intranet_db = Intranet_client['test']
Intranet_collection = Intranet_db['JsonInfo']
Intranet_collection_data = Intranet_db["JsonData"]

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

def insert2mongo(collection, dicts, record_list):
    id = dicts.get('id')
    children = dicts.get("children")
    # 节点最后没有children
    record_list.append(id)
    # 当没有节点数据时候将其存入Monogo中
    if children == None or len(children) == 0:
        collection.insert_one({"startid": record_list[0], "chain": record_list})
    elif len(children) == 1:
        childrendicts = children[0]
        insert2mongo(collection, childrendicts, record_list)
    else:
        # 如果遍历到交叉节点,那么把这个数据存入数据库
        collection.insert_one({"startid": record_list[0], "chain": record_list})
        record_list = []
        for dicts in children:
            # 这里相当于是多个进程处理每个分支下的数据
            insert2mongo(collection, dicts, [])


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

# # 章首页
# data_insert1 = {
#     "createId": 1,
#     "chapter": 1,
#     "commandType": 0,
#     "bgimg": "",
#     "bgm": {
#             "storage": "",
#             "starttime": "",
#             
#             "loop": False,
#         },
#     "seffect": [{
#             "storage": "",
#             "starttime": "",
#             "seffectEndtime": 0.0,
#         }],
#     "narrator": {
#             "content": "",
#             "starttime": "",
#             "duration": 0.0,
#         },
#
#     "avatar": {
#             "storage": "",
#             "position": "",
#         },
#     "cutscenes": {
#
#
#         "screenDark": False,
#
#         "openEyes": False,
#     },
#     "special":{
#             "Snowing": False,
#             "raining": False,
#             "zoomIn": False,
#         },
#     "dialogue": {
#         "starttime": "",
#
#         "content": {
#             "name": "",
#             "speak": "",
#         }
#     },
#     "nodeChoice": [
#             {
#                 "createId": 0,
#                 # 文字大小颜色配置， 背景色配置
#                 'content': "",
#                 "position": "",
#
#             },
#
#         ],
#     "sceneDuration": "2.0",
#         "autoplay": True,
#
# }

# 酒吧街背景页
data_insert2 = {
    "createId": 2,
    "chapter": 1,
    "commandType": 1,
    "bgimg": "/barStreet.jpg",
    "bgm": {
            "storage": "/bgm_barStreet.mp3",
            "starttime": "",
            "loop": True,
        },
    "seffect": [{
            "storage": "",
            "starttime": "",
        },],
    "narrator": {
            "content": "深秋, 晚上11点11分，酒吧街",
            "starttime": "",
            "duration": 0.0,
        },

    "avatar": {
            "storage": "",
            "position": "",
        },
    "cutscenes": {
        
        
        "screenDark": False,
        "openEyes": False,
    },
    "special":{
            "Snowing": False,
            "raining": False,
            "zoomIn": False,
        },
    "dialogue": {
        "starttime": "",
        "content": {
            "name": "",
            "speak": "深秋, 晚上11点11分，酒吧街",
        }
    },
    "nodeChoice": [
            {
                "createId": 0,
                # 文字大小颜色配置， 背景色配置
                'content': "",
                "position": "",

            },

        ],
    "sceneDuration": "2.0",
        "autoplay": True,
}
# 出租车内张连
data_insert3 = {
        "createId": 3,
        "chapter": 1,
        "commandType": 2,
        "bgimg": "/car.jpg",
        "bgm": {
            "storage": "/bgm_barStreet.mp3",
            "starttime": "",
            "loop": False,
        },
        "seffect": [{
            "storage": "/effect_closeOrder.mp3",
            "starttime": "1.2",
        },
        ],
        "narrator": {
            "content": "",
            "starttime": "",
            "duration": 0.0,
        },

        "avatar": {
            "storage": "/zhanglian.png",
           "position": "左",
        },
        "cutscenes": {
            
            
            "screenDark": False,
            
            "openEyes": False,
        },
        "special":{
            "Snowing": False,
            "raining": False,
            "zoomIn": False,
        },
    "dialogue": {
            "starttime": "",
            
            "content": {
                "name": "张连",
                "speak": "呼~终于结束了，该回去了！结束接单！",
            }
        },
        "nodeChoice": [
            {
                "createId": 0,
                # 文字大小颜色配置， 背景色配置
                'content': "",
                "position": "",

            },

        ],
        "sceneDuration": "2.0",
        "autoplay": True,
    }
# 出租车内张连
data_insert4 = {
        "createId": 4,
        "chapter": 1,
        "commandType": 2,
        "bgimg": "/car.jpg",
        "bgm": {
            "storage": "",
            "starttime": "",
            
            "loop": False,
        },
        "seffect": [
        {
            "storage": "/effect_beatCar.WAV",
            "starttime": "",
        },
            {
            "storage": "/effect_pullCarDoor.WAV",
            "starttime": "1.0",
        },
        ],
        "narrator": {
            "content": "",
            "starttime": "",
            "duration": 0.0,
        },

        "avatar": {
            "storage": "/zhanglian.png",
           "position": "左",
        },
        "cutscenes": {
            
            "screenDark": False,
            
            "openEyes": False,
        },
        "special":{
            "Snowing": False,
            "raining": False,
            "zoomIn": False,
        },
    "dialogue": {
            "starttime": "0.5",
            
            "content": {
                "name": "张连",
                "speak": "！！是谁？？！！",
            }
        },
"nodeChoice": [
            {
                "createId": 0,
                # 文字大小颜色配置， 背景色配置
                'content': "",
                "position": "",

            },

        ],
        "sceneDuration": "2.0",
        "autoplay": True,
    }

# 陌生女人
data_insert5 = {
        "createId": 5,
        "chapter": 1,
        "commandType": 2,
        "bgimg": "/barStreet.jpg",
        "bgm": {
            "storage": "",
            "starttime": "",
            
            "loop": False,
        },
        "seffect": [{
            "storage": "/effect_closeCar.mp3",
            "starttime": "",
        },],
        "narrator": {
            "content": "",
            "starttime": "",
            "duration": 0.0,
        },

        "avatar": {
            "storage": "/girl.png",
           "position": "左",
        },
        "cutscenes": {
            
            
            "screenDark": False,
            
            "openEyes":False,
        },
        "special":{
            "Snowing": False,
            "raining": False,
            "zoomIn": False,
        },
    "dialogue": {
            "starttime": "",
            
            "content": {
                "name": "陌生女人",
                "speak": "师…师傅，走哇！",
            }
        },
"nodeChoice": [
            {
                "createId": 0,
                # 文字大小颜色配置， 背景色配置
                'content': "",
                "position": "",

            }
        ],
        "sceneDuration": "2.0",
        "autoplay": True,
    }
# 出租车内张连
data_insert6 = {
        "createId": 6,
        "chapter": 1,
        "commandType": 2,
        "bgimg": "/car.jpg",
        "bgm": {
            "storage": "",
            "starttime": "",
            
            "loop": False,
        },
        "seffect": [{
            "storage": "",
            "starttime": "",
        },],
        "narrator": {
            "content": "",
            "starttime": "",
            "duration": 0.0,
        },

        "avatar": {
            "storage": "/zhanglian.png",
           "position": "左",
        },
        "cutscenes": {
            
            
            "screenDark": False,
            
            "openEyes":False,
        },
        "special":{
            "Snowing": False,
            "raining": False,
            "zoomIn": False,
        },
    "dialogue": {
            "starttime": "",
            
            "content": {
                "name": "张连",
                "speak": "收工了，您换车吧！",
            }
        },
"nodeChoice": [
            {
                "createId": 0,
                # 文字大小颜色配置， 背景色配置
                'content': "",
                "position": "",

            }
        ],
        "sceneDuration": "2.0",
        "autoplay": True,
    }


# 陌生女人
data_insert7 = {
        "createId": 7,
        "chapter": 1,
        "commandType": 2,
        "bgimg": "/car.jpg",
        "bgm": {
            "storage": "",
            "starttime": "",
            
            "loop": False,
        },
        "seffect": [{
            "storage": "",
            "starttime": "",
        },],
        "narrator": {
            "content": "",
            "starttime": "",
            "duration": 0.0,
        },

        "avatar": {
            "storage": "/girl.png",
           "position": "左",
        },
        "cutscenes": {
            
            
            "screenDark": False,
            
            "openEyes":False,
        },
        "special":{
            "Snowing": False,
            "raining": False,
            "zoomIn": False,
        },
    "dialogue": {
            "starttime": "",
            
            "content": {
                "name": "陌生女人",
                "speak": "轻微的鼾声"
            }
        },
"nodeChoice": [
            {
                "createId": 0,
                # 文字大小颜色配置， 背景色配置
                'content': "",
                "position": "",

            }
        ],
        "sceneDuration": "2.0",
        "autoplay": True,
    }

# 出租车内张连
data_insert8 = {
        "createId": 8,
        "chapter": 1,
        "commandType": 2,
        "bgimg": "/car.jpg",
        "bgm": {
            "storage": "",
            "starttime": "",
            
            "loop": False,
        },
        "seffect": [{
            "storage": "",
            "starttime": "",
        },],
        "narrator": {
            "content": "",
            "starttime": "",
            "duration": 0.0,
        },

        "avatar": {
            "storage": "/zhanglian.png",
           "position": "左",
        },
        "cutscenes": {
            
            
            "screenDark": False,
            
            "openEyes":False,
        },
        "special":{
            "Snowing": False,
            "raining": False,
            "zoomIn": False,
        },
    "dialogue": {
            "starttime": "",
            
            "content": {
                "name": "张连",
                "speak": "睡、睡着了？！喂，喂，醒醒！",
            }
        },
"nodeChoice": [
            {
                "createId": 0,
                # 文字大小颜色配置， 背景色配置
                'content': "",
                "position": "",

            }
        ],
        "sceneDuration": "2.0",
        "autoplay": True,
    }

# 出租车内张连
data_insert9 = {
        "createId": 9,
        "chapter": 1,
        "commandType": 2,
        "bgimg": "/car.jpg",
        "bgm": {
            "storage": "",
            "starttime": "",
            
            "loop": False,
        },
        "seffect": [{
            "storage": "",
            "starttime": "",
        }],
        "narrator": {
            "content": "",
            "starttime": "",
            "duration": 0.0,
        },

        "avatar": {
            "storage": "/zhanglian.png",
           "position": "左",
        },
        "cutscenes": {
            
            
            "screenDark": False,
            
            "openEyes":False,
        },
        "special":{
            "Snowing": False,
            "raining": False,
            "zoomIn": False,
        },
    "dialogue": {
            "starttime": "",
            
            "content": {
                "name": "张连",
                "speak": "睡得真够死的！这人真是……至少说一声去哪儿呀！怎么办好呢？",
            }
        },
"nodeChoice": [
            {
                "createId": 0,
                # 文字大小颜色配置， 背景色配置
                'content': "",
                "position": "",

            },
        ],
        "sceneDuration": "2.0",
        "autoplay": True,
    }

# 出租车内选择
data_insert10 = {
        "createId": 10,
        "chapter": 1,
        "commandType": 3,
        "bgimg": "/car.jpg",

        "bgm": {
            "storage": "",
            "starttime": "",
            
            "loop": False,
        },
        "seffect": [{
            "storage": "",
            "starttime": "",
        }],
        "narrator": {
            "content": "",
            "starttime": "",
            "duration": 0.0,
        },
        # 头像
        "avatar": {
            "storage": "",
            "position": "",
        },
        "cutscenes": {
            
            
            "screenDark": False,
            
            "openEyes":False,
        },
        "special":{
            "Snowing": False,
            "raining": False,
            "zoomIn": False,
        },
    "dialogue": {
            "starttime": "",
            
            "content": {
                "name": "",
                "speak": "",
            }
        },

        "nodeChoice": [
            {
                "createId": 11,
                # 文字大小颜色配置， 背景色配置
                'content': "唉，我还是等她醒来再说吧！",
               "position": "中",

            },
            {
                "createId": 16,
                'content': "算了，我先往家开吧！",
               "position": "中",
            },
        ],
        "sceneDuration": "2.0",
        "autoplay": False,
}

# 出租车内张连
data_insert11 = {
        "createId": 11,
        "chapter": 1,
        "commandType": 2,
        "bgimg": "/car.jpg",
        "bgm": {
            "storage": "/bgm_car.mp3",
            "starttime": "",
            
            "loop": False,
        },
        "seffect": [{
            "storage": "",
            "starttime": "",
        }],
        "narrator": {
            "content": "",
            "starttime": "",
            "duration": 0.0,
        },

        "avatar": {
            "storage": "/zhanglian.png",
           "position": "左",
        },
        "cutscenes": {
            
            
            "screenDark": False,
            
            "openEyes":False,
        },
        "special":{
            "Snowing": False,
            "raining": False,
            "zoomIn": False,
        },
    "dialogue": {
            "starttime": "",
            
            "content": {
                "name": "张连",
                "speak": "唉，我还是等她醒过来吧！这得等到什么时候去啊…唉…",
            }
        },
"nodeChoice": [
            {
                "createId": 0,
                # 文字大小颜色配置， 背景色配置
                'content': "",
                "position": "",

            },
        ],
        "sceneDuration": "2.0",
        "autoplay": True,
    }


# 陌生女人
data_insert12 = {
        "createId": 12,
        "chapter": 1,
        "commandType": 2,
        "bgimg": "/car.jpg",
        "bgm": {
            "storage": "",
            "starttime": "",
            
            "loop": False,
        },
        "seffect": [{
            "storage": "",
            "starttime": "",
        },],
        "narrator": {
            "content": "",
            "starttime": "",
            "duration": 0.0,
        },

        "avatar": {
            "storage": "/girl.png",
           "position": "左",
        },
        "cutscenes": {
            
            
            "screenDark": False,
            
            "openEyes":True,
        },
        "special":{
            "Snowing": False,
            "raining": False,
            "zoomIn": False,
        },
    "dialogue": {
            "starttime": "",
            
            "content": {
                "name": "陌生女人",
                "speak": "这…我在哪儿？",
            }
        },
"nodeChoice": [
            {
                "createId": 0,
                # 文字大小颜色配置， 背景色配置
                'content': "",
                "position": "",

            }
        ],
        "sceneDuration": "2.0",
        "autoplay": True,
    }


# 酒吧街背景页
# 酒吧街背景页
data_insert13 = {
    "createId": 13,
    "chapter": 1,
    "commandType": 1,
    "bgimg": "/barStreet.jpg",
    "bgm": {
            "storage": "/bgm_barStreet.mp3",
            "starttime": "",
            
            "loop": True,
        },
    "seffect": [{
            "storage": "",
            "starttime": "",
        },],
    "narrator": {
            "content": "车窗外，深夜的酒吧街还是灯红酒绿。但是下起了雨。",
            "starttime": "",
            "duration": 0.0,
        },

    "avatar": {
            "storage": "",
            "position": "",
        },
    "cutscenes": {
        
        
        "screenDark": False,
        
        "openEyes": False,
    },

    "special":{
            "Snowing": False,
            "raining": False,
            "zoomIn": False,
        },
    "dialogue": {
        "starttime": "",
        "content": {
            "name": "",
            "speak": "车窗外，深夜的酒吧街还是灯红酒绿。但是下起了雨。",
        }
    },
    "nodeChoice": [
            {
                "createId": 0,
                # 文字大小颜色配置， 背景色配置
                'content': "",
                "position": "",

            },

        ],
    "sceneDuration": "2.0",
        "autoplay": True,
}

# 出租车内张连
data_insert14 = {
        "createId": 14,
        "chapter": 1,
        "commandType": 2,
        "bgimg": "/car.jpg",
        "bgm": {
            "storage": "/bgm_car.mp3",
            "starttime": "",
            
            "loop": False,
        },
        "seffect": [{
            "storage": "",
            "starttime": "",
        },],
        "narrator": {
            "content": "",
            "starttime": "",
            "duration": 0.0,
        },

        "avatar": {
            "storage": "/zhanglian.png",
           "position": "左",
        },
        "cutscenes": {
            
            
            "screenDark": False,
            
            "openEyes":False,
        },


"special":{
            "Snowing": False,
            "raining": False,
            "zoomIn": False,
        },
    "dialogue": {
            "starttime": "",
            
            "content": {
                "name": "张连",
                "speak": "唉，你总算是醒了！",
            }
        },
"nodeChoice": [
            {
                "createId": 0,
                # 文字大小颜色配置， 背景色配置
                'content': "",
                "position": "",

            },
        ],
        "sceneDuration": "2.0",
        "autoplay": True,
    }

# 陌生女人
data_insert15 = {
        "createId": 15,
        "chapter": 1,
        "commandType": 2,
        "bgimg": "/car.jpg",
        "bgm": {
            "storage": "",
            "starttime": "",
            
            "loop": False,
        },
        "seffect": [{
            "storage": "",
            "starttime": "",
        }],
        "narrator": {
            "content": "",
            "starttime": "",
            "duration": 0.0,
        },

        "avatar": {
            "storage": "/girl.png",
           "position": "左",
        },
        "cutscenes": {
            
            "screenDark": False,
            "openEyes": True,
        },
        "special":{
            "Snowing": False,
            "raining": False,
            "zoomIn": False,
        },
    "dialogue": {
            "starttime": "",
            "content": {
                "name": "陌生女人",
                "speak": "那个，请问你是…?",
            }
        },
"nodeChoice": [
            {
                "createId": 0,
                # 文字大小颜色配置， 背景色配置
                'content': "",
                "position": "",

            },
        ],
        "sceneDuration": "2.0",
        "autoplay": True,
    }

# 出租车内张连
data_insert16 = {
        "createId": 16,
        "chapter": 1,
        "commandType": 2,
        "bgimg": "/car.jpg",
        "bgm": {
            "storage": "/bgm_car.mp3",
            "starttime": "",
            
            "loop": False,
        },
        "seffect": [{
            "storage": "",
            "starttime": "",
        }],
        "narrator": {
            "content": "",
            "starttime": "",
            "duration": 0.0,
        },

        "avatar": {
            "storage": "/zhanglian.png",
           "position": "左",
        },
        "cutscenes": {
            
            
            "openEyes": False,
            "screenDark": True,

        },
        "special":{
            "Snowing": False,
            "raining": False,
            "zoomIn": False,
        },
    "dialogue": {
            "starttime": "",
            "content": {
                "name": "张连",
                "speak": "算了，我还是先往家开吧！",
            }
        },
"nodeChoice": [
            {
                "createId": 0,
                # 文字大小颜色配置， 背景色配置
                'content': "",
                "position": "",

            },
        ],
        "sceneDuration": "2.0",
        "autoplay": True,
    }


if __name__ == '__main__':
    def changejson(dicts):
        dicts["bgmStorage"] = dicts.get("bgm").get("storage")
        # dicts["bgmStarttime"] = dicts.get("bgm").get("starttime")
        # dicts["bgmEndtime"] = dicts.get("bgm").get("endtime")
        dicts["bgmLoop"] = dicts.get("bgm").get("loop")
        dicts["bgmStorage"] = dicts.get("bgm").get("storage")
        dicts.pop("bgm")
        # dicts["narratorContent"] = dicts.get('narrator').get("content")
        # dicts["narratorStarttime"] = dicts.get('narrator').get("starttime")
        # dicts["narratorDuration"] = dicts.get('narrator').get("duration")
        dicts.pop('narrator')

        dicts["avatarStorage"] = dicts.get('avatar').get("storage")
        dicts["avatarPosition"] = dicts.get('avatar').get("position")
        dicts.pop("avatar")

        dicts["screenDark"] = dicts.get("cutscenes").get("screenDark")
        # dicts["bgmGradually"] = dicts.get("cutscenes").get("bgmGradually")
        # dicts["bgmFades"] = dicts.get("cutscenes").get("bgmFades")
        # dicts["screenBrighter"] = dicts.get("cutscenes").get("screenBrighter")
        dicts["openEyes"] = dicts.get("cutscenes").get("openEyes")
        dicts.pop("cutscenes")

        dicts["snowing"] = dicts.get("special").get("Snowing")
        dicts["raining"] = dicts.get("special").get("raining")
        dicts["zoomIn"] = dicts.get("special").get("zoomIn")
        dicts.pop("special")

        dicts["dialogueStarttime"] = dicts["dialogue"].get("starttime")
        # dicts["dialogueDuration"] = dicts["dialogue"].get("duration")
        dicts["dialogueName"] = dicts["dialogue"].get("content").get("name")
        dicts["dialogueSpeak"] = dicts["dialogue"].get("content").get("speak")
        dicts.pop("dialogue")

        dicts['vedioStorage'] = ""
        dicts['vedioSkip'] = True

        # collection_data.insert_one(dicts)
        Intranet_collection_data.insert_one(dicts)

    changejson(data_insert2)
    changejson(data_insert3)
    changejson(data_insert4)
    changejson(data_insert5)
    changejson(data_insert6)
    changejson(data_insert7)
    changejson(data_insert8)
    changejson(data_insert9)
    changejson(data_insert10)
    changejson(data_insert11)
    changejson(data_insert12)
    changejson(data_insert13)
    changejson(data_insert14)
    changejson(data_insert15)
    changejson(data_insert16)
    # insert2mongo(collection, data[0], [])







