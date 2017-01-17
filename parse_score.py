#!/usr/bin/env python3
# -*- coding: utf-8 -*- 
import urllib
from urllib import request
from bs4 import BeautifulSoup
import http.cookiejar
import re
import time
import random

def make_cookie(name, value):
    return http.cookiejar.Cookie(
        version=0,
        name=name,
        value=value,
        port=None,
        port_specified=False,
        domain="programming.grids.cn",
        domain_specified=True,
        domain_initial_dot=False,
        path="/",
        path_specified=True,
        secure=False,
        expires=None,
        discard=False,
        comment=None,
        comment_url=None,
        rest=None
    )

user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36"
head = {'User-Agent': user_agent, 'Accept-Encoding':'gzip, deflate, sdch', 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}

#修改以下三行
mycookie = "34276ba71a3ca93846af35a650413de049d481ef80d381ed17e98e8114a2938bb355040f00c56f703ca30fe623d774da8caf1da95eda6dfec32512ad59c73960"
myurl = "http://programming.grids.cn/programming/admin/course/82cb41a9976b474d8bd773bcf0ea770b/showProblemList.do?problemsId=2943fa72326a416f8003ada10040d85e"
file_name = "6.txt"#写入的文件名

cookie = http.cookiejar.CookieJar()
#change this when needed
cookie.set_cookie(make_cookie("passport", mycookie))

domain = "http://programming.grids.cn"

def open_html(url):
    time.sleep(random.uniform(0, 1)) #延迟0-1秒
    request = urllib.request.Request(url, headers=head)
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie))  
    response = opener.open(request)
    # response = urllib.request.urlopen(request)
    html = response.read().decode("gb2312")
    return html

#寻找第一次accepted的时间
def parse_score_html(url):
    html = open_html(url)
    soup = BeautifulSoup(html, "lxml")
    ans_list = soup.find_all("tr", attrs={"class":re.compile(r'evenrow|oddrow')})
    # ans_list = ans_list.reverse()
    first_time = 'not_found'
    l = len(ans_list)
    for i in range(l):
        ans = ans_list[l - i - 1]
        tmp_list = ans.find_all("td")
        tid = tmp_list[0].get_text().strip()
        status = tmp_list[2].get_text().strip()
        atime = tmp_list[5].get_text().strip().replace(' ', '')
        if status == "Passed":
            # print(tid, status, time)
            first_time = atime
            break
    return first_time
    # for ans in ans_list:
    #     tmp_list = ans.find_all("td")
    #     tid = tmp_list[0].get_text().strip()
    #     status = tmp_list[2].get_text().strip()
    #     time = tmp_list[5].get_text().strip()
    #     print(tid, status, time)


if __name__ == '__main__':
    url = myurl
    print(url)
    html = open_html(url)
    soup = BeautifulSoup(html, "lxml")
    # st_list = soup.find_all("tr", class_="evenrow" )
    # st_list = st_list + soup.find_all("tr", class_="oddrow")
    st_list = soup.find_all("tr", attrs={"class":re.compile(r'evenrow|oddrow')})
    cnt = 0
    f = open(file_name, 'w')
    new_url = ""
    for st in st_list:
        tmp_list = st.find_all("td")
        if len(tmp_list) > 6:
            res_list = []
            cnt += 1
            tid = tmp_list[0].get_text()
            uname = tmp_list[2].get_text()
            uid = tmp_list[3].get_text()
            # res_list.append(tid)
            res_list.append(uid)
            # res_list.append(uname)

            for i in range(6, len(tmp_list)):
                c = tmp_list[i].find("font").attrs['color']
                if c == "green":
                    new_url = tmp_list[i].find("a").attrs['href']
                    new_url = domain + new_url + "&start=0&step=100"
                    atime = parse_score_html(new_url)
                    res_list.append(atime)
                else:
                    res_list.append("notpassed")
            # print(len(tmp_list))
            # print(str(st))
            # print(tmp_list[0].get_text())
            # print(tmp_list[2].get_text())
            tmp_str = ""
            for i in res_list:
                tmp_str += str(i) + " "
            print(tmp_str, file = f)
            f.flush()
            print(tmp_str)
            # print(res_list)
    print(cnt)
    # print(new_url)
    # s = parse_score_html(new_url)
    # print(s)


