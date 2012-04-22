# -*- coding:utf-8 -*-
'''
version : __version__
date    : __date__

Created on 2012/4/16

Find Controllerクラス

@author: shinyorke
'''
import traceback
from sabani_controller import SabaniController

class FindController(SabaniController):
    '''
    Find用検索コントローラー・クラス
    リスト検索はこのクラスを使う
    [GET 引数]
    nelat(必須)
    nelon(必須)
    swlat(必須)
    swlon(必須)
    zoom(必須)
    skip(任意)
    limit(任意)
    [戻り値]
    [OK]
    {
    "status": 0, 
    "body": {
                photos:{
                # TODO ここに写真APIの検索結果が並ぶ
                },
                poi:{
                # TODO ここにコンテンツAPIの検索結果が並ぶ
                },
            }
    "count": bodyの行数
    }
    [NG]
    {
    "status": -1(引数エラー),-1000(Internal Server Error), 
    "msg"   :エラーメッセージ
    "body": {
            # ここにidとか並ぶ
            }
    }
    '''

    def __init__(self):
        '''
        コンストラクタ
        input : none
        output: none
        raise : none
        '''
        SabaniController.__init__(self)

    def __call__(self, environ, start_response):
        ''' WSGI アプリケーション '''
        SabaniController.__call__(self, environ, start_response)

    def find(self, environ, start_response):
        '''
        カテゴリーをキーに、検索を行う
        input : environ,start_response
        output: JSON TEXT
        raise : none
        '''
        # パラメータ取得
        params = self.get_parameter(environ)
        
        # パラメータチェック
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
        
        # オプション取得
        query = self.get_find_query(params)
        options = self.get_find_options(params)
        try:
            self.connection()
            self.col = self.col_class({self.DB_KEY:self.get_mdb()})
            # ソートなし
            rows = self.col.find(query,options)
            start_response(self.HTTP_STS_200, self.HTTP_RESPONSE_HEADER_TEXT)
            if rows is not None and rows.count(with_limit_and_skip=True) > 0:
                ret_list = self.col.get_cursor_to_list(rows)
                self.create_http_responce_dict(
                                               self.API_STS_OK,
                                               None,
                                               ret_list,
                                               rows.count(with_limit_and_skip=True),
                                               )
            else:
                self.create_http_responce_dict(
                                               self.API_STS_OK,
                                               None,
                                               {},
                                               0,
                                               )
                
        except:
            # 何かしらの例外が発生した場合は501エラー
            print traceback.format_exc()
            start_response(self.HTTP_STS_501, self.HTTP_RESPONSE_HEADER_TEXT)
            self.create_http_responce_dict(
                                           self.API_STS_NG_OTHER,
                                           self.API_MSG_BODY_MONGODB_ERROR,
                                           params,
                                           None,
                                           )
        finally:
            self.disconnection()

        return self.json_dumps_utf8(self.ret_dict)
    
    def get_nelatlon_swlatlon(self,params):
        ne_latlon = [
                     float(params[self.HTTP_REQUEST_GET_NE_LAT]),
                     float(params[self.HTTP_REQUEST_GET_NE_LON]),
                     ]
        sw_latlon = [
                     float(params[self.HTTP_REQUEST_GET_SW_LAT]),
                     float(params[self.HTTP_REQUEST_GET_SW_LON]),
                     ]
        return [ne_latlon,sw_latlon]
    
    def get_find_query(self,params):
        '''
        クエリーを作る
        input : GETパラメータ(dict)
        output: dict(クエリー無しは空)
        raise : none
        '''
        return {"location": {"$within": {"$box": self.get_nelatlon_swlatlon(params)}}}
    
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
                                           [self.HTTP_REQUEST_GET_NE_LAT,
                                            self.HTTP_REQUEST_GET_NE_LON,
                                            self.HTTP_REQUEST_GET_SW_LAT,
                                            self.HTTP_REQUEST_GET_SW_LON,
                                            self.HTTP_REQUEST_GET_ZOOM,
                                            #self.HTTP_REQUEST_GET_LIMIT # チェックしない
                                            ]))
        # skip
        chk_dict.update(self.chk_isdigit(params, self.HTTP_REQUEST_GET_SKIP))
        # limit
        chk_dict.update(self.chk_isdigit(params, self.HTTP_REQUEST_GET_LIMIT))
        
        return chk_dict

    
