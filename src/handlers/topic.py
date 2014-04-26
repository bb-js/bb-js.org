#coding:utf-8
import json
import sqlite3
from datetime import datetime

import web

from models import User, Topic
from .base import bad_request, display_time

session = web.config._session

CACHE_USER = {}


class TopicHandler:
    def GET(self, pk=None):
        if pk:
            topic = Topic.get_by_id(pk)
            topic['created_time'] = display_time(topic['created_time'])
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
            topic['created_time'] = display_time(topic['created_time'])
            result.append(topic)
        return json.dumps(result)

    def POST(self):
        if not session.user or session.user.id is None:
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
            "created_time": display_time(topic_data.get('created_time')),
        }
        return json.dumps(result)

    def PUT(self, obj_id=None):
        data = web.data()
        print data

    def DELETE(self, obj_id=None):
        pass
