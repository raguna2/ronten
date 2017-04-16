# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.contrib.loader.processor import TakeFirst,Join,MapCompose
from scrapy.loader import ItemLoader



class PageItem(scrapy.Item):
    text = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()

"""
class ArticleLoader(ItemLoader):
	default_output_processor = TakeFirst()
	title_in = MapCompose()
	title_out = Join()

	text_in = MapCompose()
	text_out = MapCompose()
"""