import scrapy
from PTTSpider.items import PttbeautyItem
from PTTSpider.FileSaver import FileSaver
import time

class PttscrperSpider(scrapy.Spider):
    name = 'PTTScraper'
    allowed_domains = ['www.ptt.cc']
    start_urls = ['https://www.ptt.cc/bbs/Beauty/']
    def __init__(self):
        self.Saver = None
        if not self.Saver: #singleton initialize
            self.Saver = FileSaver()
    def get_content(self, response):

        img_url_list = response.xpath("//div[@class='bbs-screen bbs-content']/a/@href").getall() #圖檔的url
        meta = response.css("span.article-meta-value").getall() #抓標題區
        author = meta[0][33:-7] #把抓到的tag去掉 只留文字
        title = meta[2][33:-7] #把抓到的tag去掉 只留文字

        comments_authors = response.xpath("//span[@class = 'f3 hl push-userid']/text()").getall() #推文者
        comments_text = response.xpath("//span[@class = 'f3 push-content']/text()").getall() #推文內容
        comments = list(zip(comments_authors, comments_text))
        #把推文跟推文者合起來


        cur_item = PttbeautyItem() #做成scrapty item

        cur_item["author_name"] = author
        cur_item["article_title"] = title
        cur_item["comments"] = comments
        cur_item["pic_urls"] = img_url_list


        """本來應該要分開來的 但現在是用yield 只好把兩個函式寫在一起"""
        self.save_item(cur_item)

    def save_item(self, item):
        #存抓到的item
        self.Saver.set_item(item)
        self.Saver.save_comments_to_file()
        self.Saver.save_imgs()

    def parse(self, response, front_url = 'https://www.ptt.cc', article_number = 10):

        for i in range(article_number):
            index_page_url = f'https://www.ptt.cc/bbs/Beauty/index{4004-i}.html' #往前抓幾頁
            yield scrapy.Request(index_page_url, cookies={'over18': '1'}) #給ptt 18禁回應
            article_url_list = response.xpath("//div[@class='title']/a/@href").getall()
            #print(article_url_list)
            time.sleep(3) #睡眠以免被抓

            for idx in range(len(article_url_list)):

                cur_article_url = front_url+article_url_list[idx]

                yield scrapy.Request(cur_article_url, self.get_content)

