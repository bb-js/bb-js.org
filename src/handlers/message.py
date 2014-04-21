#coding:utf-8
import json
from datetime import datetime

import web

from models import Message, User
from .base import bad_request

session = web.config._session

CACHE_USER = {}


class MessageHandler:
    def GET(self):
        topic_id = web.input().get('topic_id')
        if topic_id:
            messages = Message.get_by_topic(topic_id) or []
        else:
            messages = Message.get_all()

        result = []
        current_user_id = session.user.id
        for m in messages:
            try:
                user = CACHE_USER[m.get('user_id')]
            except KeyError:
                user = User.get_by_id(m.get('user_id'))
                CACHE_USER[m.get('user_id')] = user
            message = dict(m)
            message['created_time'] = str(message['created_time'])
            message['user_name'] = user.username
            message['is_mine'] = (current_user_id == user.id)
            result.append(message)
        return json.dumps(result)

    def POST(self):
        data = web.data()
        data = json.loads(data)
        if not (session.user and session.user.id):
            return bad_request("请先登录！")

        message_data = {
            "content": data.get("content"),
            "topic_id": data.get("topic_id"),
            "user_id": session.user.id,
            "created_time": datetime.now(),
        }
        m_id = Message.create(**message_data)
        result = {
            "id": m_id,
            "content": message_data.get("content"),
            "topic_id": message_data.get("topic_id"),
            "user_id": session.user.id,
            "user_name": session.user.username,
            "created_time": str(message_data.get("created_time")),
            "is_mine": True,
        }
        return json.dumps(result)
