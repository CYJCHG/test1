# -*- coding:utf-8 -*-
import ssl
ssl._create_default_https_context = ssl._create_unverified_context  # 全局都取消验证 SSL 证书
# import random
import requests
import time
# import datetime
import pymysql
import traceback
from bs4 import BeautifulSoup as bs
import re
import importlib,sys 
importlib.reload(sys)
#sys.setdefaultencoding('utf-8')

# def get_html(url):
#     try:
#         response=requests.get(url)
#         if response.status_code==200:
#             soup=BeautifulSoup(response.text,'lxml')
#             return soup
#         else:
#             print response.status_code
#
#     except Exception,e:
#         print "失败"
#         print e

######获得代理
# def get_proxies():
#     proxies = list(set(requests.get("http://localhost:8080").text.split('\n')))
#     return proxies

def get_html(shop_url):
    while True:
        try:
            headers = {
                'Host': 'stockdata.stock.hexun.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
                'Cookie':'__jsluid=1da46053ffc9dfabb1199c2c2717555f; HexunTrack=SID=20180506102758146b13f49c4605844a2b14c80e610fb0577&CITY=0&TOWN=0'
                      }
            # proxies = get_proxies()
            # index = random.randint(1, len(proxies) - 1)
            # proxy = {"http": "http://" + str(proxies[index]), "https": "http://" + str(proxies[index])}
            # print ('Now Proxy is : ' + str(proxy) + ' @ ' + str(datetime.datetime.now()))
            try:
                response = requests.get(shop_url, timeout=50,  headers=headers)
            except Exception as e:
                if str(e).find('10061') >= 0 or str(e).find('403') >= 0:
                    time.sleep(1)
                    # index = random.randint(1, len(proxies) - 1)
                    # proxy = {"http": "http://" + str(proxies[index]), "https": "http://" + str(proxies[index])}
                    try:
                        #driver = selenium.webdriver.Chrome()
                        driver = selenium.webdriver.PhantomJS()
                        driver.get(shop_url)
                        time.sleep(1)
                        driver.maximize_window()
                        cookie = [item["name"] + "=" + item["value"] for item in driver.get_cookies()]
                        # print cookie
                        cookiestr = ';'.join(item for item in cookie)
                        headers['Cookie'] = cookiestr
                        driver.quit()
                        print ('Cookie 获取成功')
                    except:
                        print ('Cookie 获取失败')
                    try:
                        response = requests.get(shop_url, timeout=50,  headers=headers)
                    except:
                        print ('再次尝试失败')
                        return shop_url
                else:
                    print (traceback.format_exc())
                    return shop_url
            print (response.status_code)
            if response.status_code == 200:
                soup = bs(response.text, 'lxml')
                if str(soup.text).find('验证中心'):
                    print ('需要输入验证码')
                    try:
                        driver = selenium.webdriver.PhantomJS()
                        driver.get(shop_url)
                        time.sleep(1)
                        cookie = [item["name"] + "=" + item["value"] for item in driver.get_cookies()]
                        # print cookie
                        cookiestr = ';'.join(item for item in cookie)
                        headers['Cookie'] = cookiestr
                        driver.quit()
                        print ('Cookie 获取成功')
                    except:
                        print ('Cookie 获取失败')
                    try:
                        response = requests.get(shop_url, timeout=50, headers=headers)
                        response.encoding = 'gb2312'
                        print ('解析成功')
                        return response.text
                    except:
                        print ('验证失败')
                        return shop_url
                else:
                    response.encoding = 'gb2312'
                    return response.text
            elif response.status_code == 404:
                return '页面不存在'
            else:
                return 'error'
        except:
            print (traceback.format_exc())
            return 'error'


def get_detail(url,p):
    try:
        conn = None
        conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", passwd="594740",db="test",charset="utf8")
        cursor = conn.cursor()
        html = get_html(url)
        print (html)
        while html=='页面不存在':
            print ('页面不存在')
            break
        while html=='error' or html=='url':
            print ('需要重新解析该网页')
            sql_url = "INSERT  hexun_error1  VALUES ('%s')" % (p)
            try:
                cursor.execute(sql_url)
                conn.commit()
                break
            except:
                print (traceback.format_exc())
                conn.rollback()
            break
        else:
            try:
                industry=re.findall("industry:'(.*?)',",html)
                print (industry[0])
                print (len(industry))
                industryrate=re.findall("industryrate:'(.*?)',",html)
                Pricelimit=re.findall("Pricelimit:'(.*?)',",html)
                stockNumber=re.findall("stockNumber:'(.*?)',",html)
                lootingchips=re.findall("lootingchips:'(.*?)',",html)
                Scramble=re.findall("Scramble:'(.*?)',",html)
                rscramble=re.findall("rscramble:'(.*?)',",html)
                Strongstock=re.findall("Strongstock:'(.*?)',",html)
                for i in range(len(industry)):
                    print (industry[i],industryrate[i],Pricelimit[i],stockNumber[i],lootingchips[i],Scramble[i],rscramble[i],Strongstock[i])
                    while True:
                        try:
                            cursor.execute("insert into hexun_2015 values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % \
                                (0,p,industry[i],industryrate[i],Pricelimit[i],stockNumber[i],lootingchips[i],Scramble[i],rscramble[i],Strongstock[i]))
                            conn.commit()
                            print("p=",p,'------------save end--------------')
                            break

                        except Exception as e:
                            print ("插入错误")
                            print (e)
                            sql_url = "INSERT hexun_error1  VALUES ('%s')"%(p)
                            try:
                                cursor.execute(sql_url)
                                conn.commit()
                                break
                            except:
                                print (traceback.format_exc())
                                conn.rollback()

            except Exception as e:
                print ('正则匹配错误')
                sql_url = "INSERT  hexun_error1  VALUES ('%s')" %(p)
                try:
                    cursor.execute(sql_url)
                    conn.commit()
                except:
                    print (traceback.format_exc())
                    conn.rollback()
    except Exception as e:
        print (traceback.format_exc())
        print ('数据库连接错误')
    finally:
        if conn != None:
            cursor.close()  # 关闭游标
            conn.close()  # 释放数据库资源


# if __name__=='__main__':
#     pages=[32,37,85,86,88,89,120,145,167]
#     for page in pages:
#         url='http://stockdata.stock.hexun.com/zrbg/data/zrbList.aspx?date=2015-12-31&count=20&pname=20&titType=null&page={}&callback=hxbase_json11525657153794'.format(page)
#         get_detail(url,page)
#
if __name__=='__main__':
    for page in range(1,178):
        url='http://stockdata.stock.hexun.com/zrbg/data/zrbList.aspx?date=2015-12-31&count=20&pname=20&titType=null&page={}&callback=hxbase_json11525657153794'.format(page)
        get_detail(url,page)


