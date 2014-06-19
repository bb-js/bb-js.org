#coding:utf-8
import json
import sqlite3
from datetime import datetime

import web

from models import User, Topic, Message
from .base import bad_request, display_time, pass_time

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
            if 'tags' not in topic:
                topic['tags'] = ''

            try:
                user = CACHE_USER[t.owner_id]
            except KeyError:
                user = User.get_by_id(t.owner_id)
                CACHE_USER[t.owner_id] = user
            topic['owner_name'] = user.username
            topic['created_time'] = display_time(topic['created_time'])

            message = Message.get_latest_by_topic(str(t.id))
            message_count = Message.topic_count(str(t.id))
            if message:
                # 最新回复
                try:
                    user = CACHE_USER[message.user_id]
                except KeyError:
                    user = User.get_by_id(message.user_id)
                    CACHE_USER[message.user_id] = user
                message.user_name = user.username
                message.created_time = pass_time(message.created_time)
            topic['new_comment'] = message
            topic['message_count'] = message_count
            result.append(topic)
        return json.dumps(result)

    def POST(self):
        if not session.user or session.user.id is None:
            return bad_request('请先登录！')

        data = web.data()
        data = json.loads(data)

        tags = [tag for tag in data.get('tags', '').split(' ') if tag]
        topic_data = {
            "title": data.get('title'),
            "tags": tags,
            "owner_id": session.user.id,
            "created_time": datetime.now(),
        }

        try:
            topic_id = Topic.create(**topic_data)
        except sqlite3.IntegrityError:
            return bad_request('你已创建过该名称!')

        topic_data.update({
            "id": topic_id,
            "owner_name": session.user.username,
            "created_time": display_time(topic_data.get('created_time')),
        })
        return json.dumps(topic_data)

    def PUT(self, obj_id=None):
        data = web.data()
        print data

    def DELETE(self, obj_id=None):
        pass
