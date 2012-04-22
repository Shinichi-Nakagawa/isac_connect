# -*- coding:utf-8 -*-
'''
version : __version__
date    : __date__

Created on 2012/4/16

CoordinatesFind Controllerクラス

@author: shinyorke
'''
from find_controller import FindController
from coordinates import Coordinates

class CoordinatesFind(FindController):
    '''
    磁力線位置情報検索コントローラー・クラス
    リスト検索はこのクラスを使う
    [GET 引数]
    nelat      : 緯度（北東）
    nelon      : 経度（北東）
    swlat      : 緯度（南西）
    swlon      : 経度（南西）
    zoom     : zoom level
    skip     : 検索開始位置(クライアントで算出)
    limit    : 取得件数
    '''

    def __init__(self):
        '''
        コンストラクタ
        input : none
        output: none
        raise : none
        '''
        FindController.__init__(self)
        self.col_class = Coordinates

    def __call__(self, environ, start_response):
        ''' WSGI アプリケーション '''
        FindController.__call__(self, environ, start_response)
        # リクエストメソッドを取得
        method = self.get_method(environ)

        if method == 'GET':
            # GET の場合
            return self.find(environ, start_response)
        else:
            # GET以外は501エラー扱い
            start_response(self.HTTP_STS_501, self.HTTP_RESPONSE_HEADER_TEXT)
            self.create_http_responce_dict(
                                           self.API_STS_NG_OTHER,
                                           self.API_MSG_BODY_NOT_IMPLEMENTED,
                                           {'method':method},
                                           None,
                                           )
            return self.json_dumps_utf8(self.ret_dict)

from wsgiref import simple_server

application = CoordinatesFind()

if __name__ == '__main__':

    srv = simple_server.make_server('', 8080, application)

    srv.serve_forever()

    
