#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018-05-11 09:37:35
# Project: Anjuke

from pyspider.libs.base_handler import *
import re

class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('https://nj.fang.anjuke.com/loupan/?pi=baidu-cpcaf-nj-tyong1&kwid=1779038907', callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        page = response.doc('div.list-contents > div.list-results > div.list-page').text()
        page_num_1 = ''.join(re.findall('¹²ÓÐ\s([0-9]*)\s¸ö',page))
        page_num = int(int(page_num_1)/30)
        for i in range(int(page_num)-1):
            url = 'https://nj.fang.anjuke.com/loupan/all/p%s/' %i
            self.crawl(url, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        lp_num = len(re.findall('<h3><span class="items-name">',response.text))
        l = str()
        #print(lp_num)
        for i in range(1,int(lp_num)+1):
            lp_name_css = 'div.list-contents > div.list-results > div.key-list > div:nth-child(%s) > div > .a.lp-name > h3' %i
            adress_css = 'div.list-contents > div.list-results > div.key-list > div:nth-child(%s) > div > a.address' %i
            huxing_mianji_css = 'div.list-contents > div.list-results > div.key-list > div:nth-child(%s) > div > a.huxing' %i
            price_css = 'div.list-contents > div.list-results > div.key-list > div:nth-child(%s) > a.favor-pos > p.price' %i
            list_dp_css = 'div.list-contents > div.list-results > div.key-list > div:nth-child(%s) > div > a.lp-name ' %i
            tag_css = 'div.list-contents > div.list-results > div.key-list > div:nth-child(%s) > div > a.tags-wrap ' %i
            lp_name = response.doc(lp_name_css).text().strip().replace(',',' ')
            adress_1 = response.doc(adress_css).text().strip().replace(',',' ')
            adress = ''.join(adress_1.split())
            huxing_mianji_1 = response.doc(huxing_mianji_css).text().strip().replace(',',' ')
            huxing_mianji = ''.join(huxing_mianji_1.split())
            price = response.doc(price_css).text().strip().replace(',',' ')
            list_dp = response.doc(list_dp_css).text().strip().replace(',',' ')
            tag = response.doc(tag_css).text().strip().replace(',',' ')
            p = ','.join([lp_name,adress, huxing_mianji, price, list_dp, tag]) + '\n'
            l += p
        #print(l)
        return l
               
        
