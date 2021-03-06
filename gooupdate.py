# -*- coding:utf-8 -*-
import urllib2
import time
from maps_util import get_html
from dianping import h2d_dianping, h2d_main
from pymongo import MongoClient, GEOSPHERE, ASCENDING
from maps_util import geocode

key_words = [
    #"望京",
    "酒仙桥"
]

db = MongoClient("172.100.102.163", 27019)
db_shop = db.honey.shop
db_shop.create_index([("storeid", ASCENDING), ("mallid", ASCENDING)], unique=True, background=True)
db_shop.create_index([("loc", GEOSPHERE)], unique=True, background=True)

if __name__== '__main__':
    all = db_shop.find()
    print "all:{}".format(all.count())
    count = 0
    for shop in all:
        print "======{}=======".format(count)
        print shop
        shop_id = shop["_id"]
        address = shop["addr"]
        for i in range(0, 3):
            loc_coordinates = []
            try:
                #time.sleep(5)
                loc_coordinates = geocode(address.encode("utf-8"))
            except Exception, e:
                print e
            if loc_coordinates:
                break
            print "retry: " + str(i)
        if loc_coordinates:
            loc = []
            loc.append(loc_coordinates[0][0]["lng"])
            loc.append(loc_coordinates[0][0]["lat"])
            db_shop.update_one({"_id": shop_id}, {"$set":{"loc": {"type": "Point", "coordinates": loc}}})
            print loc
        print "================"
    print "OK!!!!!"
    print "count!!!!!{}".format(count)