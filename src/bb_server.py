#!/usr/bin/env python
#coding:utf-8
from gevent import monkey
monkey.patch_all()

import web
from web.httpserver import StaticMiddleware
from socketio import server


urls = (
    '/', 'IndexHandler',  # 返回首页
    '/topic', 'TopicHandler',
    '/topic/(\d+)', 'TopicHandler',
    '/message', 'MessageHandler',
    '/user', 'UserHandler',
    '/user/(\d+)', 'UserHandler',
    '/login', 'LoginHandler',
    '/logout', 'LogoutHandler',
    '/socket.io/.*', 'SocketHandler',
)

app = web.application(urls, globals())
application = app.wsgifunc(StaticMiddleware)

if web.config.get('_session') is None:
    session = web.session.Session(
        app,
        web.session.DiskStore('sessions'),
        initializer={'login': False, 'user': None}
    )
    web.config._session = session

web.config.debug = False

from handlers.index import IndexHandler  # noqa
from handlers.user import UserHandler, LoginHandler, LogoutHandler  # noqa
from handlers.topic import TopicHandler  # noqa
from handlers.message import MessageHandler  # noqa
from handlers.socket import SocketHandler  # noqa


if __name__ == "__main__":
    import sys
    PORT = 8080
    if len(sys.argv) > 1:
        PORT = int(sys.argv[1])
    print 'http://localhost:%s' % PORT
    server.SocketIOServer(
        ('localhost', PORT),
        application,
        resource="socket.io",
        policy_server=True,
        policy_listener=('0.0.0.0', 10843),
    ).serve_forever()
