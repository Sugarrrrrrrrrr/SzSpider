import urllib.request
import http.cookiejar
import urllib.error
import re
import time
import sqlite3

#url = 'http://www.xicidaili.com/wt/2'
url = 'file:///D:/exchange/test.html'

headers = {"Accept":"*/*",
           "Accept-Language":"zh-CN",
           "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063",
           "Connection":"Keep-Alive"
    }

cjar = http.cookiejar.CookieJar()
proxy = urllib.request.ProxyHandler({'http': '118.178.124.33:3128'})
opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler, urllib.request.HTTPCookieProcessor(cjar))

headall = []

for key,value in headers.items():
    item = (key, value)
    headall.append(item)
    
opener.addheaders = headall

dataString = ''
try:
    file = opener.open(url, timeout = 5)
    data = file.read()
    #print(data)
    dataString = data.decode('utf-8')

    #fhandle = open('D:\\exchange\\2.html',"wb")
    #fhandle.write(data)
    #fhandle.close()
    
except urllib.error.HTTPError as e:
    print(e.code)
    print(e.reason)
except urllib.error.URLError as e:
    print(e.reason)
except Exception as e:
    print(str(e))

pat_tr = '''<tr class=".*?">[\s\S]*?</tr>'''
pattern_tr = re.compile(pat_tr)
result_tr = pattern_tr.findall(dataString)

count = 0
for i in range(len(result_tr)):
    print(result_tr[i])
    pat_td = "<td.*?>[\s\S]*?</td>"
    pattern_td = re.compile(pat_td)
    result_td = pattern_td.findall(result_tr[i])
    for j in range(len(result_td)):
        print(j,"---------------")
        print(result_td[j])
        # 提取字段
        if j == 0:  # country
            pat_country = '<td class="country">(.*alt="(.*)" />)*</td>'
            temp = re.search(pat_country, result_td[j])
            print(type(temp))
            if(temp.group(2)):
                country = temp.group(2)
            else:
                country = ''
            print(country)
            
        elif j == 1: # IPaddress
            pat_IPaddress = '<td>(.*)</td>'
            temp = re.search(pat_IPaddress, result_td[j])
            IPaddress = temp.group(1)
            print(IPaddress)
            
        elif j == 2: # port
            pat_port = '<td>(.*)</td>'
            temp = re.search(pat_port, result_td[j])
            port = temp.group(1)
            print(port)
            
        elif j == 3: # location
            pat_location = '<td>\n        (<a href=".*">(.*)</a>)*(.*)\n      </td>'
            temp = re.search(pat_location, result_td[j])
            if temp.group(2):
                location = temp.group(2)
            else:
                location = temp.group(3) 
            print(location)
            
        elif j == 4: # anonymous
            pat_anonymous = '>(.*)</td>'
            temp = re.search(pat_anonymous, result_td[j])
            anonymous = temp.group(1)
            print(anonymous)
            
        elif j == 5: # proxyType
            pat_proxyType = '<td>(.*)</td>'
            temp = re.search(pat_proxyType, result_td[j])
            proxyType = temp.group(1)
            print(proxyType)
            
        elif j == 6: # speed
            pat_speed = 'title="(.*?)"'
            temp = re.search(pat_speed, result_td[j])
            speed = temp.group(1)
            print(speed)

        elif j == 7: # connectTime
            pat_connectTime = 'title="(.*?)"'
            temp = re.search(pat_connectTime, result_td[j])
            connectTime = temp.group(1)
            print(connectTime)

        elif j == 8: # survivalTime
            pat_survivalTime = '<td>(.*)</td>'
            temp = re.search(pat_survivalTime, result_td[j])
            survivalTime = temp.group(1)
            print(survivalTime)

        elif j == 9: # proofTime
            pat_proofTime = '<td>(.*)</td>'
            temp = re.search(pat_proofTime, result_td[j])
            proofTime = temp.group(1)
            proofTime_float = time.mktime(time.strptime(proofTime,"%y-%m-%d %H:%M"))
            print(proofTime)
            print(proofTime_float)

    # writeTime
    writeTime = time.strftime("%y-%m-%d %H:%M", time.localtime())
    writeTime_float = time.time()
    print(writeTime)
    print(writeTime_float)

    # INSERT
    conn = sqlite3.connect('SpiderDB.db')
    c = conn.cursor()
    rl = c.execute("select IPaddress, port, proofTime from proxyServer where IPaddress = '%s' and port = '%s'" % (IPaddress, port)).fetchall()


    if len(rl)==0 or (len(rl)>0 and rl[0][2]>proofTime_float):
        #print('insert--------')
        c.execute("INSERT OR replace INTO proxyServer (country, IPaddress, port, location, anonymous, proxyType, speed, connectTime, survivalTime, proofTime, writeTime) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', %f, %f)" % (country, IPaddress, port, location, anonymous, proxyType, speed, connectTime, survivalTime, proofTime_float, writeTime_float))
        conn.commit()
        count += 1
    conn.close()
                    
    #print("input")
    #input()

print(len(result_tr))
print("insert",count)
print("input")
input()




