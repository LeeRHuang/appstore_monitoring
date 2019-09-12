# -*- coding:utf-8 -*-
import requests
import json
import threading as thd
import time
from bs4 import BeautifulSoup
import ConfigParser
import os

'''配置请求头'''
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
}



def loadData(appname):
    '''
    请求数据
    :return: soup对象
    '''
    if appname == 'laiqiandashi':
        url = 'https://itunes.apple.com/cn/app/id1475225384'
    if appname == 'duduqianguan':
        url = 'https://itunes.apple.com/cn/app/id1366733557'
    # if appname == 'laiqiandashi':
    #     url = 'https://itunes.apple.com/cn/app/id1383686333'
    # if appname == 'yeguoqianhe':
    #     url = 'https://itunes.apple.com/cn/app/id1354762033'

    print(time.time())
    # thd.Timer(1 * 5, loadData, (appname,)).start()

    print('开始爬取: ', url)

    wb_data = requests.get(url, headers=headers, verify=False)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    titleArray = soup.select('head title')
    if len(titleArray) > 0:
        title = titleArray[0].get_text()
        if title:
            tempTitle = title.encode('utf-8')
            if tempTitle.startswith('正在连接到'):
                print(appname, 'has been removed from App Store')
                handleInIData(appname)
            else:
                print(appname, 'still on App Store')
            print(tempTitle)


def sendMessage(appname):
    body = {
  "text": "Message from monitoring",
  "attachments": [
    {
      "title": "Warning",
      "text": appname +' '+ 'has been removed from App Store',
      "color": "#fa623d",
      "images": [{"url":"https://ss0.bdstatic.com/70cFuHSh_Q1YnxGkpoWK1HF6hhy/it/u=117847195,3417012957&fm=26&gp=0.jpg"}]
    }
  ]}

    url = 'https://hook.bearychat.com/=bwGRT/incoming/e4a4404b9bcfbfebcbc38b31bddc6f2b'
    message_headers = {
        "Content-Type": "application/json; charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
    }
    response = requests.post(url, data=json.dumps(body), headers=message_headers).text
    print(response)


def handleInIData(appname):

    curpath = os.getcwd()
    cfgpath = os.path.join(curpath, "config.ini")
    # print(cfgpath)  # cfg.ini的路径

    # 创建管理对象
    conf = ConfigParser.ConfigParser()

    # 读ini文件
    # conf.read(cfgpath, encoding="utf-8")  # python3

    conf.read(cfgpath)  # python2

    # 获取所有的section
    sections = conf.sections()
    # print('sections is', sections)

    for s in sections:
        items = conf.items(s)
        # print('items is', items)
        if items[0][1] == appname:
            if items[2][0] == 'revokecount':
                count = items[2][1]
                print('count is :', count)
                revokecount = int(count)
                if revokecount > 4:
                    print "超过最大次数了！！！"
                else:
                    sendMessage(appname)
                    revokecount += 1
                    conf.set(appname, "revokecount", str(revokecount))  # 写入发送次数
                    conf.write(open(cfgpath, "r+"))  # 追加模式写入

                print('revokecount is', revokecount)



# if __name__ == '__main__':
print "start"
loadData('laiqiandashi')
# time.sleep(2)
loadData('duduqianguan')
    # time.sleep(2)
    # loadData('laiqiandashi')
    # time.sleep(2)
    # loadData('yeguoqianhe')
print "end"

