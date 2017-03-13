# -*- coding: utf-8 -*-
#by:Lov3
#date:2017-3-14
import json
import requests
from lxml import etree
from urllib import request
import re
import threading




def geturl(search,page):                 #输入搜索和数量
    urls=[]
    for i in range(0,int(page)):
        url="http://search.bilibili.com/all?keyword="+search+"&page="+str(i)+"&order=totalrank"
        urls.append(url)
    return urls
def gethtml(url):                   #获取网页源代码取得带有cid的链接
    htm=requests.get(url)
    html=etree.HTML(htm.content)
    href=html.xpath('/html/body/div[5]/ul/li/a/@href')
    all_urls=[]
    for urls in href:
        all_urls.append("http:"+urls)
    return all_urls

def getcid(url):                #爬取cid链接取得cid
    htm=requests.get(url)
    html=str(htm.content)
    reg='cid=\d{1,12}'
    res=re.compile(reg)
    path=re.findall(res,html)
    for cid in path:
        return cid

def getpath(cid):               #抓取cid获取下载链接
    url="http://www.ibilibili.com/api/bilibili/get_video_by_cid.php?"+cid+"&ptype=flv"
    data=requests.get(url).text
    try:
        datas=json.loads(data)['src']
    except KeyError:
        pass
    return datas
def down(url,name):             #定义下载函数方便启用多线程
    request.urlretrieve(url,name)


print("input your search:",end="\t")
search=input()
print("input your search pages:",end="\t")
page=input()
urls=geturl(search,page)
links=[]
for url in urls:
    html=gethtml(url)
    for xml in html:
        #print(xml)
        links.append(xml)
print(len(links))

cids=[]
for id in links:
    cid=getcid(id)
    #print(cid)
    cids.append(cid)
print(len(cids))
i=1
Theads=[]
for us in cids:
    path=getpath(us)
    print("获取下载链接"+path)
    name=search+str(i)+'.mp4'
    t=threading.Thread(target=down,args=(path,name))
    Theads.append(t)
    #request.urlretrieve(path,search+str(i)+'.mp4')
    i+=1
print("=====开始下载请稍等=====")
for mp4 in Theads:
	mp4.start()
for mp4 in Theads:
	mp4.join()
print("全部下载完成")


