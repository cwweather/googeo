# -*- coding:utf-8 -*-
import urllib2
from maps_util import get_html, geocode
from dianping import h2d_dianping, h2d_main
from pymongo import MongoClient, GEOSPHERE, ASCENDING

key_words = [
    #"望京",
    "三元桥"
]



db = MongoClient("172.100.102.163", 27019)
db_shop = db.honey.test_shop
db_shop.create_index([("storeid", ASCENDING), ("mallid", ASCENDING)], unique=True, background=True)
db_shop.create_index([("loc", GEOSPHERE)], background=True)

if __name__== '__main__':
    search_url = "http://www.dianping.com/search/keyword/2/1_{key_word}/p{page}"
    main_url =   "http://www.dianping.com/search/keyword/2/0_%E6%9C%9B%E4%BA%ACsoho/r1471p{page}"
    result = []
    count = 0
    count_exi = 0
    for kw in key_words:
        print kw
        for i in range(1, 2):
            print_url = search_url.format(key_word=kw, page=i)
            open_url = search_url.format(key_word=urllib2.quote(kw), page=i)
            print "search: {}".format(print_url)
            #url = main_url.format(page=i)
            html = get_html(open_url)
            if not html:
                continue
            page_site = h2d_main(html=html).h2d()
            shop_urls = page_site["url"]
            for url in shop_urls:
                url_open = "http://www.dianping.com" + url
                if db_shop.find_one({"mallid": 2001, "storeid": filter(str.isdigit, str(url))}):
                    print "p{}-exist: {}".format(i, url_open)
                    count_exi = count_exi + 1
                    continue
                print "p{}: {}".format(i, url_open)
                html = get_html(url_open)
                shop_info = h2d_dianping(html=html, storeid=url).h2d()
                print shop_info
                if shop_info["addr"]:
                    # 获取地理坐标 maximum retry = 3
                    for i in range(0, 3):
                        loc_coordinates = []
                        try:
                            loc_coordinates = geocode(shop_info["addr"].encode("utf-8"))
                        except Exception, e:
                            print e
                        if loc_coordinates:
                            loc = []
                            loc.append(loc_coordinates[0][0]["lng"])
                            loc.append(loc_coordinates[0][0]["lat"])
                            shop_info["loc"] = {"type": "Point", "coordinates": loc}
                            print loc
                            break
                        print "geocode retry: " + str(i)
                db_shop.replace_one({"mallid": shop_info["mallid"],
                                                   "storeid": shop_info["storeid"]}, shop_info, upsert=True)
                count = count + 1
            if not page_site["next"]:
                break
    print "OK!!!!!"
    print "count!!!!!{}".format(count)
    print "exist!!!!!{}".format(count_exi)