# -*- coding:utf-8 -*-
'''
version : __version__
date    : __date__

Created on 2011/12/10

DataBaseClientクラス

@author: shinyorke
'''
import unittest
from unittest import TestCase
from pymongo import Connection

class MongoDbClient(object):
    '''
    mongoDB用DatabaceClientクラス
    接続・DB設定・接続解除はすべてここでやる。
    基本的にはpymongoライブラリのRapper
    '''
    # Host
    host = None
    # Port
    port = None
    # コネクション
    con = None

    def __init__(self,host,port):
        '''
        コンストラクタ
        hostとportを指定（値がなければデフォルト値採用）
        input : host(デフォルトはlocalhost),port(デフォルトは27017)
        output: none
        raise : none
        '''
        if host is not None:
            self.host = host
        else:
            raise 'Has Not Host.'
            
        if port is not None:
            self.port = port
        else:
            raise 'Has Not Port.'
        
    def connection(self):
        '''
        コネクト
        input : none
        output: none
        raise : none
        '''
        self.con = Connection(self.host,self.port)
        
    def disconnection(self):
        '''
        ディスコネクト
        disconnection命令後、コネクションプールをNone埋め
        input : none
        output: none
        raise : none
        '''
        if self.con is not None:
            self.con.disconnect()
            self.con = None
    
    def get_db(self,name):
        '''
        DBを取得
        input : データベース名（文字列）
        output: DataBace Object
        raise : none
        '''
        self.db = self.con[name]
        return self.db

class TestMongoDbClient(TestCase):
    # クライアント
    db_client = None
    # host
    host ='127.0.0.1'
    # port
    port = 27017
    
    #setUpは、テストメソッド実行毎に事前に実行される
    def setUp(self):
        print 'setUp'
        self.db_client = MongoDbClient(self.host,self.port)
        
    def test_connection(self):
        print 'test_connection'
        self.db_client.connection()
        assert self.db_client.con is not None

    def test_disconnection(self):
        print 'test_disconnection'
        self.db_client.disconnection()
        assert self.db_client.con is None
        
    def test_get_db(self):
        print 'test_get_db'
        self.db_client.connection()
        assert self.db_client.con is not None
        
    def tearDown(self):
        print 'tearDown'
        pass

if __name__ == '__main__':
    unittest.main()
        