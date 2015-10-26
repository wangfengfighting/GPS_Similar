__author__ = 'Administrator'
#coding: utf-8
import numpy as np
import  math
a=[
    [(28.231311798095703, 112.9939193725586, 1443243136.0, 1.0),
    (28.231313705444336, 112.99392700195312, 1443243136.0, 2.0)]
    ,
    [(28.231311798095703, 112.9939193725586, 1443243136.0, 0.0),
    (28.231313705444336, 112.99392700195312, 1443243136.0, 0.0)]
 ]
b=np.array(a[0][0][1])
print  len(a[0])
def midpoint(x1, y1, x2, y2):
#Input values as degrees

#Convert to radians
    lat1 = math.radians(x1)
    lon1 = math.radians(x2)
    lat2 = math.radians(y1)
    lon2 = math.radians(y2)

    bx = math.cos(lat2) * math.cos(lon2 - lon1)
    by = math.cos(lat2) * math.sin(lon2 - lon1)
    lat3 = math.atan2(math.sin(lat1) + math.sin(lat2), \
           math.sqrt((math.cos(lat1) + bx) * (math.cos(lat1) \
           + bx) + by**2))
    lon3 = lon1 + math.atan2(by, math.cos(lat1) + Bx)

    return [round(math.degrees(lat3), 2), round(math.degrees(lon3), 2)]