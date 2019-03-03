# -*- coding: utf-8 -*-
import re
import time
import socket
import requests
from random import randint
from requests.adapters import HTTPAdapter
from novel import SaveNovel

timeout = 20
socket.setdefaulttimeout(timeout)

save = SaveNovel()

pages_index_url = []

urls = "http://www.xbiquge.la/fenlei/10_1.html"

header = {

    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36",
}

s = requests.session()
s.mount('http://', HTTPAdapter(max_retries=3))


def avoid_10060(fun, text_url, lastrowid):
    error_time = 0
    while True:
        time.sleep(0.3)
        try:
            return fun(text_url, lastrowid)
        except requests.exceptions.ConnectionError:
            error_time += 1
            if error_time == 100:
                print('your network is little bad')
                time.sleep(60)
            if error_time == 101:
                print('your network is broken')
                break
            continue
        finally:
            return None
        break


def code(res):
    if res.status_code == 200:
        if res.encoding == 'ISO-8859-1':
            encodings = requests.utils.get_encodings_from_content(res.text)
            if encodings:
                res.encoding = encodings[0]
            else:
                res.encoding = res.apparent_encoding


def find_text(text_url, lastrowid):
    try:
        res = s.get(text_url, headers=header, timeout=(3, 7))
        code(res)
        res = res.text.encode("utf-8").decode("utf-8")
        pattern = re.compile('class="bookname">.*?<h1>(.*?)</h1>', re.S)
        title = re.findall(pattern, res)
        content = text_url
        s.close()
        save.addchaper(lastrowid, title[0], content)
        print(title[0])
        return None
    except requests.HTTPError as e:
        print(e)
        time.sleep(5)
        find_text(text_url, lastrowid)
        return None
    except requests.exceptions.ConnectionError as e:
        print(e)
        time.sleep(5)
        find_text(text_url, lastrowid)
        return None


def find_novel(pages_index_url):
    try:
        max_page_num = len(pages_index_url)
        for i in range(0, max_page_num + 1):
            url = pages_index_url[randint(0, max_page_num - 1)]
            res = s.get(url, headers=header, timeout=(3, 7))
            code(res)
            res = res.text.encode("utf-8").decode("utf-8")
            pattern1 = re.compile('<div id="maininfo">.*?<h1>(.*?)</h1>', re.S)
            pattern2 = re.compile('<div id="maininfo">.*?<h1>.*?<p>.*?者：(.*?)</p>', re.S)
            pattern3 = re.compile('<dd><a href=.(.*?). >.*?</a></dd>', re.S)
            novel_name = re.findall(pattern1, res)
            writer_name = re.findall(pattern2, res)
            chapter_urls = re.findall(pattern3, res)
            chapter_urls = ["http://www.xbiquge.la{}".format(url_id) for url_id in chapter_urls]
            con = save.findnovel(novel_name[0], len(chapter_urls))
            s.close()
            if isinstance(con, tuple):
                chapter_urls = chapter_urls[-con[0]:]
                for item in chapter_urls:
                    print(item)
                    avoid_10060(find_text, item, con[1])
                    time.sleep(0.5)
            elif con is -1:
                sort = save.findsort()
                lastrowid = save.addnovels(sort, novel_name[0], writer_name[0])
                for item in chapter_urls:
                    print(item)
                    avoid_10060(find_text, item, lastrowid)
                    time.sleep(0.5)
    except requests.HTTPError as e:
        print(e)
        return None
    except requests.exceptions.ConnectionError as e:
        print(e)
        return None


def get_url(main_url):
    try:
        res = s.get(main_url, headers=header, timeout=(3, 7))
        code(res)
        res = res.text.encode("utf-8").decode("utf-8")
        time.sleep(1)
        s.close()
        return res
    except requests.HTTPError as e:
        print(e)
        return None
    except requests.exceptions.ConnectionError as e:
        error_time = 0
        while True:
            time.sleep(0.3)
            try:
                get_url(main_url)
            except:
                error_time += 1
                if error_time == 100:
                    time.sleep(10)
                if error_time == 101:
                    print(e)
                    return None
                continue
            break


def get_pages(url):
    html = get_url(url)
    if html:
        pattern = re.compile('<body>.*?id="main".*?<div class="novellist">(.*?)class="dahengfu"', re.S)
        pattern1 = re.compile('<li><a href="(.*?)/">.*?</a></li>')
        p = re.findall(pattern, html)
        page_index = re.findall(pattern1, p[0])
        for item in page_index:
            pages_index_url.append(item)
        return 1
    else:
        print("获取页面出错")
        return None


if __name__ == '__main__':
    while True:
        error = get_pages(urls)
        if error is not None:
            find_novel(pages_index_url)
            pages_index_url.clear()
        else:
            continue
