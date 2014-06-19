#coding:utf-8
from datetime import datetime

import web


def bad_request(message):
    raise web.BadRequest(message=message)


def display_time(_datetime, format='%y-%m-%d %H:%M:%S'):
    return _datetime.strftime(format)


def pass_time(_datetime):
    duration = datetime.now() - _datetime
    if duration.days > 1:
        return "%s天前" % duration.days

    hours, minutes, seconds = convert_timedelta(duration)
    if hours > 0:
        return "%s小时前" % hours

    if minutes > 0:
        return "%s分钟前" % minutes

    if seconds > 0:
        return "%s秒前" % seconds


def convert_timedelta(duration):
    days, seconds = duration.days, duration.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 60)
    return hours, minutes, seconds
