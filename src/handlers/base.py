#coding:utf-8

import web


def bad_request(message):
    raise web.BadRequest(message=message)


def display_time(_datetime, format='%y-%m-%d %H:%M:%S'):
    return _datetime.strftime(format)
