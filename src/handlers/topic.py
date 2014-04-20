#coding:utf-8
import json
import sqlite3
from datetime import datetime

import web

from models import User, Topic
from .base import bad_request

session = web.config._session

CACHE_USER = {}


class TopicHandler:
    def GET(self, pk=None):
        if pk:
            topic = Topic.get_by_id(pk)
            return json.dumps(topic)

        topics = Topic.get_all()
        result = []
        for t in topics:
            topic = dict(t)
            try:
                user = CACHE_USER[t.owner_id]
            except KeyError:
                user = User.get_by_id(t.owner_id)
                CACHE_USER[t.owner_id] = user
            topic['owner_name'] = user.username
            result.append(topic)
        return json.dumps(result)

    def POST(self):
        if not session.user or not session.user.id:
            return bad_request('请先登录！')
        if session.user.username != 'the5fire':
            return bad_request('sorry，你没有创建权限')

        data = web.data()
        data = json.loads(data)

        topic_data = {
            "title": data.get('title'),
            "owner_id": session.user.id,
            "created_time": datetime.now(),
        }

        try:
            topic_id = Topic.create(**topic_data)
        except sqlite3.IntegrityError:
            return bad_request('你已创建过该名称!')

        result = {
            "id": topic_id,
            "title": topic_data.get('title'),
            "owner_id": session.user.id,
            "owner_name": session.user.username,
            "created_time": str(topic_data.get('created_time')),
        }
        return json.dumps(result)

    def PUT(self, obj_id=None):
        data = web.data()
        print data

    def DELETE(self, obj_id=None):
        pass
