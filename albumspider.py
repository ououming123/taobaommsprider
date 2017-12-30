from constant import *


def getalbumlist1(userId, album_ids, currPage, error=False):
    album_re = re.compile(
        r'<a href="//mm.taobao.com/self/album_photo.htm\?user_id=%d&album_id=(?P<album_id>.+)&album_flag=0" target="_blank">' % userId)
    url = albumlisturl % (mmids[i], currPage)
    data = send(url, None, headers=headers)
    sdata = album_re.findall(data)
    if (sdata is None or len(sdata) == 0):
        if (error):
            print("连续报错出错.  换代理吧.")
            return None
        else:
            changeProxy()
            return getalbumlist1(userId, album_ids, currPage, error=True)

    album_ids.extend(sdata)
    allPage = int(ablum_page_re.findall(data)[0])
    print("userId=%d, allPage=%d, currPage=%d, album_id in this page =%s" % (userId, allPage, currPage, str(sdata)))
    if currPage < allPage:
        time.sleep((random.random() + 0.5) * 2)  # 休眠1-3秒
        currPage += 1
        getalbumlist1(userId, album_ids, currPage)

    return album_ids


if __name__ == '__main__':
    mmids = list(set(readListFromDB(mmiddbfile)))#获取取到的MMID数据并去重
    albumdb = open(albumdbfile, "ab")
    changeProxy()  # 设定初始代理
    user_album = {}
    for i in range(0, len(mmids)):
        userId = mmids[i]
        currPage = 1
        time.sleep((random.random() + 0.5) * 2)  # 休眠1-3秒
        album_ids = []
        getalbumlist1(userId, album_ids, currPage, False)
        user_album[userId] = album_ids
        if(len(user_album) % 10 == 0):
            pickle.dump(user_album, albumdb)
            user_album = {}
            print('dump data....')







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