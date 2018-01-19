from scrapy import Request
from scrapy.spiders import Spider
from example.items import CFDAItem
import re
import copy
import os

site_urls = []

class CFDASpider(Spider):
    name = 'cfda'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',}

    def start_requests(self):
        url = 'http://www.sfda.gov.cn/WS01/CL1842/'
        yield Request(url,headers = self.headers)


    def parse(self, response):
        item = CFDAItem()
        trs = response.xpath("//tr/td[@class = 'ListColumnClass15']/..")

        for tr in trs:
            item = CFDAItem()
            temp_url = tr.xpath(
                './/td[@class="ListColumnClass15"]/a/@href').extract()[0]
            news_url = temp_url.replace('..','http://www.sfda.gov.cn/WS01')
            item['news_url'] = news_url

            temp_date = tr.xpath(
                './/span[@class = "listtddate15"]/text()').extract()[0]
            item['news_date'] = re.findall(r'[0-9]{4}-[0-9]{2}-[0-9]{2}',temp_date)[0]

            temp_title = tr.xpath(
                './/font/text()').extract()
            item['news_title'] = ''.join(temp_title)

            item['site_url'] = response.url

            yield Request(news_url,headers=self.headers,meta={'key':item},callback=self.parse_content)

        # extract next page link
        # global site_urls
        next_url = response.xpath("//td[@class = 'pageTdE15']/a/@href").extract()[0]
        url = response.urljoin(next_url)
        if url not in site_urls:
            site_urls.append(url)
            yield Request(url,headers = self.headers)

    def parse_content(self,response):

        ##write the html out
        html_obj = response.xpath("//body/table").extract()

        #head
        head_str = html_obj[0].replace('..','http://www.sfda.gov.cn/WS01')

        #content
        html_str = html_obj[1].replace('..','http://www.sfda.gov.cn/WS01')
        html_str = html_str.replace('"/directory','"http://www.sfda.gov.cn/directory')

        WriteSNS = response.xpath("//script[contains(.,'WriteSNS')]").extract()[0]
        html_str = html_str.replace(WriteSNS,'')
        html_str = html_str.replace('&amp;nbsp',' ')

        #if multi-pages?
        if response.xpath("//a[text()=1]"):
            page_url = response.xpath("//a[text()=1]/@href").extract()[0]
            page_url_d = page_url.split('.')[0]

            parentUrl = re.sub(r'[0-9]+\.html','',response.url)

            html_str = html_str.replace(page_url_d, parentUrl + page_url_d)

        #css
        css_str = response.xpath("//head").extract()[0]
        css_str = css_str.replace('..','http://www.sfda.gov.cn/WS01')

        #write
        file_content = u'<html>' + head_str + u'<body>'+ css_str + html_str + u'</body> </html>'
        file_name = re.findall(r'CL.*html',response.url)[0].replace('/','_')
        file_path = os.getcwd() + '\\CFDA'


        if not os.path.exists(file_path):
            os.makedirs(file_path)
        file_path_name = file_path + '\\' + file_name

        f = open(file_path_name,'w')
        f.write(file_content.encode('utf-8'))
        f.close()

        item = response.meta['key']
        temp = len(response.xpath("//td").extract())
        item['content_len'] = temp
        item['html_file_url'] = file_path_name

        yield item
