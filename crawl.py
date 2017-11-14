import errno
from pyquery import PyQuery as pq
from lxml import etree
from urllib import request, parse
import re
import os


class meizi:
    def __init__(self):
        self.urls = []
        self.headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}

    # 获取一共多少页
    def getnum(self, url):
        req = request.Request(headers=self.headers, url=url)
        html = request.urlopen(req)
        d = pq(html.read().decode("utf-8"))
        # 获取一共多少页
        pagenum = d(".info").text()
        patt = re.compile("共(.*?)页", re.S)
        num = re.findall(patt, pagenum)
        return num[0]

    # 把每页的url添加
    def addpageurl(self, url):
        num = self.getnum(url)
        sum = int(num)
        for i in range(1, sum + 1, 1):
            tmpurl = url + '/' + str(i)
            self.getpageurl(tmpurl)
        print(self.urls.__len__())

    # 把一个页面的图集链接加入urls数组
    def getpageurl(self, url):
        req = request.Request(headers=self.headers, url=url)
        html = request.urlopen(req)
        d = pq(html.read().decode("utf-8"))
        pic = d(".pic")('ul')
        lis = pic('li')
        for ll in lis.items():
            a0 = ll('a').eq(0)
            href = a0.attr('href')
            self.urls.append(href)

    # 下载图片
    def downloadimg(self, url, dir):
        req = request.Request(headers=self.headers, url=url)
        html = request.urlopen(req)
        d = pq(html.read().decode("utf-8"))
        d('#opic')
        pic = d(".content")('img')
        picsrc = pic.attr('src')
        # 获取下载图片前缀
        ptt = re.compile("(.*?)/..jpg")
        repicsrc = re.findall(ptt, picsrc)
        pageneum = d('#page')('a').eq(-2).text()
        num = int(pageneum) + 1
        title = d('.article')('h2').text()
        print(title)
        path = self.mkdir(dir + '/' + title)
        for i in range(1, num, 1):
            s = str(i)
            mz.saveImg(str(repicsrc[0]) + '/' + s + '.jpg', dir + '/' + title + '/' + s + '.jpg', url)

    # 保存图片
    def saveImg(self, imageURL, filename, refurl):
        try:
            # headers = {"User-Agent": self.user_agent}
            # 添加refer，否则会无法下载
            # refer = 'http://www.mmjpg.com/mm/988';
            self.headers = {'Referer': refurl}
            req = request.Request(imageURL, headers=self.headers)
            u = request.urlopen(req)
            data = u.read()
            f = open(filename, 'wb')
            f.write(data)
            f.close()
        except request.URLError as e:
            print('error----->')
            print(e.reason + e.code())

    # 创建文件夹,可以创建多级目录
    def mkdir(self, path):
        try:
            os.makedirs(path)
        except OSError as exc:  # Python >2.5 (except OSError, exc: for Python <2.5)
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise

    def start(self, url, dir):
        self.addpageurl(url);
        for uu in self.urls:
            self.downloadimg(uu, dir)


mz = meizi()
url = 'http://www.mmjpg.com/tag/xiaoqingxin/2'
dir = '/calu/美女图'
mz.start('http://www.mmjpg.com/tag/disi', dir)
