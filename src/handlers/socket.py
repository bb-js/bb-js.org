#coding:utf-8
import copy
from datetime import datetime

import web
from socketio import socketio_manage
from socketio.namespace import BaseNamespace
from socketio.mixins import RoomsMixin, BroadcastMixin
import markdown

from models import Message
from .base import display_time

session = web.config._session

CACHE_USER = {}


class ChatNamespace(BaseNamespace, RoomsMixin, BroadcastMixin):
    def on_go_out(self):
        room_num = self.socket.session.get('room')
        if room_num:
            print 'go_out', room_num
            self.leave(room_num)

    def on_topic(self, topic_id):
        """ 加入以某个主题id为房间

        客户端进入聊天室界面先发送此请求，确定房间号
        """
        room_num = 'room_%s' % topic_id
        self.socket.session['room'] = room_num
        print 'join', room_num
        self.join(room_num)

    def on_message(self, model):
        user = self.environ['user']
        if user is None:
            # 手动从store中取出user
            session_id = self.environ['session_id']
            _data = session.store[session_id]
            user = _data['user']
        model.update({
            "user_id": user.id,
            "created_time": datetime.now(),
        })
        m_id = Message.create(**model)
        raw_content = model.get('content')
        model.update({
            "content": markdown.markdown(raw_content),
            "raw_content": raw_content,
            "user_name": user.username,
            'id': m_id,
            'created_time': display_time(model['created_time']),
            'is_mine': True,
        })
        # 发送回客户端
        self.emit('message', model)

        # 发送给其他人
        model['is_mine'] = False
        self.emit_to_room(
            self.socket.session['room'],
            'message',
            model,
        )

    def recv_disconnect(self):
        print 'DISCONNECT!!!!!!!!!!!!!!!!!!!!!!!'
        self.disconnect(silent=True)


class SocketHandler:
    def GET(self):
        context = copy.copy(web.ctx.environ)
        context.update({
            "user": session.user,
            "session_id": session.session_id,
        })
        socketio_manage(context, {'': ChatNamespace})
        # 重新载入session数据，因为session在socket请求中改变了
        session._load()
