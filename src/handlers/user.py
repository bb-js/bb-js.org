#coding:utf-8
import json
import hashlib
import sqlite3
from datetime import datetime

import web

from models import User
from .base import bad_request

session = web.config._session

CACHE_USER = {}


def sha1(data):
    return hashlib.sha1(data).hexdigest()


class UserHandler:
    def GET(self):
        # 获取当前登录的用户数据
        user = session.user
        return json.dumps(user)

    def POST(self):
        data = web.data()
        data = json.loads(data)
        username = data.get("username")
        password = data.get("password")
        password_repeat = data.get("password_repeat")

        if password != password_repeat:
            return bad_request('两次密码输入不一致')

        user_data = {
            "username": username,
            "password": sha1(password),
            "registed_time": datetime.now(),
        }

        try:
            user_id = User.create(**user_data)
        except sqlite3.IntegrityError:
            return bad_request('用户名已存在!')

        user = User.get_by_id(user_id)
        session.login = True
        user.pop('password')
        session.user = user

        result = {
            'id': user_id,
            'username': username,
        }
        return json.dumps(result)


class LoginHandler:
    def POST(self):
        data = web.data()
        data = json.loads(data)
        username = data.get("username")
        password = data.get("password")
        user = User.get_by_username_password(
            username=username,
            password=sha1(password)
        )
        if not user:
            return bad_request('用户名或密码错误！')

        session.login = True
        session.user = user
        result = {
            'id': user.get('id'),
            'username': user.get('username'),
        }
        return json.dumps(result)


class LogoutHandler:
    def GET(self):
        session.login = False
        session.user = None
        session.kill()
        return web.tempredirect('/#login')
