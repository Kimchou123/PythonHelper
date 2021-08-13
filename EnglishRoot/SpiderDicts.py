import requests
import re
import json
from bs4 import BeautifulSoup


staticcookies='DICTWEB_LOGIN_NAME=74657374;DICTWEB_LOGIN_PASSWORD=313233343536;JSESSIONID=9BD5BED3F5063FF83B44105B295A7BBA;'
#获取Cookies
def get_dictsCookies(logId,pwd,typ):
    # cos='';
    # co={'DICTWEB_LOGIN_NAME': '74657374', 'DICTWEB_LOGIN_PASSWORD': '313233343536', 'JSESSIONID': '9DCAED6B4504CAC6EA3164CD25E6E475'}
    # for name,value in co.items():
    #         print(name)
    #         print(value)
    #         cos += '{0}={1};'.format(name, value)
    #         print(cos)
    #         return cos;
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'}
    data={'phone':logId,'pwd':pwd,'denglu':typ}
    r=requests.post("http://www.dicts.cn/dict/dict/dict!login.asp",data=data,headers=headers)
    if r.status_code==200:
        cookie = ''
        # for name, value in r.cookies:
        #     cookie += '{0}={1};'.format(name, value)
        cookies = requests.utils.dict_from_cookiejar(r.cookies)
        for key,value in cookies.items():
            cookie += '{0}={1};'.format(key, value)
        global staticcookies
        staticcookies=cookie
        # for cookie in r.cookies:
        #      print(cookie['DICTWEB_LOGIN_NAM'])
            #  cookie_dict[cookie['name']]=cookie['value']
        # print(r.cookies)
        # print(r.content)
#解析网页
def get_dictsHtml(word):
    try:
        if(staticcookies==''):
            return '请先登录'
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
        'Cookie':staticcookies,
        'Origin': 'http://www.dicts.cn'}
        url='http://www.dicts.cn/dict/dict/dict!searchhtml3.asp?id='+word
        r=requests.post(url,headers=headers)
        if r.status_code==200:
            con= str(r.content, encoding = "utf-8")
            if(con.__contains__('login')):
                return '请重新登录'  
            hurl='http://www.dicts.cn'+r.text#+str(r.content, encoding = "utf-8")
            htm=requests.get(hurl,headers=headers)
            soup = BeautifulSoup(htm.text, 'lxml')
            for span in soup.find_all('div', attrs={"class":"jsmind-inner"}):#词源树
                print(span)
    except:
        return ""
def exp():
    if(staticcookies==''):
        get_dictsCookies('test','416266','登录')
    print(get_dictsHtml("extort"))

#exp()

def simple():
    file = open('F:\周鑫\Project\GitHub\PythonHelper\EnglishRoot\\ache.html',encoding='utf-8') 
    html = file.read() 
    bs = BeautifulSoup(html,"html.parser")      
    for span in bs.find_all("script"):#词源树
        da=span.string 
        if(da!=None):
            # print(da.find('"data":[{'))
            # print(da.find('}]'))    
            str= da[da.find('"data":[{')+7:da.find('}]')+2] 
            if(str!=''):
                 res=json.loads()
                 print(res)
        print("-----------")    
simple()

