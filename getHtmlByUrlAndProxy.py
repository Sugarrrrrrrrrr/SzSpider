import sqlite3
import urllib.request
import http.cookiejar
import urllib.error


class GetProxy:
    proxyList = []

    def __init__(self):
        print('GetProxy::__init__()')

    def getMoreServer(self):
        print('GetProxy::getMoreServer()')
        conn = sqlite3.connect('SpiderDB.db')
        c = conn.cursor()
        cursor = c.execute("select IPaddress, port, writeTime from proxyServer order by writeTime ASC")
        rl = cursor.fetchall()
        for row in rl:
            self.proxyList.append("%s:%s" % (row[0], row[1]))


    @property
    def proxyServer(self):
        while not self.proxyList:
            self.getMoreServer()
        return self.proxyList.pop(0)


class GetHtml:
    url = ''
    proxy = ''

    def __init__(self, url):
        print('GetHtml::__init__()')
        self.url = url

        print(self.url)
        

    def getHtml(self, proxy):
        print('GetHtml::getHtml()')
        self.proxy = proxy
        print(self.proxy)
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
            file = opener.open(self.url, timeout = 5)
            
            data = file.read()
            print(type(data))
            dataString = data.decode('utf-8')
            print(type(data))

            return dataString

        except urllib.error.HTTPError as e:
            print(e.code)
            print(e.reason)
        except urllib.error.URLError as e:
            print(e.reason)
        except Exception as e:
            print('Exception', type(e))




if __name__ == '__main__':
    gp = GetProxy()

    url = "http://www.xicidaili.com/wt/"
    gh = GetHtml(url)
    
    for i in range(20):
        print('----- try',i,'-----')
        html = gh.getHtml(gp.proxyServer)
        print(html)
