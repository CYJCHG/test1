
#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018-05-22 14:10:46
# Project: test

from pyspider.libs.base_handler import *
import re

class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('http://newhouse.nanjing.fang.com/house/s/', callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
       #page = response.doc('#sjina_C01_47 > ul > li.fr ').text()
       #page_num_1 = ''.join(re.findall('¹²ÓÐ\s([0-9]*)\s¸ö',page))
       #page_num = 22
        #int(int(page_num_1)/20)
        for i in range(int(23)):
            url = 'http://newhouse.nanjing.fang.com/house/s/b9%s/' %i
            self.crawl(url, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        #lp_num = len(re.findall('<span class="nlcd-name">',response.text))
        l = str()
        #print(lp_num)
        #for i in range(1,int(lp_num)+1):
        for i in range(20,40):    
            nlcd_name_css = '#sjina_C%s_02 > a' %i
            adress_css = '#sjina_C%s_06 > a' %i
            huxing_mianji_css = '#sjina_C%s_04' %i
            status_css = '#sjina_C%s_07 > span' %i
            price_css = '#newhouse_loupai_list > ul > li:nth-child(%s) > div > div.nlc_details > div.nhouse_price ' %(i-20)
            style_css = '#sjina_C%s_07 > a:nth-child(2) ' %i
            reviews_css = '#sjina_C%s_03 > a > span' %i
            nlcd_name = response.doc(nlcd_name_css).text().strip().replace(',',' ')
            #print(nlcd_name)
            adress = response.doc(adress_css).text().strip().replace(',',' ')
            huxing_mianji = response.doc(huxing_mianji_css).text().strip().replace(',',' ')
            status = response.doc(status_css).text().strip().replace(',',' ')
            price = response.doc(price_css).text().strip().replace(',',' ')
            style = response.doc(style_css).text().strip().replace(',',' ')
            reviews = response.doc(reviews_css).text().strip().replace(',',' ')
            p = ','.join([nlcd_name,adress, huxing_mianji, status, price, style, reviews]) + '\n'
            l += p
            #print(l)
        return l


