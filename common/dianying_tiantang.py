from utils import base_headers
from concurrent.futures import ThreadPoolExecutor
import threading
import requests
from bs4 import BeautifulSoup
import json
import time

BASE_DOMAIN = 'http://www.dytt8.net{}'

base_url = 'http://www.dytt8.net/html/gndy/dyzz/list_23_{}.html'


class Spider:
    def __init__(self):
        self.lock = threading.Lock()
        self.results = []

    def scrawl(self, url):
        print('current url : {} '.format(url))
        res = requests.get(url, headers=base_headers, timeout=5)
        res.encoding = 'gbk'
        time.sleep(0.5)
        soup = BeautifulSoup(res.text, 'html.parser')
        movie_list = soup.select('table.tbspan')
        for movie in movie_list:
            a_link = movie.find('a', class_="ulink")
            if not a_link:
                continue
            name = a_link.text
            url = BASE_DOMAIN.format(a_link.get('href'))
            with self.lock:
                self.results.append({
                    'name': name,
                    'url': url
                })
                if len(self.results) % 10 == 0:
                    print('current count is {}'.format(len(self.results)))

    def run(self):
        start = time.time()
        urls = [base_url.format(i) for i in range(1, 2)]
        with ThreadPoolExecutor(64) as executor:
            executor.map(self.scrawl, urls)
        print('total {} with time used {}'.format(len(self.results), time.time() - start))


if __name__ == '__main__':
    spider = Spider()
    spider.run()
    with open('results.json', 'w') as f:
        json.dump(spider.results, f, ensure_ascii=False, indent=2)
