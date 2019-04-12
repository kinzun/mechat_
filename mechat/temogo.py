from pymongo import MongoClient

mgclient = MongoClient("127.0.0.1", 27017)
MONGO_DB = mgclient["chat_mess_room"]

# re = list(MONGO_DB.groups.find({}, {"_id": 0}))
# print(re)


# """
# color, full, feature为新添加的字段，执行update时，操作失败了。请问这个应该怎么写？
# """
# conn = pymongo.MongoClient(conf.mongodb["host"], conf.mongodb["port"])
# db = getattr(conn, conf.mongodb["dbname"])
# collection = getattr(db, "main")
# data = {}
# data['color'] = color
# data['full'] = color
# data['feature'] = feature
# collection.update({"_id": ObjectId(objectid)},
#                   {"$set": data)
#
# re = MONGO_DB.groups.find({}, {"_id": 0})
re = MONGO_DB.groups.find({})

# res = MONGO_DB.users.update_many({"name":"alexDSB"},{"$set":{"age":2}})

# MONGO_DB.groups.update_many({'msg_type': 'message'},{"$set":{"cur_time":'2019年3月27日星期三12:58:50'}})




# for i in re:
#     i.update()

    # i['cur_time'] = '2019年3月27日星期三12:58:50'

