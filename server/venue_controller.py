# -*- coding:utf-8 -*-
'''
version : __version__
date    : __date__

Created on 2012/4/19

Venue Controllerクラス

@author: shinyorke
'''
from sabani_controller import SabaniController
from venue_gateway import Venue

class VenueController(SabaniController):
    '''
    Venueコントローラー・クラス
    場所検索はこのクラスを使う。基本的にはfour square前提
    [GET 引数]
    # TODO 暫定です、変わる可能性アリ
    lat      : 緯度
    lon      : 経度
    '''

    def __init__(self):
        '''
        コンストラクタ
        input : none
        output: none
        raise : none
        '''
        SabaniController.__init__(self)
        self.venue = Venue()

    def __call__(self, environ, start_response):
        ''' WSGI アプリケーション '''
        SabaniController.__call__(self, environ, start_response)
        # リクエストメソッドを取得
        method = self.get_method(environ)

        if method == 'GET':
            # GET の場合
            # パラメーター取得
            params = self.get_parameter(environ)
            # パラメーターの必須チェック
            chk_dict = self.chk_param(params)
            # 何かしらのパラメーターエラーがあった場合
            if chk_dict.has_key(self.API_MSG_KEY):
                start_response(self.HTTP_STS_200, self.HTTP_RESPONSE_HEADER_TEXT)
                self.create_http_responce_dict(
                                               self.API_STS_NG_PARAM,
                                               chk_dict[self.API_MSG_KEY],
                                               params,
                                               None,
                                               )
                return self.json_dumps_utf8(self.ret_dict)
            # コンテンツを検索
            ret_list,count = self.venue.venue_search({},
                                                     ll=(params[self.HTTP_REQUEST_GET_LAT],
                                                         params[self.HTTP_REQUEST_GET_LON]))
            if count == 0:
                ret_list,count = self.venue.venue_search({},
                                                         ll=(params[self.HTTP_REQUEST_GET_LAT],
                                                             params[self.HTTP_REQUEST_GET_LON]),
                                                         radius=100000)
            start_response(self.HTTP_STS_200, self.HTTP_RESPONSE_HEADER_TEXT)
            self.create_http_responce_dict(
                                            self.API_STS_OK,
                                            None,
                                            ret_list,
                                            count,
                                            )
            return self.json_dumps_utf8(self.ret_dict)
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
    
    def chk_param(self,params):
        '''
        GET パラメータのチェックを行う
        input : GETパラメータ(dict)
        output: dict(エラー無しは空)
        raise : none
        '''
        # チェック戻り値
        chk_dict = {}
        # GETパラメーター存在チェック
        chk_dict.update(self.chk_is_params(params,
                                           [
                                            # TODO
                                            self.HTTP_REQUEST_GET_LAT,
                                            self.HTTP_REQUEST_GET_LON,
                                            ]))
        
        return chk_dict

from wsgiref import simple_server

application = VenueController()

if __name__ == '__main__':

    srv = simple_server.make_server('', 8080, application)

    srv.serve_forever()

    
