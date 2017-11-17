from _getHtmlByUrlAndProxy import GetProxy, GetHtml
from _UpdateProxyDB import UpdateProxyDB
from _UrlList import UrlList

from datetime import datetime


def write_log_file(read, insert, url, proxy_server):

    if url.startswith('file'):
        return

    t = datetime.now()
    date = t.strftime('%Y-%m-%d')
    time = t.strftime('%Y-%m-%d %H:%M:%S')

    with open(r'log/log_%s.txt' % date, 'at', encoding='utf-8') as file:
        if read > 0:
            file.write(r'''%s
read %d insert %d
from %s
with %s
----------------------------------------
''' % (time, read, insert, url, proxy_server))
        else:
            file.write(r'''%s
bad proxy server: %s
----------------------------------------
''' % (time, proxy_server))


def main(num=100):
    gp = GetProxy()
    up = UpdateProxyDB()
    ul = UrlList(initial_url = '')

    url_ = "http://www.xicidaili.com/wt/%s"
    for i in range(10):
       ul.url_append(url_ % str(i+1))

    url = ul.url_pop()
    while url:
        gh = GetHtml(url)
        for i in range(num):
            print('-----', url, '----- try', i+1, '-----')
            html = gh.getHtml(gp.proxyServer)
            if html:
                result, count = up.update(html)

                write_log_file(result, count, url, gp.used_proxy)

                if result > 0:
                    if not url.startswith('file'):
                        gp.proxy_valid()
                    if count > 0:
                        gp.proxyList = []
                    break
            else:
                print(html)

            if i == num-1:
                ul.url_append(url)

        url = ul.url_pop()
    

if __name__ == '__main__':
    main(100)
