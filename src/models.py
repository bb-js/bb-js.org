#coding:utf-8
from web import Storage
from pymongo import MongoClient
import markdown


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
    except TypeError:
        db.counters.insert(
            {
                "_id": name,
                "seq": 0
            }
        )
    if ret:
        return ret.get('seq')
    return 0


class class_property(object):
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, klass):
        return self.func(klass)


class DBManage(object):
    @class_property
    def table(cls):
        return cls.__name__.lower()

    @classmethod
    def get_by_id(cls, id):
        id = int(id)
        obj = db[cls.table].find_one({'_id': id})
        return Storage(**obj)

    @classmethod
    def get_all(cls):
        return [Storage(**obj) for obj in db[cls.table].find().sort("_id", -1)]

    @classmethod
    def create(cls, **model_dict):
        _id = get_next_id(cls.table)
        model_dict.update({
            '_id': _id,
            'id': _id,
        })
        return db[cls.table].insert(model_dict)

    @classmethod
    def update(cls, **model_dict):
        query = {"_id": model_dict.pop('id')}
        return db[cls.table].update(query, model_dict)

    @classmethod
    def delete(cls, id):
        query = {"_id": id}
        db[cls.table].update(query, {'available': False})


class User(DBManage):
    id = None
    username = None
    password = None
    registed_time = None

    @classmethod
    def get_by_id(cls, id):
        obj = super(User, cls).get_by_id(id)
        obj.pop('password')
        obj.pop('registed_time')
        return obj

    @classmethod
    def get_by_username_password(cls, username, password):
        query = {"username": username, "password": password}
        user = [Storage(obj) for obj in db[cls.table].find(query)]
        try:
            obj = user[0]
        except IndexError:
            return None
        obj.pop('password')
        obj.pop('registed_time')
        return obj


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
    def topic_count(cls, topic_id):
        query = {
            "topic_id": topic_id
        }
        return db[cls.table].find(query).count()

    @classmethod
    def get_latest_by_topic(cls, topic_id):
        query = {
            "topic_id": topic_id
        }
        result = db[cls.table].find_one(query)
        if result:
            return Storage(result)

    @classmethod
    def get_by_topic(cls, topic_id):
        query = {
            "topic_id": topic_id
        }
        return [obj for obj in db[cls.table].find(query)]

    @classmethod
    def create(cls, **model_dict):
        raw_content = model_dict.pop('content')
        # markdown处理
        content = markdown.markdown(raw_content, safe_mode=True)
        model_dict.update({
            'content': content,
            'raw_content': raw_content
        })
        return super(Message, cls).create(**model_dict)
