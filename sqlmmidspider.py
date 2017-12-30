
from constant import *
from sqldb.dao import *
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
    data = send(url=url, formdata=formdata, headers=headers)
    dataToDict = json.loads(data)
    if(isMmidDataOk(dataToDict)):
        if(not error):
            mmids = dataToDict['data']['searchDOList']
            mmids = addExtraData(mmids)
        else:
            print("连续报错出错.  换代理吧.")
            return None
    else:
        if error:
            return None
        return getMMData(url, currentPage, True)
    return mmids

# 获取ID
# def getMMID(data):
#     ID = []
#     for i in data:
#         ID.append(i['userId'])
#     return ID

def addExtraData(data):
    temp = []
    for i in data:
        i['mainPage'] = 'https://mm.taobao.com/self/aiShow.htm?userId=%d'%i['userId']
        i['albumPage'] = 'https://mm.taobao.com/self/model_album.htm?userId=%d'%i['userId']
        temp.append(i)
    return temp

def trasToSQLData(data):
    values = []
    for i in data:
        value = (i['userId'], i['realName'], i['mainPage'], i['albumPage'], i['city'], i['height'], i['weight'],
                 i['avatarUrl'], i['cardUrl'], i['identityUrl'], i['modelUrl'], str(i['totalFanNum']), str(i['totalFavorNum']))
        values.append(value)
    return values


# def getalbumphotolist(userId, albumId):
#     page=1
#     url = photolisturl%(userId, albumId, page)
#     headers = {'User-Agent': random.choice(user_agent)}
#     requ = Request(url, headers=headers)
#     data = urllib.request.urlopen(requ).read()

if __name__ == '__main__':
    ID = []

    changeProxy()# 设定初始代理
    mmidss = []


    for i in range(1, 1450+1):#...  骗人的.   显示总共1450页. 实际上167页开始就没了.
        time.sleep((random.random() + 0.5) * 2)  # 休眠1-3秒
        mmids = getMMData(mmlisturl,i)
        if(mmids is None):
            print('检测到连续出错. 退出...')
            exit()
        print("page=%d, mmids=%s"%(i, str(mmids)))
        conn = getDB()
        cursor = conn.cursor()
        cursor.executemany("insert into taobaomm values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",trasToSQLData(mmids))
        conn.commit()
        cursor.close()
        conn.close()







