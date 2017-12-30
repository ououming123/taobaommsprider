
from constant import *

import urllib.parse



def getMMData(url,currentPage=0, error=False):
    ID = []
    formdata = {
        'q':'',
        'viewFlag':'A',
        'sortType':'default',
        'searchStyle':'',
        'searchRegion':'city:',
        'searchFansNum':'',
        'currentPage': currentPage,
        'pageSize': '100'
    }
    data = send(url = url, formdata=formdata, headers = headers)
    dataToDict = json.loads(data)
    if(isMmidDataOk(dataToDict)):
        if(not error):
            mmids = getMMID(dataToDict['data']['searchDOList'])
        else:
            print("连续报错出错.  换代理吧.")
            return None
    else:
        getMMData(url, currentPage, True)
    return mmids

# 获取ID
def getMMID(data):
    ID = []
    for i in data:
        ID.append(i['userId'])
    return ID



# def getalbumphotolist(userId, albumId):
#     page=1
#     url = photolisturl%(userId, albumId, page)
#     headers = {'User-Agent': random.choice(user_agent)}
#     requ = Request(url, headers=headers)
#     data = urllib.request.urlopen(requ).read()

if __name__ == '__main__':
    ID = []
    mmiddb = open(mmiddbfile, "ab")
    changeProxy()# 设定初始代理
    for i in range(1, 1450+1):#...  骗人的.   显示总共1450页. 实际上167页开始就没了.
        time.sleep((random.random() + 0.5) * 2)  # 休眠1-3秒
        mmids = getMMData(mmlisturl,i)
        if(mmids is None):
            pickle.dump(ID, mmiddb)
            print('检测到连续出错. 退出...')
            exit()
        print("page=%d, mmids=%s"%(i, str(mmids)))
        ID.extend(mmids)
        if(i % 10 == 0):
            pickle.dump(ID, mmiddb)
            ID = []
            print('dump data....')
    mmiddb.close()






