from constant import *
from sqldb.dao import *

def getalbumlist1(userId, album_ids, currPage, error=False):
    userId = int(userId)
    album_re = re.compile(
        r'<h4><a href="//mm.taobao.com/self/album_photo.htm\?user_id=%d&album_id=(?P<album_id>.+)&album_flag=0" target="_blank">' % userId)
    albumName_re = re.compile(r'(?P<albumName>.+)</a></h4>')
    url = albumlisturl % (userId, currPage)
    data = send(url, None, headers=headers)
    # print(data)
    iddata = album_re.findall(data)
    namedata = albumName_re.findall(data)
    sdata = dict(zip(iddata, namedata))
    if (sdata is None or len(sdata) == 0):
        if (error):
            print("连续报错出错.  换代理吧.")
            return None
        else:
            if(error):
                return None
            changeProxy()
            return getalbumlist1(userId, album_ids, currPage, error=True)

    album_ids.append(sdata)
    allPage = int(ablum_page_re.findall(data)[0])
    print("userId=%d, allPage=%d, currPage=%d, album_id in this page =%s" % (userId, allPage, currPage, str(sdata)))
    if currPage < allPage:
        time.sleep((random.random() + 0.5) * 2)  # 休眠1-3秒
        currPage += 1
        getalbumlist1(userId, album_ids, currPage, False)

    return album_ids


def trasToSQLData(data):
    print(data)
    values = []
    for k, v in data.items():
        for s in v:
            for sk, sv in s.items():
                value = (sk, k, sv.strip(), "https://mm.taobao.com/self/album_photo.htm?user_id=%s&album_id=%s"%(str(k), str(sk)))
                values.append(value)
    return values


if __name__ == '__main__':
    # mmids = list(set(readListFromDB(mmiddbfile)))#获取取到的MMID数据并去重
    # albumdb = open(albumdbfile, "ab")
    conn = getDB()
    cursor = conn.cursor()
    cursor.execute("select userId from taobaomm;")
    mmids = cursor.fetchall()
    cursor.close()
    conn.close()
    print(mmids)
    changeProxy('http://183.32.88.108:808')  # 设定初始代理
    user_album = {}
    for i in range(1446, len(mmids)):
        userId = mmids[i]['userId']
        currPage = 1
        time.sleep((random.random() + 0.3) * 2)  # 休眠0.6-2.6秒
        album_ids = []
        getalbumlist1(userId, album_ids, currPage, False)
        user_album[userId] = album_ids
        if(len(user_album) % 1 == 0):
            conn = getDB()
            cursor = conn.cursor()
            print("current index = %d"%i)
            cursor.executemany("insert into mmalbum values(%s,%s,%s,%s)",trasToSQLData(user_album))
            conn.commit()
            cursor.close()
            conn.close()
            user_album = {}
            # print('dump data....')










# def getalbumlist(userId):
#     album_ids = []
#     pages=1
#     url = albumlisturl%(userId, pages)
#
#     album_re = re.compile(r'<a href="//mm.taobao.com/self/album_photo.htm\?user_id=%d&album_id=(?P<album_id>.+)&album_flag=0" target="_blank">' % userId)
#     headers = {'User-Agent': random.choice(user_agent)}
#     requ = Request(url, headers=headers)
#     data = bytes.decode(chardet.detect(urllib.request.urlopen(Request(url, headers=headers)).read())['encoding'])
#     # print(data)
#     album_ids.append(album_re.findall(data))
#     # print(album_id)
#     page = ablum_page_re.findall(data)
#     if(page > 1):
#         for i in range(2, page+1):
#             url = albumlisturl%(userId, i)
#             data = bytes.decode(chardet.detect(urllib.request.urlopen(Request(url, headers=headers)).read())['encoding'])
#             album_ids.append(album_re.findall(data))
#     return album_ids, page