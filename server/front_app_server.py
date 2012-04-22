#-*- coding:utf-8 -*-
'''
version : __version__
date    : __date__

Created on 2012/4/20

API振り分け処理

@author: shinyorke
'''

from wsgi_controller import Controller

class BeforeAppProc(Controller):
    '''
    振り分け前処理
    今のところは何も無いので空実装
    '''
    
    def __init__(self, application):
        '''
        コンストラクタ
        input : none
        output: none
        raise : none
        '''
        self.application = application


    def __call__(self, environ, start_response):
        ''' WSGI アプリケーション '''
        return self.application(environ, start_response)

class FrontApp(Controller):
    '''
    振り分け処理
    定義したパスに従い、振り分け処理を行う
    '''

    def __init__(self, table):
        '''
        コンストラクタ
        input : none
        output: none
        raise : none
        '''
        # パスは長い順にマッチさせたいので、あらかじめソートしておく
        tmp = sorted(table, key=lambda x:len(x), reverse=True)

        # 扱いやすいように、タプルのリストにしておく
        table = [(x, table[x]) for x in tmp]

        self.table = table


    def __call__(self, environ, start_response):
        ''' リクエストのパスを見て振り分ける '''

        scriptname = self.get_scriptname(environ)
        pathinfo = self.get_pathinfo(environ)

        for p, app in self.table:

            if p == '' or p == '/' and pathinfo.startswith(p):
                return app(environ, start_response)

            # 同じパスならそのまま
            # 同じパスで始まっていて、その後にスラッシュがある
            if pathinfo == p or pathinfo.startswith(p) and \
                    pathinfo[len(p)] == '/':

                scriptname = scriptname + p
                pathinfo = pathinfo[len(p):]

                # リクエスト情報を書き換える
                self.set_scriptname(environ, scriptname)
                self.set_pathinfo(environ, pathinfo)

                return app(environ, start_response)

        return self.return_http_request_404(environ, start_response)



from wsgiref import simple_server
from coordinates_find_controller import CoordinatesFind
from flicker_photos_controller import FlickerPhotosController
from venue_controller import VenueController

# サブドメインとURLをここで決める
    
# サブドメイン
sub_domain = "/jiryokusen"

application = FrontApp({
                        sub_domain+'/geo':CoordinatesFind(),
                        sub_domain+'/photos':FlickerPhotosController(),
                        sub_domain+'/venues':VenueController(),
                        })

# 事前処理を噛ませる（なにもしないけど）
application = BeforeAppProc(application)

if __name__ == '__main__':

    srv = simple_server.make_server('', 8080, application)
    srv.serve_forever()
