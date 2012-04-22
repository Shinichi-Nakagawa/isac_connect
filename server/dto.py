# -*- coding:utf-8 -*-
'''
version : __version__
date    : __date__

Created on 2011/12/07
Change  on 2012/4/16

DataTransferObjectクラス

@author: shinyorke
'''

import re
import json
import unittest
from unittest import TestCase
from pymongo.objectid import ObjectId
from pymongo import Connection, GEO2D

class MongoDbDto(object):
    '''
    mongoDB用DataTransferObjectクラス
    コレクション操作用methodを提供する。
    基本的にはpymongoライブラリのRapper
    '''
    
    # エンコード文字列
    char_type ='utf-8'

    # データObject
    # data = {'key':'hoge','value':'hoge'}
    data = {}
    
    # コレクションのオブジェクト
    _col = None
    
    # Object ID
    _col_obj_id = '_id'
    
    # オプション文字列
    str_limit = 'limit'
    str_skip = 'skip'

    def __init__(self,params):
        '''
        コンストラクタ
        input : params(dict)
        output: none
        raise : none
        '''
        self._col = params['db'][params['col']]

    def set_list_to_data(self,params):
        '''
        行データ格納
        配列リストからinsert/save/
        input : params(dict)
        output: none
        raise : none
        '''
        # TODO 全体でやりそうな処理があったら書く（なさそうだけど）
        '''
        self.data = {
                   'hoge':'hoge_value',
                   'foo' :'foo_value',
                   # TODO 追加するときはここに書く
                   }
        '''
    
    def save(self,data):
        '''
        saveメソッド
        input : data(dict)
        output: none
        raise : none
        '''
        self._is_col()
        self._col.save(data)
    
    def insert(self,data):
        '''
        insertメソッド
        input : data(dict)
        output: none
        raise : none
        '''
        self._is_col()
        self._col.insert(data)
            
    def find(self,query,options):
        '''
        findメソッド
        完全一致or部分一致検索
        input(query) : dict{'key':value} valueはstrまたはre(正規表現使う場合） 
                       Noneオブジェクトの場合は全件検索
        input(options) : dict{'key':value} limit,skip等の検索オプション
        output: dict
        raise : Collection Not Found!
        '''
        self._is_col()
        # オプション内容チェック
        is_skip,is_limit = self._is_options_skip_limit(options)
        if is_skip and is_limit:
            # skip,limit両方
            return self._col.find(query).skip(int(options[self.str_skip])).limit(int(options[self.str_limit]))
        elif is_limit:
            # limitのみ
            return self._col.find(query).limit(int(options[self.str_limit]))
        elif is_skip:
            # skipのみ
            return self._col.find(query).skip(int(options[self.str_skip]))
        else:
            # オプション無し
            return self._col.find(query)
            
    def find_sort(self,query,sort_clms,options):
        '''
        findメソッド(ソート付き)
        完全一致or部分一致検索
        input(query) : dict{'key':value} valueはstrまたはre(正規表現使う場合） 
                       Noneオブジェクトの場合は全件検索
        input(sort_clms) : ソート対象カラム
        input(options) : dict{'key':value} limit,skip等の検索オプション
        output: dict
        raise : Collection Not Found!
        '''
        self._is_col()
        # オプション内容チェック
        is_skip,is_limit = self._is_options_skip_limit(options)
        if is_skip and is_limit:
            # skip,limit両方
            return self._col.find(query).sort(sort_clms).skip(int(options[self.str_skip])).limit(int(options[self.str_limit]))
        elif is_limit:
            # limitのみ
            return self._col.find(query).sort(sort_clms).limit(int(options[self.str_limit]))
        elif is_skip:
            # skipのみ
            return self._col.find(query).sort(sort_clms).skip(int(options[self.str_skip]))
        else:
            # オプション無し
            return self._col.find(query).sort(sort_clms)
            
    def find_near(self,query,sort_clms,options):
        '''
        findメソッド(ソート付き)
        完全一致or部分一致検索
        input(query) : dict{'key':value} valueはstrまたはre(正規表現使う場合） 
                       Noneオブジェクトの場合は全件検索
        input(sort_clms) : ソート対象カラム
        input(options) : dict{'key':value} limit,skip等の検索オプション
        output: dict
        raise : Collection Not Found!
        '''
        self._is_col()
        # オプション内容チェック
        is_skip,is_limit = self._is_options_skip_limit(options)
        if is_skip and is_limit:
            # skip,limit両方
            return self._col.find(query).sort(sort_clms).skip(int(options[self.str_skip])).limit(int(options[self.str_limit]))
        elif is_limit:
            # limitのみ
            return self._col.find(query).sort(sort_clms).limit(int(options[self.str_limit]))
        elif is_skip:
            # skipのみ
            return self._col.find(query).sort(sort_clms).skip(int(options[self.str_skip]))
        else:
            # オプション無し
            return self._col.find(query).sort(sort_clms)
    
    def find_one(self,obj):
        '''
        findOneメソッド
        完全一致or部分一致検索
        input : オブジェクトID(pymongo.objectid)またはクエリー(dic)
        output: dict
        raise : Collection Not Found!
        '''
        self._is_col()
        return self._col.find_one(obj)
    
    def remove(self,query):
        '''
        removeメソッド
        input : dict{'key':value} valueはstrまたはre(正規表現使う場合） 
        output: none
        raise : none
        '''
        self._is_col()
        self._col.remove(query)
        
    def drop(self):
        '''
        コレクションをDropする
        全データが飛ぶので使用注意
        input : none
        output: none
        raise : none
        '''
        self._col.drop()
        
    def get_cursor_to_list(self,cursor):
        '''
        Object IDを含むcursorを配列に変換
        input : cursor(findした後のObject,listでも化)
        output: str(json)
        raise : none
        '''
        ret_list = []
        for row in cursor:
            ret_list.append(self.get_dict_objectid_to_str(row))
        return ret_list
    
    def get_dict_objectid_to_str(self,row_dict):
        '''
        Object IDを含む辞書を文字列に変換
        input : dict
        output: str(json)
        raise : none
        '''
        if row_dict.has_key(self._col_obj_id):
            row_dict[self._col_obj_id] = self.get_objectid_to_str(row_dict[self._col_obj_id])
        return row_dict
    
    def get_objectid_to_str(self,objectid):
        '''
        Object IDを文字列に変換
        input : objectid
        output: str
        raise : None
        '''
        return str(objectid)
    
    def get_str_to_objectid(self,objectid):
        '''
        文字列からObject IDを導出
        input : str
        output: objectid
        raise : None
        '''
        return ObjectId(str(objectid))

    def create_index_geo2d(self,column):
        '''
        地理情報空間INDEX作成
        input : 対象カラム(str)
        output: None
        raise : None
        '''
        self._is_col()
        self._col.create_index([(column, GEO2D)])
        
    def get_find_query_geo2d_near(self,column,params):
        '''
        検索条件作成（地理情報空間検索用）
        [format]
        {"column": {"$near": params}}
        input : column 対象カラム(str)
        input : params 検索キー(dict)
        output: dict
        raise : None
        '''
        return {column:{"$near":params}}
    
    def get_location_dict(self,lat,lon):
        '''
        ロケーション辞書を返す
        [format]
        {"lat": float(lat),"lon":float(lon)}
        input : lat 緯度
        input : lon 軽度
        output: dict
        raise : None
        '''
        
        # Noneかどうか
        if lat is None or lon is None:
            return {}
        
        # 小数点+数値チェック
        # 厳密な値チェックはしてない
        for row in [lat,lon]:
            if len(str(row).split(".")) > 2:
                return {}
            for row2 in str(row).split("."):
                if str(row2).isdigit() == False:
                    return {}
                
        return {"lat":float(lat),"lon":float(lon)}
    
    def _is_col(self):
        '''
        コレクションのNoneチェック
        input : none
        output: True
        raise : None
        '''
        if self._col is not None:
            return True
        else:
            raise 'Collection Not Found!'
    
    def _is_options_skip_limit(self,options):
        '''
        オプションの中にskip,limitが入ってるか確かめる
        一個目の戻り値がskip有無、二個目がlimitのBoolean値を返す
        input : none
        output 1(skip):  True or False
        output 2(limit): or False
        raise : Collection Not Found!
        '''
        is_skip,is_limit = False,False
        # 引数が空ならチェックしない
        if options is None:
            return False,False
        # skip有無
        if options.has_key(self.str_skip):
            is_skip = True
        # limit有無
        if options.has_key(self.str_limit):
            is_limit = True
        return is_skip,is_limit
        
        
class TestMongoDbDto(TestCase):
    # テスト対象クラスのオブジェクト
    dto = None
    # コネクション
    con = None
    # データベース
    db = None
    db_name = 'test_db'
    
    # テスト用コレクション
    col_key = 'col'
    col_val = 'test_col'
    col_gis = 'location'
    col_dic = {col_key:col_val}
    # テストデータを突っ込む
    test_data = [
            {'title':'検索one','value':'find One確認','category':'findone'},
            {'title':'検索1','value':'findのテスト1','category':'find'},
            {'title':'検索2','value':'findのテスト2','category':'find'},
            {'title':'検索3','value':'findのてすと3','category':'find'},
            {'title':'検索4','value':'findのTEST4','category':'find'},
            {'title':'dummy1','value':'hogeのテスト','category':'dummy'},
            {'title':'dummy2','value':'foo','category':'dummy'},
            ]
    
    #setUpは、テストメソッド実行毎に事前に実行される
    def setUp(self):
        print 'setUp'
        #コネクション作成
        self.con = Connection('127.0.0.1', 27017)
        print 'DB connect() done.'
        self.db = self.con[self.db_name]
        print 'DB set done.'
        self.col_dic['db'] = self.db
        self.mdd = MongoDbDto(self.col_dic)
        print 'mongoDB DTO Object create done.'
        
        # テストデータを突っ込む
        for row in self.test_data:
            self.db[self.col_val].insert(row)
        
    def tearDown(self):
        print 'tearDown'
        if self.db is not None:
            self.db[self.col_val].drop()
            print 'Collections drop() done.'
            
        if self.con is not None:
            self.con.disconnect()
            print 'DB disconnect() done.'
    
    def test_is_col(self):
        print 'test_is_col'
        assert self.mdd._is_col()
        self.mdd.col = None

        try:
            self.mdd._is_col()
            assert False
        except:
            assert True
            print 'test_is_col Done.'
    
    def test_is_options_skip_limit(self):
        print 'test_is_options_skip_limit'
        ret1,ret2 = self.mdd._is_options_skip_limit(None)
        assert ret1 == False and ret2 == False
        ret3,ret4 = self.mdd._is_options_skip_limit({"hoge":"hoge","foo":"foo"})
        assert ret3 == False and ret4 == False
        ret5,ret6 = self.mdd._is_options_skip_limit({"skip":1,"limit":2})
        assert ret5 == True and ret6 == True
        ret7,ret8 = self.mdd._is_options_skip_limit({"limit":2})
        assert ret7 == False and ret8 == True
        ret9,ret10 = self.mdd._is_options_skip_limit({"skip":2})
        assert ret9 == True and ret10 == False
            
    def test_find_all(self):
        print 'test_find_all'
        # 全件検索のテスト
        find_list = self.mdd.find(None,None)
        print "count:"+ str(find_list.count())
        assert find_list.count() == 7
        for row in find_list:
            print row.items()

        # 全件検索のテスト(limit付き)
        find_list = self.mdd.find(None,{"limit":3})
        print "count:"+ str(find_list.count(with_limit_and_skip=True))
        assert find_list.count(with_limit_and_skip=True) == 3
        for row in find_list:
            print row.items()
        # 全件検索のテスト(limit付き)
        find_list = self.mdd.find(None,{"limit":"5"})
        print "count:"+ str(find_list.count(with_limit_and_skip=True))
        assert find_list.count(with_limit_and_skip=True) == 5
        for row in find_list:
            print row.items()
        # 全件検索のテスト(skip付き)
        find_list = self.mdd.find(None,{"skip":2})
        print "count:"+ str(find_list.count(with_limit_and_skip=True))
        assert find_list.count(with_limit_and_skip=True) == 5
        for row in find_list:
            print row.items()
        # 全件検索のテスト(skip,limit付き)
        find_list = self.mdd.find(None,{"skip":"3","limit":"2"})
        print "count:"+ str(find_list.count(with_limit_and_skip=True))
        assert find_list.count(with_limit_and_skip=True) == 2
        for row in find_list:
            print row.items()
            
    def test_find(self):
        print 'test_find'
        # 条件指定検索のテスト
        # 完全一致
        find_list = self.mdd.find({'category':'find'},{})
        print "count:"+ str(find_list.count())
        assert find_list.count() == 4
        for row in find_list:
            print str(row['category'])

        # 部分一致
        obj = re.compile("のテスト")
        find_list = self.mdd.find({'value':obj},None)
        print "count:"+ str(find_list.count())
        assert find_list.count() == 3
        for row in find_list:
            print str(row['value'])
            
    def test_find_sort(self):
        print 'test_find_sort'
        # ソート機能テスト
        # 全件
        find_list = self.mdd.find_sort(None,'category',None)
        print 'category昇順'
        for row in find_list:
            print str(row['category'])
        # 先頭4件だけ
        find_list = self.mdd.find_sort(None,'category',{'limit':4})
        print 'category昇順先頭4件'
        assert find_list.count(with_limit_and_skip=True) == 4
        for row in find_list:
            print str(row['category'])

        # skip 最初の4レコードをスキップ
        find_list = self.mdd.find_sort(None,'category',{'skip':4})
        print 'category昇順4件スキップ、5件目以降'
        assert find_list.count(with_limit_and_skip=True) == 3
        for row in find_list:
            print str(row['category'])

        # skipとlimit同時並行
        find_list = self.mdd.find_sort(None,'category',{'skip':2,'limit':4})
        print 'category昇順3件目から4レコード'
        assert find_list.count(with_limit_and_skip=True) == 4
        for row in find_list:
            print str(row['category'])
            assert row['category'] == 'find'

    
    def test_findone(self):
        print 'test_findone'
        # まず、オブジェクトIDを引っこ抜く
        find_list = self.mdd.find({'title':'検索one'},None)
        key = ''
        for row in find_list:
            key = row['_id']
            break
        obj = self.mdd.find_one(key)
        assert str(obj['category']) == 'findone'
        assert str(obj['title']) == '検索one'
        print str(obj['value'])
    
    def test_set_list_to_data(self):
        print 'test_set_list_to_data'
        # 空実装、テストなし
        pass
    
    def test_insert(self):
        print 'test_insert'
        ins_dict = {'hoge':'insert test','foo':'これはインサートのテストです','category':'insert'}
        self.mdd.insert(ins_dict)
        find_list = self.mdd.find({'hoge':'insert test'},None)
        for row in find_list:
            assert str(row['foo']) == 'これはインサートのテストです'
            assert str(row['category']) == 'insert'
            print row.items()
    
    def test_save(self):
        print 'test_save'
        # まずdata作る
        ins_dict = {'hoge':'insert test','foo':'これはインサートのテストです','category':'insert'}
        self.mdd.insert(ins_dict)
        # 作ったdataをfindoneしてsave
        save_data = self.mdd.find_one({'hoge':'insert test'})
        save_data['hoge'] = 'save test'
        save_data['foo'] = 'これはせーぶのてすとです'
        save_data['category'] = 'save'
        save_data['bar'] = 'カラムを足してみる'
        self.mdd.save(save_data)
        
        # もう一度検索（更新前のキーで）
        # NoneだったらOK
        ret_chk1 = self.mdd.find_one({'hoge':'insert test'})
        assert ret_chk1 is None
        
        # 今度は更新後のキーで
        # 何かしらのオブジェクトが拾える
        ret_chk2 = self.mdd.find_one({'hoge':'save test'})
        assert ret_chk2 is not None
        # オブジェクトの中身チェック
        assert ret_chk2['hoge'] == 'save test'
        assert ret_chk2['foo'] == 'これはせーぶのてすとです'
        assert ret_chk2['category'] == 'save'
        assert ret_chk2['bar'] == 'カラムを足してみる'
        
    def test_remove(self):
        print 'test_remove'
        # まずdata作る
        remove_dict = {'hoge':'remove test','foo':'これは削除のテストです','category':'remove'}
        self.mdd.insert(remove_dict)
        
        # 削除前チェック
        before_chk = self.mdd.find_one({'hoge':'remove test'})
        assert before_chk is not None
        bcnt = self.mdd.find(None,None)
        assert bcnt.count() == 8
        
        # 削除してみる
        self.mdd.remove({'hoge':'remove test'})
        after_chk = self.mdd.find_one({'hoge':'remove test'})
        assert after_chk is None
        acnt = self.mdd.find(None,None)
        assert acnt.count() == 7
    
    def test_drop(self):
        print 'test_drop'
        self.mdd.drop()
        acnt = self.mdd.find(None,None)
        assert acnt.count() == 0
    
    def test_get_cursor_to_list(self):
        print 'test_get_cursor_to_list'
        ret = self.mdd.find(None,None)
        ret_list = self.mdd.get_cursor_to_list(ret)
        print json.dumps(ret_list,encoding='utf-8',ensure_ascii=False)
        
    def test_get_dict_objectid_to_str(self):
        print 'test_get_dict_objectid_to_str'
        objid = ObjectId(str('4b3f270c114f5cca93dc6a89'))
        in_dict = {self.mdd._col_obj_id:objid,'hoge':'hogehoge','foo':'foo'}
        ret = self.mdd.get_dict_objectid_to_str(in_dict)
        assert ret[self.mdd._col_obj_id] == '4b3f270c114f5cca93dc6a89'
        assert ret['hoge'] == 'hogehoge'
        assert ret['foo'] == 'foo'
        
    def test_get_str_to_objectid(self):
        print 'test_objectid_to_str'
        objid = ObjectId(str('4b3f270c114f5cca93dc6a89'))
        str_objid = self.mdd.get_objectid_to_str(objid)
        assert str_objid == '4b3f270c114f5cca93dc6a89'
        
    def test_get_objectid_to_str(self):
        print 'test_str_to_objectid'
        objid = self.mdd.get_str_to_objectid('4b3f270c114f5cca93dc6a89')
        assert isinstance(objid,ObjectId)
        assert str(objid) == '4b3f270c114f5cca93dc6a89'
        
    def test_create_index_geo2d(self):
        print 'test_create_index_geo2d'
        # まずdata作る
        geo_dict = {
                    'hoge':'geo test','foo':'これはgeocodeのテストです','category':'geocode',
                    'location':{
                                'lat':float(35.703868),
                                'lon':float(139.580011)
                                }
        }
        self.mdd.create_index_geo2d(self.col_gis)
        self.mdd.insert(geo_dict)
        # GIS座標で完全一致検索
        # 35.703868,139.580011
        ret_list = self.mdd._col.find({"location": {"$near": [35.703868, 139.580011]}})
        assert ret_list.count() == 1
        for row in ret_list:
            assert row['hoge'] == 'geo test'
            assert row['foo'] == 'これはgeocodeのテストです'
            assert row['category'] == 'geocode'
            assert row['location'].has_key('lat')
            assert float(row['location']['lat']) == 35.703868
            assert row['location'].has_key('lon')
            assert float(row['location']['lon']) == 139.580011
    
    def test_get_find_query_geo2d_near(self):
        print 'test_get_find_query_geo2d_near'
        obj = self.mdd.get_find_query_geo2d_near('loc', {'lat':3.01,'lon':50.22})
        assert obj is not None
        assert obj.has_key('loc')
        assert obj['loc'].has_key('$near')
        assert obj['loc']['$near'].has_key('lat')
        assert obj['loc']['$near'].has_key('lon')
        assert obj['loc']['$near']['lat'] == 3.01
        assert obj['loc']['$near']['lon'] == 50.22
        
    def test_get_location_dict(self):
        print 'test_get_location_dict'
        # 両方共整数
        test_dic1 = self.mdd.get_location_dict(1, 2)
        assert test_dic1['lat'] == 1
        assert test_dic1['lon'] == 2

        # 両方共それっぽい緯度経度
        test_dic2 = self.mdd.get_location_dict("35.703254","139.579837")
        assert test_dic2['lat'] == 35.703254
        assert test_dic2['lon'] == 139.579837

        # 値が片方欠損
        test_dic3 = self.mdd.get_location_dict("35.703254",None)
        assert len(test_dic3) == 0
        test_dic4 = self.mdd.get_location_dict(None,"139.579837")
        assert len(test_dic4) == 0
        # 小数点が無駄に多い
        test_dic5 = self.mdd.get_location_dict("35.703.254",None)
        assert len(test_dic5) == 0
        test_dic6 = self.mdd.get_location_dict(None,"139.57.98.37")
        assert len(test_dic6) == 0
        # 数値以外
        test_dic7 = self.mdd.get_location_dict("hoge",None)
        assert len(test_dic7) == 0
        test_dic8 = self.mdd.get_location_dict(None,"ほげ")
        assert len(test_dic8) == 0

if __name__ == '__main__':
    unittest.main()

        
        