import urllib.request
import http.cookiejar
import urllib.error
import re

#url = 'http://www.xicidaili.com/wt/'
url = 'file:///D:/Share/test.html'

headers = {"Accept":"*/*",
           "Accept-Language":"zh-CN",
           "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063",
           "Connection":"Keep-Alive"
    }

cjar = http.cookiejar.CookieJar()
proxy = urllib.request.ProxyHandler({'http':'1.63.107.198:80'})
opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler, urllib.request.HTTPCookieProcessor(cjar))

headall = []

for key,value in headers.items():
    item = (key, value)
    headall.append(item)
    
opener.addheaders = headall

try:
    file = opener.open(url)
except urllib.error.HTTPError as e:
    print(e.code)
    print(e.reason)
except urllib.error.URLError as e:
    print(e.reason)

data = file.read()#.decode('utf-8')
dataString = data.decode('utf-8')

#fhandle = open('D:\\Share\\1.html',"wb")
#fhandle.write(data)
#fhandle.close()

pat_tr = '''<tr class=".*?">[\s\S]*?</tr>'''
pattern_tr = re.compile(pat_tr)
result_tr = pattern_tr.findall(dataString)


for i in range(len(result_tr)):
    print(result_tr[i])
    pat_td = "<td.*?>[\s\S]*?</td>"
    pattern_td = re.compile(pat_td)
    result_td = pattern_td.findall(result_tr[i])
    for j in range(len(result_td)):
        print(j,"---------------")
        print(result_td[j])

    print("input")
    input()

print(len(result_tr))
input()




