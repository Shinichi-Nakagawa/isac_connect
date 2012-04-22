# -*- coding:utf-8 -*-
'''
version : __version__
date    : __date__

Created on 2011/12/14

WSGI Controllerクラス

@author: shinyorke
'''
import cgi
import json
from wsgiref import util

class Controller(object):
    '''
    WSGI用コントローラー・クラス
    WSGIで汎用的に使う実装は全部こっちに書く
    WSGI規約でAPIを作るときはこの人を継承しよう
    '''
    
    # HTTPステータスコード
    HTTP_STS_200 = '200 OK'
    HTTP_STS_501 = '501 Not Implemented'
    HTTP_STS_303 = '303 See Other'
    HTTP_STS_404 = '404 NotFound'
    
    # HTTPレスポンスヘッダー
    HTTP_RESPONSE_HEADER_TEXT = [('Content-type', 'text/plain'),('Access-Control-Allow-Origin','*')]
    HTTP_RESPONSE_HEADER_HTML = [('Content-type', 'text/html; charset=utf-8'),('Access-Control-Allow-Origin','*')]
    
    # environ用キー
    HTTP_ENVIRON_KEY_REQUEST_METHOD = 'REQUEST_METHOD'
    HTTP_ENVIRON_KEY_QUERY_STRING = 'QUERY_STRING'
    HTTP_ENVIRON_KEY_SCRIPT_NAME = 'SCRIPT_NAME'
    HTTP_ENVIRON_KEY_PATH_INFO = 'PATH_INFO'

    
    # 文字コード
    CHAR_TYPE = 'utf-8'

    def __init__(self):
        '''
        コンストラクタ
        input : none
        output: none
        raise : none
        '''
        pass

    def __call__(self, environ, start_response):
        ''' WSGI アプリケーション '''
        pass
    
    def get_method(self,environ):
        '''
        HTTP Method名取得
        input : environ
        output: メソッド名(str)
        raise : none
        '''
        return environ.get(self.HTTP_ENVIRON_KEY_REQUEST_METHOD)
    
    def get_parameter(self,environ):
        '''
        HTTP GET parameter取得
        input : environ
        output: Parameter辞書(dict)
        raise : none
        '''
        ret_dict = {}
        for row in cgi.parse_qsl(environ.get(self.HTTP_ENVIRON_KEY_QUERY_STRING)):
            ret_dict[str(row[0])] = str(row[1])
        return ret_dict
    
    def json_dumps_utf8(self,obj):
        '''
        オブジェクトをJSON形式にdumpする(UTF-8)
        input : オブジェクト
        output: JSONテキスト
        raise : none
        '''
        return str(json.dumps(obj,encoding=self.CHAR_TYPE,ensure_ascii=True))
    
    def get_scriptname(self,environ):
        '''
        HTTP スクリプト名取得
        input : environ
        output: スクリプト名(str)
        raise : none
        '''
        return environ.get(self.HTTP_ENVIRON_KEY_SCRIPT_NAME, '')
    
    def get_pathinfo(self,environ):
        '''
        HTTP パス名取得
        input : environ
        output: パス名(str)
        raise : none
        '''
        return environ.get(self.HTTP_ENVIRON_KEY_PATH_INFO, '')
    
    def set_scriptname(self,environ,scriptname):
        '''
        HTTP スクリプト名セット
        input : environ,スクリプト名
        output: none
        raise : none
        '''
        environ[self.HTTP_ENVIRON_KEY_SCRIPT_NAME] = scriptname
    
    def set_pathinfo(self,environ,pathinfo):
        '''
        HTTP パス名セット
        input : environ,パス名
        output: パス名(str)
        raise : none
        '''
        environ[self.HTTP_ENVIRON_KEY_PATH_INFO] = pathinfo

    def return_http_request_404(self,environ, start_response):
        '''
        404　Not Found用メソッド
        input : environ,start_response
        output: TEXT(404 Not Found)
        raise : none
        '''

        start_response(Controller.HTTP_STS_404, Controller.HTTP_RESPONSE_HEADER_TEXT)

        return '%s is not found' % util.request_uri(environ)
    
