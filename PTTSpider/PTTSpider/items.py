
import scrapy


class PttbeautyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    author_name = scrapy.Field()
    article_title = scrapy.Field()
    comments = scrapy.Field()
    pic_urls = scrapy.Field()
