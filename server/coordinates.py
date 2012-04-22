# -*- coding:utf-8 -*-
'''
version : __version__
date    : __date__

Created on 2012/4/14

Coordinatesクラス

@author: shinyorke
'''
import json
from dto import MongoDbDto

class Coordinates(MongoDbDto):
    '''
    KMLファイルより、緯度経度および高さを引っこ抜いたcollection
    '''
    
    # コレクション名
    _col_name = 'coordinates'
    
    # 地理空間情報用カラム
    _col_gis = 'location'

    def __init__(self,params):
        '''
        コンストラクタ
        input : {'db':databace object}
        output: none
        raise : none
        '''
        self._col = params['db'][self._col_name]

    def set_list_to_data(self,params):
        '''
        行データ格納
        配列リストからinsert/save/
        input : params(text)
        output: none
        raise : none
        '''
        # JSONデータを読み込む
        row = json.loads(params)
        self.data = {
                     'name':row["name"],
                     'location':self.get_location_dict(row["latitude"], row["longitude"]),
                     'elevation':row["elevation"]
                   }
