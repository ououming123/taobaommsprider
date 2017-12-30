#和sqlphotospider代码逻辑完全一样.  只是为了简单并发.
from constant import *
from sqldb.dao import *


def getPhotoData(userId, albumId, photo_ids, currPage, error=False):
    url = photolisturl%(userId, albumId, currPage)
    data = send(url=url, formdata=None, headers=headers)
    data = json.loads(data)
    totalPage = int(data['totalPage'])
    photo_ids.extend(data['picList'])
    print("userId=%d, albumId=%d, allPage=%d, currPage=%d, album_id in this page =%s" % (int(userId), int(albumId), totalPage, currPage, str(data['picList'])))
    if currPage < totalPage:
        time.sleep((random.random() + 0.5) * 2)  # 休眠1-3秒
        currPage += 1
        getPhotoData(userId, albumId, photo_ids, currPage, False)

    return photo_ids


def trasToSQLData(data):
    values = []
    for pic in data:
        value = (pic['picId'], pic['userId'], pic['albumId'], pic['picUrl'], pic['des'])
        values.append(value)
    return values




if __name__ == '__main__':
    conn = getDB()
    cursor = conn.cursor()
    cursor.execute("select albumId, userId from mmalbum;")
    useralbums = cursor.fetchall()
    cursor.close()
    conn.close()
    print(useralbums)
    user_ablum_photo = {}
    changeProxy(proxyurl='http://183.32.88.115:808')  # 设定初始代理
    for i in range(6000, 7000):
        userId = useralbums[i]['userId']
        albumId = useralbums[i]['albumId']
        currPage = 1
        photo_ids = []
        time.sleep((random.random() + 0.3) * 2)  # 休眠0.6-2.6秒
        getPhotoData(userId, albumId, photo_ids, currPage, False)
        conn = getDB()
        cursor = conn.cursor()
        print("current index = %d" % i)
        cursor.executemany("insert into mmphoto values(%s,%s,%s,%s,%s)", trasToSQLData(photo_ids))
        conn.commit()
        cursor.close()
        conn.close()
        photo_ids = []







