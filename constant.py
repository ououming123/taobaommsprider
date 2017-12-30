import re
import random
import json
import urllib.request
from urllib.request import Request
import chardet
import time
import pickle
from utils import *


mmlisturl = 'https://mm.taobao.com/tstar/search/tstar_model.do?_input_charset=utf-8'
albumlisturl = "https://mm.taobao.com/self/album/open_album_list.htm?_charset=utf-8&user_id=%d&page=%d"
photolisturl = 'https://mm.taobao.com/album/json/get_album_photo_list.htm?user_id=%s&album_id=%s&page=%d'

user_agent = [
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
]

ablum_page_re = re.compile(r'<input name="totalPage" id="J_Totalpage" value="(?P<pager>.+)" type="hidden" />')
mmiddbfile = "./db/mmid.db"
albumdbfile = "./db/album.db"
headers = {'User-Agent': random.choice(user_agent)}