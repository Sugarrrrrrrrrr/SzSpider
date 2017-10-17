from _getHtmlByUrlAndProxy import GetProxy, GetHtml
from _UpdateProxyDB import UpdateProxyDB
from _UrlList import UrlList

import time
import sqlite3



def main():
    gp = GetProxy()
    up = UpdateProxyDB()
    ul = UrlList()

    url_ = "http://www.xicidaili.com/wt/%s"
    for i in range(10):
       ul.url_append(url_ % str(i+1))

    url = ul.url_pop()
    while url:
        gh = GetHtml(url)
        for i in range(100):
            print('-----', url, '----- try', i, '-----')
            html = gh.getHtml(gp.proxyServer)
            if html:
                result = up.update(html)
                print(result)
                if result > 0:
                    gp.proxyList=[]
                    gp.proxy_valid()
                    break
            else:
                print(html)

        url = ul.url_pop()
    

if __name__ == '__main__':
    main()
