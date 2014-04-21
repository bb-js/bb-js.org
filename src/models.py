#coding:utf-8
from pymongo import MongoClient


client = MongoClient('localhost', 27017)
db = client.bb_js_db


def get_next_id(name):
    name = 'counter_%s' % name
    ret = None
    try:
        ret = db.counters.find_and_modify(
            query={'_id': name},
            update={'$inc': {'seq': 1}},
            upsert=True
        )
    except TypeError as e:
        print e
        db.counters.insert(
            {
                "_id": name,
                "seq": 0
            }
        )
    if ret:
        return ret.get('seq')
    return 0


class DBManage(object):
    @classmethod
    def table(cls):
        return cls.__name__.lower()

    @classmethod
    def get_by_id(cls, id):
        id = int(id)
        obj = db[cls.table()].find_one({'_id': id})
        return obj

    @classmethod
    def get_all(cls):
        return [obj for obj in db[cls.table()].find()]

    @classmethod
    def create(cls, **model_dict):
        _id = get_next_id(cls.table())
        model_dict.update({
            '_id': _id,
            'id': _id,
        })
        return db[cls.table()].insert(model_dict)

    @classmethod
    def update(cls, **model_dict):
        query = {"_id": model_dict.pop('id')}
        return db[cls.table()].update(query, model_dict)

    @classmethod
    def delete(cls, id):
        query = {"_id": id}
        db[cls.table()].update(query, {'available': False})


class User(DBManage):
    id = None
    username = None
    password = None
    registed_time = None

    def to_json(self):
        return self.__dict__

    @classmethod
    def get_by_id(cls, id):
        obj = super(User, cls).get_by_id(id)
        instance = cls()
        obj.pop('password')
        obj.pop('registed_time')
        instance.__dict__ = obj
        return instance

    @classmethod
    def get_by_username_password(cls, username, password):
        query = {"username": username, "password": password}
        user = [obj for obj in db[cls.table()].find(query)]
        try:
            return user[0]
        except IndexError:
            return None


class Topic(DBManage):
    id = None
    title = None
    created_time = None
    owner = None


class Message(DBManage):
    id = None
    content = None
    top_id = None
    user_id = None
    reply_to = None

    @classmethod
    def get_by_topic(cls, topic_id):
        query = {
            "topic_id": topic_id
        }
        return [obj for obj in db[cls.table()].find(query)]
