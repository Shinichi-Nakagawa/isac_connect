# -*- coding:utf-8 -*-
'''
version : __version__
date    : __date__

Created on 2011/12/14

SABANI API Controllerクラス

@author: shinyorke
'''
from wsgi_controller import Controller
from databaceclient import MongoDbClient

class SabaniController(Controller):
    '''
    SABANI API用コントローラー・クラス
    mongoDB系の実装はこっちに書く
    SABANI APIはすべてこのクラスを継承する
    '''
    
    # GETパラメーターのキー
    HTTP_REQUEST_GET_KEY_OBJECT_ID = '_id'
    HTTP_REQUEST_GET_LAT = 'lat'
    HTTP_REQUEST_GET_LON = 'lon'
    HTTP_REQUEST_GET_PAGE = 'page'
    HTTP_REQUEST_GET_PER_PAGE = 'per_page'
    HTTP_REQUEST_GET_NE_LAT = 'nelat'
    HTTP_REQUEST_GET_NE_LON = 'nelon'
    HTTP_REQUEST_GET_SW_LAT = 'swlat'
    HTTP_REQUEST_GET_SW_LON = 'swlon'
    HTTP_REQUEST_GET_ZOOM = 'zoom'
    HTTP_REQUEST_GET_SKIP = 'skip'
    HTTP_REQUEST_GET_LIMIT = 'limit'
    
    # DBホスト設定
    # 環境によって変えてください
    SERVER_HOST = '127.0.0.1'
    SERVER_PORT = 27017
    
    # DB名
    DB_KEY = 'db'
    DB_NAME = 'snmfl'
    
    # ハッシュのキー
    # APIステータス
    API_STS_KEY = 'status'
    # API メッセージ（主にエラー用）
    API_MSG_KEY = 'msg'
    # 戻り値
    API_BODY_KEY = 'body'
    # 戻り値の行数
    API_COUNT_KEY = 'count'
    
    # APIのステータス（独自設定）
    API_STS_OK = 0              # OK(0件返し含む）
    API_STS_NG_PARAM = -1       # 引数不正
    API_STS_NG_OTHER = -1000    # その他
    
    # API メッセージBody
    API_MSG_BODY_NOT_IMPLEMENTED = 'Not mplemented'
    API_MSG_BODY_PARAMETER_NOT_EXIST_ERROR = 'Parameter not exist Error'
    API_MSG_BODY_OBJECT_ID_ERROR = 'Object Id Error'
    API_MSG_BODY_IS_DIGIT_ERROR = 'isdigit Error'
    API_MSG_BODY_MONGODB_ERROR = 'mongoDB Exception'
    
    # 戻り値
    # 必ずコイツを使うこと、初期値は正常(API_STS_OK)
    ret_dict = {}
    
    # mongoDBクライアント
    mclient = None
    # mongoDB DBObject
    mdb = None

    # コレクション
    col = None
    # コレクションのクラス
    col_class = None

    def __init__(self):
        '''
        コンストラクタ
        input : none
        output: none
        raise : none
        '''
        Controller.__init__(self)
        # mongoDBクライアントのオブジェクトを作る
        self.mclient = MongoDbClient(self.SERVER_HOST,self.SERVER_PORT)

    def __call__(self, environ, start_response):
        ''' WSGI アプリケーション '''
        # 戻り値を初期化
        Controller.__call__(self, environ, start_response)
        self.ret_dict = {self.API_STS_KEY:self.API_STS_OK}
    
    def get_mdb(self):
        '''
        mongoDB DBを取得
        input : none
        output: DB Object
        raise : none
        '''
        return self.mclient.get_db(self.DB_NAME)
        
    def connection(self):
        '''
        コネクト
        input : none
        output: none
        raise : none
        '''
        self.mclient.connection()
        
    def disconnection(self):
        '''
        ディスコネクト
        input : none
        output: none
        raise : none
        '''
        self.mclient.disconnection()
    
    def chk_objectid(self,params):
        '''
        Object Idのチェックを行う
        input : GETパラメータ(dict)
        output: dict(エラー無しは空)
        raise : none
        '''
        # キー値チェック
        if params.has_key(self.HTTP_REQUEST_GET_KEY_OBJECT_ID) == False:
            msg = ": Object Id not has key."
            return {self.API_MSG_KEY:self.API_MSG_BODY_OBJECT_ID_ERROR+msg}
        else:
            return {}
    
    def chk_is_params(self,params,keys):
        '''
        GETパラメーターの有無チェック
        空(None)又は長さゼロだったらNG
        input(params) : GETパラメータ(dict)
        input(keys)   : GETパラメーターkey項目リスト
        output: dict(エラー無しは空)
        raise : none
        '''
        if params is not None and len(params) > 0:
            return self.chk_params_is_keys(params, keys)
        else:
            return {self.API_MSG_KEY:self.API_MSG_BODY_PARAMETER_NOT_EXIST_ERROR}
    
    def chk_params_is_keys(self,params,keys):
        '''
        GETパラメーターの有無チェック
        指定したキーが全部あればTrue、無ければFalse
        input(params) : GETパラメータ(dict)
        input(keys)   : GETパラメーターkey項目リスト
        output: dict(エラー無しは空)
        raise : none
        '''
        for key in keys:
            if params.has_key(key):
                continue
            else:
                return {self.API_MSG_KEY:self.API_MSG_BODY_PARAMETER_NOT_EXIST_ERROR}
        return {}
    
    def chk_isdigit(self,params,key):
        '''
        Int型のチェックを行う
        input(params) : GETパラメータ(dict)
        input(key) : チェック対象項目のkey値(メッセージにも使う)
        output: dict(エラー無しは空)
        raise : none
        '''
        # キー値チェック
        # 必須チェックはしないので無かったら空で返す
        if params.has_key(key) == False:
            return {}
        
        # 数値チェック
        value = str(params[key])
        if value.isdigit():
            return {}
        else:
            msg = ": "+str(key)+" not has Integer."
            return {self.API_MSG_KEY:self.API_MSG_BODY_IS_DIGIT_ERROR+msg}
    
    def create_http_responce_dict(self,api_sts,api_msg,api_body,count):
        '''
        HTTP RESPONSE用のDictを生成
        ret_dictに直接書きこむ
        input(api_sts)  : HTTPステータス
        input(api_msg)  : メッセージ（エラー時等、使いたいときに指定）
        input(api_body) : HTTP RESPONCEボディー
        input(count)    : ボディーの行数(検索結果件数)
        output: dict(エラー無しは空)
        raise : none
        '''
        if api_sts is not None:
            self.ret_dict[self.API_STS_KEY] = api_sts
        if api_msg is not None:
            self.ret_dict[self.API_MSG_KEY] = api_msg
        if api_body is not None:
            self.ret_dict[self.API_BODY_KEY]= api_body
        if count is not None:
            self.ret_dict[self.API_COUNT_KEY] = count
            
    def get_find_options(self,params):
        '''
        GETパラメーターからFind用オプションを作り込む
        input : GETパラメータ(dict)
        output: dict(該当オプション無かったら空dictで返す)
        raise : none
        '''
        # TODO 作る
        options = {}
        # skip
        if params.has_key(self.HTTP_REQUEST_GET_SKIP):
            options[self.HTTP_REQUEST_GET_SKIP] = int(params[self.HTTP_REQUEST_GET_SKIP])
        # limit
        if params.has_key(self.HTTP_REQUEST_GET_LIMIT):
            options[self.HTTP_REQUEST_GET_LIMIT] = int(params[self.HTTP_REQUEST_GET_LIMIT])
            
        return options
                    
                    
