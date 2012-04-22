# -*- coding:utf-8 -*-
'''
version : __version__
date    : __date__

Created on 2012/4/19

Flickrクライアントのクラス

@author: shinyorke
'''

import flickrapi
import unittest
from unittest import TestCase

class Flickr(object):
    '''
    Flickrから写真を探す用のクラス
    '''
    api_key='cee4b06c5f3465282a78cfd9742a5e09'
    flickr = flickrapi.FlickrAPI(api_key)


    def __init__(self):
        '''
        コンストラクタ
        input : none
        output: none
        raise : none
        '''
        pass
    
    def photos_search(self,
                      lat=0.0,
                      lon=0.0,
                      text="",
                      extras="url_s,url_m,url_n,geo",
                      per_page=10,
                      page=1,
                      min_upload_date=0,
                      max_upload_date=0
                      ):
        '''
        写真一覧を検索
        input : lat,lon
        output: dict
        raise : none
        '''
        photos = self.flickr.photos_search(
                                           lat=lat, 
                                           lon=lon, 
                                           extras=extras, 
                                           per_page=per_page,
                                           page=page,
                                           min_upload_date=min_upload_date,
                                           max_upload_date=max_upload_date
                                           )
        return photos
        
    def url_list(self,photos):
        '''
        URLのリストを生成
        input : photos
        output: [{photo:{thumbnail:url,normal:url,large:url}},...],pages,total
        raise : none
        '''
        pages,total = photos.findall("photos")[0].attrib["pages"],photos.findall("photos")[0].attrib["total"]
        ret_list = []
        for row in photos.findall("photos"):
            for photo in row.findall("photo"):
                ret_list.append({"photo":
                                 {
                                  "thumbnail":photo.attrib["url_s"],
                                  "normal":photo.attrib["url_n"],
                                  "large":photo.attrib["url_m"],
                                  "location":{
                                              "lat":photo.attrib["latitude"],
                                              "lon":photo.attrib["longitude"],
                                              },
                                  }
                                 })
        return {
                "photos":ret_list,
                "pages":pages,
                "total":total
                }

class TestFlickr(TestCase):
    
    flickr = None
    #setUpは、テストメソッド実行毎に事前に実行される
    def setUp(self):
        print 'setUp'
        
    def tearDown(self):
        print 'tearDown'
    
    def test_photos_search(self):
        self.flickr = Flickr()
        photos = self.flickr.photos_search(
                                           lat=35.703189,
                                           lon=139.579926,
                                           text="",
                                           min_upload_date=1303440369,
                                           max_upload_date=1335062769
                                           )
        photo_list = self.flickr.url_list(photos)
        for row in photo_list["photos"]:
            print "thumbnail： %s normal： %s large： %s" % (str(row["photo"]["thumbnail"]), str(row["photo"]["normal"]), str(row["photo"]["large"]))
            print "latitude: %s longitude: %s" % (str(row["photo"]["location"]["lat"]),str(row["photo"]["location"]["lon"]))
        print "pages: %s, total: %s" % (photo_list["pages"],photo_list["total"])

if __name__ == '__main__':
    unittest.main()
    
        