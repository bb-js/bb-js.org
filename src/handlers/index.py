#coding:utf-8

import web

session = web.config._session


# 首页
class IndexHandler:
    def GET(self):
        render = web.template.render('templates/')
        return render.index()
