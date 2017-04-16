# -*- coding: utf-8 -*-
import scrapy
from gunosynews.items import PageItem
import logging
from scrapy.http import Request
import os
import re
from scrapy.loader.processors import Join, MapCompose, TakeFirst
from scrapy.loader import ItemLoader
from gunosynews.honbuns_make import *
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher

#gunosy.pyでスクレイピング
#→honbunList_make.pyで記事のリストを作成
#→windows_make.pyですべての記事をウィンドウに分ける
#→make_new_windows.pyで特徴語抽出、ベクトル化、コサイン類似度を出す
#vector_to_textでベクトル同士を比較→類似度が高いものをみつけてテキストにして返す
"""
タスク
・集める記事を増やしたら、フィルターの精度を上げる
・エスケープされていない原因


"""
class RontenSpider(scrapy.Spider):
	name = "ronten"
	allowed_domains = ["forbesjapan.com",'wedge.ismedia.jp','gendai.ismedia.jp','jp.reuters.com']
	query ="安倍"#input()#os.environ["SCRAPY_KEYWORD"]中国・アメリカ・原発
	articleList =[]
	honbunList =[]
	forbs_count = 0
	gendai_count = 0
	wedge_count = 0
	article_count =0
	parse_wedge_count = 0
	parse_forbes_count = 0
	parse_gendai_count = 0
	start_urls = (
		'http://forbesjapan.com/articles/search/%s' % query,
		'http://gendai.ismedia.jp/search?fulltext=%s' % query,
		'http://wedge.ismedia.jp/search?fulltext=%s' % query,
		)
	def __init__(self):
		dispatcher.connect(self.spider_closed, signals.spider_closed)

	#サーチ結果から記事のURL取得
	def parse(self, response):
		if re.search(r'http://forbesjapan',response.url):
			#(フォーブス) => response.xpath('//div[@class="kizi-honbun"]/text()').re(r'\W+([\w\S]+)')
			nukitori = '//ul[@class="edittools-stream"]/li/a[1]/@href'
			mekuri ='//li[@class="pagination-next"]//@href'
		elif re.search(r'http://gendai',response.url):
			#現代
			nukitori = '//div[@class="elementArticleItem styleText-dark"]/a/@href'
			mekuri = '//div[@class="pagination"]//@href'
			#http://gendai.ismedia.jp以下だけ抜かれる
		elif re.search(r'http://wedge',response.url):
			#ウェッジ
			nukitori = '//div[@class="content-info"]//@href'
			mekuri ='//div[@class="pagination"]//@href'
		else:
			logging.warning("以外")
		
		for article_url in response.xpath(nukitori).extract():
			#もしURLが(/articles/-/)なら生成
			if re.search(r'/articles/-/',article_url):
				if re.search(r'wedge',article_url):
					before_url = article_url
				else:
					before_url = 'http://gendai.ismedia.jp' + article_url
			else:
				before_url = article_url
			url = response.urljoin(before_url)
			yield scrapy.Request(url=url, callback=self.text_parse)
			self.article_count +=1
		"""
		if re.search(r'wedge',response.url):
			next_list_url = response.xpath(mekuri).extract()
			for next_wedge in next_list_url:
				url_x = response.urljoin(next_wedge)
				yield scrapy.Request(url=url_x, callback=self.parse)
				self.parse_wedge_count +=1
		elif re.search(r'http://gendai',response.url):
			before_next_list_url = response.xpath(mekuri).extract()
			for next_gendai in before_next_list_url:
				self.parse_gendai_count +=1
				next_list_url ="http://gendai.ismedia.jp"+next_gendai
				url_y = response.urljoin(next_list_url)
				yield scrapy.Request(url=url_y, callback=self.parse)
		else:
			for next_list_url in response.xpath(mekuri).extract():
				self.parse_forbes_count +=1
				url_z = response.urljoin(next_list_url)
				yield scrapy.Request(url=url_z, callback=self.parse)
		"""
		

#ここまでparse



	#記事のタイトルと本文を取得
	def text_parse(self, response):
		if re.search(r'http://forbesjapan',response.url):
		#URLの一部にマッチしてたらTRUE
			#フォーブス
			self.forbs_count += 1
			kiritori = '//div[@class="main-article-padding"]'
			title_cut ='//h1/text()'
			text_cut ='//div[@class="kizi-honbun"]//text()'
			yomitori ='//*[@class="inner-title"]//@href'
		elif re.search(r'http://gendai',response.url):
			#現代
			self.gendai_count += 1
			kiritori = '//*[@class="blockContainer_left2"]'
			title_cut ='//title//text()'
			text_cut ='//div[@class="articleContents"]//p/text()'
			yomitori ='//div[@class="pagination"]//@href'
		elif re.search(r'http://wedge',response.url):
			#ウェッジ
			self.wedge_count += 1
			kiritori = '//*[@class="article-wrapper"]'
			title_cut ='//title//text()'
			text_cut ='//div[@class="article-body"]//p/text()'
			yomitori ='//div[@class="pagination"]//@href'


		#記事のタイトルと本文を取得
		for quote in response.xpath(kiritori):
			article = PageItem()
			article['title'] = quote.xpath(title_cut).re(r'([^\u3000]+)')
			article['text'] = quote.xpath(text_cut).re(r'([\w\s\W]+)')
			article['url'] = response.url
			self.articleList.append(article)

		#setで重複をなくす
		url_uniq =[]
		if len(response.xpath(yomitori).extract()) is not 0:
			for x in response.xpath(yomitori).extract():
				if x not in url_uniq:
					url_uniq.append(x)

		#次のページのURL取得
		for next_page_url in url_uniq:
			#受け取ったのが現代のURLならURLを合成
			if re.search(r'/articles/-/',next_page_url):
				print()
				if re.search(r'wedge',next_page_url):
					next_page_url = next_page_url
				else:
					next_page_url = 'http://gendai.ismedia.jp' + next_page_url
			else:
				next_page_url = next_page_url
			yield scrapy.Request(url=next_page_url,callback=self.text_parse)

		total_count = self.forbs_count+self.gendai_count+self.wedge_count
		print("%d個目の記事を取得しました。" % total_count)
	#ここまでtext_parse

	#スパイダーがスクレイピングを終了したら起動
	def spider_closed(self, spider):
		print(self.article_count)
		print(self.parse_forbes_count)
		print(self.parse_gendai_count)
		print(self.parse_wedge_count)
		make_honbunList(self.articleList)




"""
ItemLoaderでよくわかんなかったとこ
		il = ArticleLoader(item=GunosynewsItem(),response=response)
		il.add_xpath('title',title_cut)
		il.add_xpath('text',text_cut,re=r'([\w\S]+)')
		il.load_item()

			
			title,url,textがまとまったハッシュのリストを見たい時
			for i in range(len(self.articleList)):
				print(self.articleList[i])
			

"""





