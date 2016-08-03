# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.selector import Selector
from spider_enterprise.items import baseInfoItem, playInfoItem
import re
import sys
import json
reload(sys)
sys.setdefaultencoding( "utf-8" )
print sys.path

class DmozSpider(scrapy.Spider):
    name = "dmoz"
    
    start_urls = [
        "http://www.smeimdf.org.cn/news/searchEntpAudit.jsp",
    ]

    def getProvinceInf(self):
        self.code2name = {}
        self.province_code = []
        self.legalButNotNum = {}
        dic    = {}
        resdic = []
        with open('province_list_data.txt','r') as f:
            txt = f.read()
            dic = json.loads(txt)
            for rlst in dic['data']:
                if rlst[0] not in dic:
                    dic[rlst[0]] = []
                dic[rlst[0]].append({'cityname':rlst[1], 'citycode':rlst[2]})
                self.code2name[rlst[2]] = rlst[1]

            for dic1 in dic[0]:
                province_code = dic1['citycode']
                province_name = dic1['cityname']
                self.province_code.append(province_code)
                if province_code in dic:
                    for dic2 in dic[province_code]:
                        #print dic2
                        city_code = dic2['citycode']
                        city_name = dic2['cityname']
                        if city_code in dic:
                            for dic3 in dic[city_code]:
                                area_code = dic3['citycode']
                                area_name = dic3['cityname']
                                resdic.append({'province_code':province_code, 'city_code':city_code, 'area_code':area_code, 'province_name':province_name, 'city_name':city_name, 'area_name':area_name})
                        else:
                            resdic.append({'province_code':province_code, 'city_code':'', 'area_code':city_code, 'province_name':province_name, 'city_name':province_name, 'area_name':city_name})
        return resdic

    def parse(self, response):
        areadic  = self.getProvinceInf()
        '''get province info fund_type=2
        '''
        '''
        for ddic in areadic:
            next_url1 = "%s?fund_type=2&province=%s&city=%s&area=%s&i_year=&entp_name=" % (response.url, ddic['province_code'], ddic['city_code'], ddic['area_code'])
            yield Request(next_url1, callback = self.parseAllPage)
            next_url2 = "%s?fund_type=1&province=%s&city=%s&area=%s&i_year=&entp_name=" % (response.url, ddic['province_code'], ddic['city_code'], ddic['area_code'])
            yield Request(next_url2, callback = self.parseAllPage)
        '''

        url = response.url.replace('Entp','')
        for ddic in areadic:
            next_url1  = "%s?fund_type=2&province=%s&city=%s&area=%s&i_year=2014&i_index=01" % (url, ddic['province_code'], ddic['city_code'], ddic['area_code'])
            yield Request(next_url1, meta={'area':ddic, 'year':'2014'}, callback = self.parseAllPage)
            next_url2  = "%s?fund_type=2&province=%s&city=%s&area=%s&i_year=2015&i_index=01" % (url, ddic['province_code'], ddic['city_code'], ddic['area_code'])
            yield Request(next_url2, meta={'area':ddic, 'year':'2015'}, callback = self.parseAllPage)
            next_url3  = "%s?fund_type=1&province=%s&city=%s&area=%s&i_year=2014&i_index=01" % (url, ddic['province_code'], ddic['city_code'], ddic['area_code'])
            yield Request(next_url3, meta={'area':ddic, 'year':'2014'}, callback = self.parseAllPage)
            next_url4  = "%s?fund_type=1&province=%s&city=%s&area=%s&i_year=2015&i_index=01" % (url, ddic['province_code'], ddic['city_code'], ddic['area_code'])
            yield Request(next_url4, meta={'area':ddic, 'year':'2015'}, callback = self.parseAllPage)

    def parseAllPage(self, response):
        sel         =  Selector(response)
        hrefAll     = sel.xpath('//div[@class="pages"]/a/@href').extract()
        maxpage     = 1
        for href in hrefAll:
            try:
                maxpage = max(int(href.split(':')[1].split('\'')[1]), maxpage)
            except:
                pass
        '''test maxpage = 2
        '''
        #maxpage = 2 #gotta delete
        res = response.url.split('?')
        goto = False
        if res[0].find('searchAudit') >= 0:
            goto = True
        for p in xrange(maxpage):
            next_url = '%s&cpf.cpage=%d&method=search&' % (response.url, p+1)
            if goto:
                yield Request(next_url, meta={'area':response.meta['area'], 'year':response.meta['year']}, callback = self.parsePlayInfo)
            else:
                yield Request(next_url, callback = self.parseBaseInfo)

    def parsePlayInfo(self, response):
        sel         =  Selector(response)
        allTr       =  sel.xpath('//table/tr')
        itemStruct  = ["index", "name", "projectname", "projectkind", "projectproperty", "fundtype"]
        fundtype    = response.url.split('?')[1].split('&')[0].split('=')[1]
        for tr in xrange(len(allTr)):
            if tr <= 0:continue
            item  = playInfoItem()
            item['fundtype'] = fundtype
            item['year']     = response.meta['year']
            tdAll = allTr[tr].xpath('.//td/text()').extract()
            for td in xrange(len(tdAll)):
                ans = ''
                ans = tdAll[td].replace(u'\xa0','')
                item[itemStruct[td]] = ans
            if not item['projectname']:continue
            item['area'] = response.meta['area']
            if self.nameIsLegal(item['projectname']):
                next_url = "https://www.baidu.com/s?wd=%s&rsv_bp=0&rsv_spt=3&rsv_n=2&inputT=6391" % item['name']
                yield Request(next_url, meta={'name':item['name'], 'item':item}, callback = self.parsePhoneNumByBaidu)
            '''
            else:
                item['phone'] = item['mobilephone'] = ''
                yield item
            '''

    def parseBaseInfo(self, response):
        sel         =  Selector(response)
        allTr       =  sel.xpath('//table/tr')
        itemStruct  =  ["index", "name", "area", "registertime", "enterpriseproject", "teamplayproject", "enterprisecoach", "serviceoutsourcing", "fundtype"]
        fundtype    = response.url.split('?')[1].split('&')[0].split('=')[1]

        ar = response.url.split('?')[1].split('&')
        pc, cc, ac = ar[1].split('=')[1], ar[2].split('=')[1], ar[3].split('=')[1]
        for tr in xrange(len(allTr)):
            if tr <= 1:continue
            item  = baseInfoItem()
            item['fundtype'] = fundtype
            tdAll = allTr[tr].xpath('.//td/text()').extract()
            for td in xrange(len(tdAll)):
                ans = tdAll[td].replace(u'\xa0','')
                if tdAll[td]   == u'\u221a':
                    ans = True
                elif tdAll[td] == u'\xd7':
                    ans = False

                if td == 2: #area
                    pn = cn = an = ''
                    try:
                        if pc:
                            pn = self.code2name[int(pc)]
                    except:
                        pass
                    
                    try:
                        if cc:
                            cn = self.code2name[int(cc)]
                        else:
                            cn = pn
                    except:
                        pass
                    
                    try:
                        if ac:
                            an = self.code2name[int(ac)]
                    except:
                        pass
                    ans = '%s,%s,%s' % (pn, cn, an)
                item[itemStruct[td]] = ans
            if item['area'] == ',,':continue
            if self.nameIsLegal(item['name']):
                next_url = "https://www.baidu.com/s?wd=%s&rsv_bp=0&rsv_spt=3&rsv_n=2&inputT=6391" % item['name']
                yield Request(next_url, meta={'name':item['name']}, callback = self.parsePhoneNumByBaidu)
            else:
                item['phonenum'] = ''
                yield item


    def parsePhoneNumByBaidu(self, response):
        sel         =  Selector(response)
        hreflst     =  sel.xpath('//h3[@class="t"]/a/@href').extract()
        for h in xrange(len(hreflst)):
            if h>=3:break
            yield Request(hreflst[h], meta={'item':response.meta['item']}, callback = self.parsePhoneNum)
            #print hreflst[h]

    def parsePhoneNum(self, response):
        #print response.meta['name']
        item        =  response.meta['item']
        sel         =  Selector(response)
        #text1       =  response.body.replace(' ','')
        text        =  response.body.replace(' ','-').replace('+','-').replace(')','-')
        '''
        g1          =  re.search('联系',   text1)
        g2          =  re.search('手机',   text1)
        g3          =  re.search('phone',  text1)
        g4          =  re.search('号码',   text1)
        g5          =  re.search('电话',   text1)
        if not g1 and not g2 and not g3 and not g4 and not g5:return
        '''
        g           =  re.search("(86|17951)?(13[0-9]|15[0-9]|17[0678]|18[0-9]|14[57])[0-9]{8}", text)
        
        item['website'] = response.url
        '''debug
        if not g:
            with open('phone.txt','a+') as f:
                f.write("url:%s\n" % response.url)
        '''

        sign1 = sign2 = sign3 = False

        if g:
            item['mobilephone'] = g.group()
            sign1               = True
        else:
            item['mobilephone'] = ''

        g           =  re.search("(((\d{4}|\d{3})-(\d{7,8})|(\d{4}|\d{3})-(\d{7,8})-(\d{4}|\d{3}|\d{2}|\d{1})))", text)
        
        if g:
            item['phone']       = g.group()
            sign2               = True
        else:
            #g = re.search('\d{7,8}', text)
            #if not g:
            item['phone']   = ''
            #else:
            #    sign2           = True
            #    item['phone']   = g.group()
        #g           = re.search("([a-z0-9]*[-_]?[a-z0-9]+)*@([a-z0-9]*[-_]?[a-z0-9]+)+[\.][a-z]{2,3}([\.][a-z]{2})?", text)
        
        '''
        if g:
            item['email']       = g.group()
            sign3               = True
        else:
            item['email']       = ''
        '''

        if sign1 or sign2:
            if item['name'] in self.legalButNotNum and self.legalButNotNum[item['name']] == -1:
                self.eraseNotExistName(item['name'])
            self.legalButNotNum[item['name']] = 1
            yield item
        else:
            if item['name'] not in self.legalButNotNum:
                self.addNotExistName(item['name'], item['projectname'])
                self.legalButNotNum[item['name']] = -1


    def eraseNotExistName(self, name):
        lines = [l for l in open("legalButNoTel.txt", "r") if l.find(name) == -1]
        fd = open("legalButNoTel.txt", "w")
        fd.writelines(lines)
        fd.close()

    def addNotExistName(self, name, projectname):
        with open("legalButNoTel.txt", "a+") as f:
            f.write('%s || %s\n' % (name, projectname))

    def nameIsLegal(self, name):
        legalLst = ['鞋', '箱', '包', '酒店用品', '服饰', '面料', '纺织', '服装', '成衣']
        for word in legalLst:
            if name.find(word) != -1:
                return True
        return False