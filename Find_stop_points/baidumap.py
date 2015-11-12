# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 20:11:28 2015

@author: yangruosong
"""
import urllib2,urllib,httplib
import json


class xBaiduMap:
    def __init__(self,key='hoTI2K20zHsn6PvWvuG8IgXo'):
        self.host='http://api.map.baidu.com'
        self.path='/geocoder/v2/?'
        self.param={'address':None,'output':'json','ak':key,'location':None,'city':None}

    def getLocation(self,address,city=None):
        rlt=self.geocoding('address',address,city)
        if rlt!=None:
            l=rlt['result']
            if isinstance(l,list):
                return None
        return l['location']['lat'],l['location']['lng']

    def getAddress(self,lat,lng):
        rlt=self.geocoding('location',"{0},{1}".format(lat,lng))
        print rlt['status']
        if rlt!=None:
            l=rlt['result']
            return l['formatted_address']
 #Here you can get more details about the location with 'addressComponent' key
#ld=rlt['result']['addressComponent']
#print(ld['city']+';'+ld['street'])
#
    def geocoding(self,key,value,city=None):
        if key=='location':
            if 'city' in self.param:
                del self.param['city']
            if 'address' in self.param:
                del self.param['address']
        elif key=='address':
            if 'location' in self.param:
                del self.param['location']
            if city==None and 'city' in self.param:
                del self.param['city']
        else:
            self.param['city']=city
            self.param[key]=value
            r=urllib.urlopen(self.host+self.path+urllib.urlencode(self.param))
            rlt=json.loads(r.read())
            if rlt['status']=='OK':
                return rlt
            else:
                print"Decoding Failed"
                return None

def getAddress(lat,lng):
    url = 'http://api.map.baidu.com/geocoder/v2/?ak=hoTI2K20zHsn6PvWvuG8IgXo&callback=renderReverse&location='
    url += str(lat)
    url += ',' 
    url += str(lng)
    url += '&output=json&pois=1'
    response = urllib2.urlopen(url) 
    address = response.read()[29:-1]
    address = json.loads(address)
    if address !=None:
        l=address['result']
        return l['formatted_address']
