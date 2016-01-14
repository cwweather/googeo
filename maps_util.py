# -*- coding: utf-8 -*-
import urllib2
import simplejson as json
import urllib
import requests


GEOCODE_BASE_URL1 = 'http://maps.google.com/maps/api/geocode/json'
GEOCODE_BASE_URL = 'https://maps.google.com/maps/api/geocode/json'


def geocode1(address):
    """
    Get Json From Google Api
    :param address:
    :return:
    """
    geo_args = {
        'address': address,
    }
    url = GEOCODE_BASE_URL + '?' + urllib.urlencode(geo_args)
    ret = requests.get(url, timeout=5)
    if ret.status_code != 200:
        return None
    response = json.loads(ret.text)
    if response['status'] != 'OK':
        return None
    results = response['results']
    rets = [(result['geometry']['location'], result['formatted_address']) for result in results]
    return rets

def geocode(address):
    """
    Get Json From Google Api
    :param address:
    :return:
    """
    geo_args = {
        'address': address,
        'key': 'AIzaSyAKTDQhIe3Q9tc-8aEg3aRUpXM1tCQ5qWo',
    }
    url = GEOCODE_BASE_URL + '?' + urllib.urlencode(geo_args)
    req = urllib.urlopen(url)
    if req.getcode() != 200:
        return None
    response = json.loads(req.read())
    # print response
    if response['status'] != 'OK':
        return None
    results = response['results']
    rets = [(result['geometry']['location'], result['formatted_address']) for result in results]
    return rets

def get_html(url):
    try:
        request = urllib2.Request(url)
        request.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2)')
        html = urllib2.urlopen(request).read()
    except Exception, e:
        print "damn"
        return
    return html

if __name__ == '__main__':
    address = '北京市朝阳区望京街阜安西路11号合生麒麟社2楼'
    rets = geocode(address)
    print rets
