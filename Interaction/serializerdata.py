# -*- coding: utf-8 -*-


# 序列化返回数据
def serializermongodata(search_dict, collection_data):
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
    return detail_list