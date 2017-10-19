import sqlite3
import urllib.request
import http.cookiejar
import urllib.error
import time


class GetProxy:
    proxyList = []
    used_proxy = ''

    def __init__(self):
        print('GetProxy::__init__()')

    def getMoreServer(self, num=100):
        print('GetProxy::getMoreServer()')
        conn = sqlite3.connect('SpiderDB.db')
        c = conn.cursor()
        cursor = c.execute("SELECT IPaddress, port, writeTime FROM proxyServer WHERE anonymous = \'高匿\' ORDER BY proofTime DESC LIMIT %d" % num)
        rl = cursor.fetchall()
        for row in rl:
            self.proxyList.append("%s:%s" % (row[0], row[1]))
        conn.close()


    def proxy_valid(self):
        if self.used_proxy:
            print('GetProxy::proxy_valid()')
            self.proxyList.insert(0, self.used_proxy)

            with sqlite3.connect('SpiderDB.db') as conn:
                t = self.used_proxy.split(':')
                c = conn.cursor()
                c.execute("UPDATE proxyServer SET proofTime=%f, writeTime=%f WHERE IPaddress='%s' and port='%s'" % (time.time(), time.time(), t[0], t[1]))
                conn.commit()


    @property
    def proxyServer(self):
        while not self.proxyList:
            self.getMoreServer()
        self.used_proxy = self.proxyList.pop(0)
        return self.used_proxy


class GetHtml:
    url = ''
    proxy = ''

    def __init__(self, url):
        print('GetHtml::__init__()')
        self.url = url

        # print(self.url)

    def getHtml(self, proxy, time_out=10):
        print('GetHtml::getHtml()')
        self.proxy = proxy
        print('use proxy:', self.proxy)
        headers = {"Accept": "*/*",
                   "Accept-Language": "zh-CN",
                   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063",
                   "Connection": "Keep-Alive"
                   }

        cjar = http.cookiejar.CookieJar()
        proxy = urllib.request.ProxyHandler({'http': self.proxy})
        opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler,
                                             urllib.request.HTTPCookieProcessor(cjar))

        headall = []

        for key, value in headers.items():
            item = (key, value)
            headall.append(item)

        opener.addheaders = headall

        try:
            file = opener.open(self.url, timeout=time_out)

            data = file.read()
            # print(type(data))
            dataString = data.decode('utf-8')
            # print(type(data))

            return dataString

        except urllib.error.HTTPError as e:
            print(e.code)
            print(e.reason)
        except urllib.error.URLError as e:
            print(e.reason)
        except Exception as e:
            print('Exception', type(e))


def test():

    conn = sqlite3.connect('SpiderDB.db')
    c = conn.cursor()
    cursor = c.execute("SELECT IPaddress, port, writeTime FROM proxyServer WHERE anonymous = \'高匿\' ORDER BY proofTime DESC Limit 0,3")
    rl = cursor.fetchall()
    for row in rl:
        print("%s:%s" % (row[0], row[1]))
   

if __name__ == '__main__':
    test()
