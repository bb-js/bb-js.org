#coding:utf-8

import web


def bad_request(message):
    raise web.BadRequest(message=message)
