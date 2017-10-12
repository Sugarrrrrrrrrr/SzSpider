from getHtmlByUrlAndProxy import GetProxy
from getHtmlByUrlAndProxy import GetHtml
from UpdateProxyDB import UpdateProxyDB


class UrlList:
    urlList = []

    def __init__(self, initial_url):
        self.urlList.append(initial_url)

    def url_append(self, new_url):
        self.urlList.append(new_url)

    def url_append(self):
        return self.urlList.pop(0)


if __name__ == '__main__':









    updb = UpdateProxyDB()

    gp = GetProxy()

    url = "http://www.xicidaili.com/wt/1"
    # url = 'file:///D:/exchange/test.html'
    gh = GetHtml(url)

    up = UpdateProxyDB()
    
    for i in range(100):
        print('----- try', i, '-----')
        html = gh.getHtml(gp.proxyServer)
        if html:
            result = up.update(html)
            print(result)
            if result > 0:
                break
        else:
            print(html)
