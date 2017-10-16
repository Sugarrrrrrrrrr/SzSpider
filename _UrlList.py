
class UrlList:
    urlList = []

    def __init__(self, initial_url = "file:///D:/exchange/test.html"):
        self.urlList.append(initial_url)

    def url_append(self, new_url):
        self.urlList.append(new_url)

    def url_pop(self):
        if self.urlList:
            return self.urlList.pop(0)
        else:
            return ''


if __name__ == '__main__':
    print('main()')
