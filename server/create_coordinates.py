# -*- coding:utf-8 -*-
'''
Created on 2012/4/16
data作成用スクリプト

@author: shinyorke
'''
import sys
import time
import traceback
from coordinates import Coordinates
from databaceclient import MongoDbClient

if __name__ == '__main__':
    argvs = sys.argv
    host = '127.0.0.1'
    port = 27017
    mclient = MongoDbClient(host,port)
    str_line = None
    try:
        mclient.connection()
        db = mclient.get_db('snmfl')
        coordinates = Coordinates({'db':db})
        coordinates.drop()
        coordinates.create_index_geo2d('location')
        
        cnt = 0
        for line in open(argvs[1],'r'):
            '''
            if cnt == 0:
                cnt = cnt + 1
                continue
            '''
            #str_line = line.rstrip("\r\n").replace('"','')   # 改行コードと引用符を取っ払う
            str_line = line.rstrip("\r\n")
            coordinates.set_list_to_data(str_line)             # 配列からdict作成
            coordinates.insert(coordinates.data)              # INSERT
            print str_line
            if cnt % 1000 == 0:
                time.sleep(0.5)
            cnt = cnt + 1
        print "total: %d" % cnt
    except:
        print traceback.format_exc() + ":" + str(str_line)
    finally:
        mclient.disconnection()
