import json
import random
import urllib.request
from urllib.request import Request
import chardet
import re
import time
import pickle

import urllib.parse

proxylist = ['http://183.32.88.108:808', 'http://183.32.88.135:808',
             'http://183.32.88.105:808',  'http://113.67.165.99:8118','http://183.32.88.115:808']
#被屏蔽IPhttps://183.32.89.73:6666,'https://183.32.89.73:6666',https://183.48.33.24:8118
def send(url, formdata, headers, charset='utf-8'):
    if formdata is not None:
        formdata = urllib.parse.urlencode(formdata)
        requ = Request(url, data=bytes(formdata, charset), headers=headers)
    else:
        requ = Request(url, headers=headers)
    data = urllib.request.urlopen(requ).read()
    data = data.decode(chardet.detect(data)['encoding'], 'ignore')
    # dataToDict = json.loads(data)
    return data

def changeProxy(proxyurl = None):
    if(proxyurl is not None):
        proxy = proxyurl
    else:
        proxy = proxylist[random.randint(0, len(proxylist)-1)]
    print('useing proxy = %s'%(proxy))
    proxy_handler = urllib.request.ProxyHandler({proxy.split('://')[0]: proxy.split('://')[1]})
    opener = urllib.request.build_opener(proxy_handler)
    urllib.request.install_opener(opener)


#判断这个接口是否已经被封.
def isMmidDataOk(data):
    try:
        data['data']['searchDOList'][0]['userId']
    except:
        return 0
    return 1

# def isAlbumDataOk(data):
#     try:



def readListFromDB(dbfile):
    f = open(dbfile, 'rb')
    objs = []
    while 1:
        try:
            objs.extend(pickle.load(f))
        except EOFError:
            break
    return objs