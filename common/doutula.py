import requests
from bs4 import BeautifulSoup
import threading
from concurrent.futures import ThreadPoolExecutor
from urllib.request import urlretrieve
import os
from fake_useragent import UserAgent
from utils.mongodb import emoji_db

ua = UserAgent()

urlpattern = 'http://www.doutula.com/article/list/?page={}'

lock = threading.Lock()


class ImgItem(object):
    def __init__(self, name, url):
        self.name = name
        self.url = url
        # self.original_url = original_url


def judge_folder():
    path = os.path.join(os.path.abspath('.'), 'doutula')
    if not os.path.exists(path):
        os.mkdir(path)
    else:
        pass


def download_img(img):
    url_split = os.path.splitext(img.get('original_url'))
    img_ext = url_split[1]
    img_name = img.get('name') + img_ext
    urlretrieve(img.get('original_url'), './doutula/{}'.format(img_name))


class Doutula:
    result = []

    def __init__(self, page=2):
        self.urls = [urlpattern.format(i) for i in range(1, page + 1)]

    def run(self, url):
        res = requests.get(url, headers={
            'User-Agent':ua.random,
            'Referer':'http://www.doutula.com/article/list/?page=631',
            'Host':'www.doutula.com'
        })
        res.encoding = 'utf-8'
        sew = BeautifulSoup(res.text, 'html.parser')
        random_list = sew.select('a.random_list')
        for item in random_list:
            img_list = item.select('img.lazy')
            for img in img_list:
                name = img.get('alt')
                url = img.get('data-original')
                img_item = ImgItem(name, url)

                with lock:
                    length = len(self.result)
                    if length and length % 20 == 0:
                        print('current count is {}'.format(len(self.result)))
                    self.result.append(vars(img_item))

    def crawl(self):
        with ThreadPoolExecutor(64) as executor:
            executor.map(self.run, self.urls)


if __name__ == '__main__':
    doutula = Doutula(page=1)
    doutula.crawl()
    emoji_db.delete_many({})
    emoji_db.insert_many(doutula.result)
