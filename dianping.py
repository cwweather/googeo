# -*- coding:utf-8 -*-
import re
import datetime
import random
from h2d import H2Dict

class h2d_dianping(H2Dict):

    def set_props(self):
        self.props = {
            "mallid": 2001,
            "storeid": "",
            "title": "",
            "desc": "",
            "avg_p": 0,
            "shop_url": "",
            "city": "",
            "region": "",
            "addr": "",
            "tel": "",
            "himg": "",
            "imgs": [],
            "loc": {},
            "created": datetime.datetime.now(),
            "modified": datetime.datetime.now(),
        }
        self.require_props = ["storeid"]

    def grap1_title(self):
        text = self.soup.findAll(name="h1", attrs={"class": "shop-name"})[0].contents[0]
        return text

    def grap1_desc(self):
        return ""

    def grap1_avg_p(self):
        text = self.soup.findAll(name="div", attrs={"class": "brief-info"})[0].contents[7].string
        return filter(str.isdigit, str(text))

    def grap1_shop_url(self):
        text = self.soup.findAll(name="link", attrs={"rel": "canonical"})[0].attrs[1][1]
        return text

    def grap1_city(self):
        text = self.soup.findAll(name="a", attrs={"class": "city J-city"})[0].contents[0]
        return text

    def grap1_region(self):
        text = self.soup.findAll(name="span", attrs={"itemprop": "locality region"})[0].text
        return text

    def grap1_addr(self):
        text = self.soup.findAll(name="span", attrs={"itemprop": "street-address"})[0].attrs[2][1]
        return text

    def grap1_tel(self):
        text = self.soup.findAll(name="span", attrs={"itemprop": "tel"})[0].text
        return text

    def grap1_himg(self):
        text = self.soup.findAll(name="img", attrs={"itemprop": "photo"})[0].attrs[1][1]
        return text

    def grap1_imgs(self):
        text = self.soup.findAll(name="img", attrs={"itemprop": "photo"})[0].attrs[1][1]
        return [text]

    def grap1_storeid(self):
        return filter(str.isdigit, str(self.storeid))

    def grap1_loc(self):
        loc = [116.47754, 39.99369]
        ran = 0
        loc[0] = loc[0] + ran
        ran = 0
        loc[1] = loc[1] + ran
        #return {"type": "Point", "coordinates": loc}
        return {}


class h2d_main(H2Dict):
    def set_props(self):
        self.props = {
            "url": [],
            "next": ""
        }
    def grap1_url(self):
        urls = []
        for sp in self.soup.findAll(name="a", attrs={"data-hippo-type": "shop"}):
            try:
                url = sp.attrs[4][1]
                urls.append(url)
            except Exception, e:
                continue
        return urls

    def grap1_next(self):
        next = self.soup.findAll(name="a", attrs={"class": "next"})[0].text
        return next