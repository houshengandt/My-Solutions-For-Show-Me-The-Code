import urllib.request
from urllib.error import HTTPError, URLError
import sys
# import time
import urllib
from bs4 import BeautifulSoup


def get_html(url):
    html = urllib.request.urlopen(url).read()
    bs = BeautifulSoup(html, 'html.parser')
    return bs


def get_pic(bs):
    pics0 = bs.select('.photolst')
    pics = pics0[0].find_all('img')
    for pic in pics:
        link = pic.get('src')
        filename = link[-15:]
        large_link = link.replace("thumb", "large")
        try:
            urllib.request.urlretrieve(large_link, '%s' % filename)
        except HTTPError or URLError:
            continue


def find_next_page(bs):
    next = bs.select('#content > div.grid-16-8.clearfix > div.article > div.paginator > span.next > a')
    if len(next) > 0:
        next_url = next[0].get('href')
        return next_url


def main(a, count):
    get_pic(a)
    print('第%d页完成\n' % count)
    count += 1
    next_url = find_next_page(a)
    if next_url is None:
        sys.exit()
    a = get_html(next_url)
    main(a, count)


a = get_html('https://www.douban.com/photos/album/65866661/')   # 地址为想要爬取的相册第一页地址
main(a, 1)


