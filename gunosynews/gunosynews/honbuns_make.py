# -*- coding: utf-8 -*-
import re
from gunosynews.windows_make import *
from gunosynews.make_new_windows import *
from gunosynews.vector_to_text import *

"""
複数ページある記事の本文をひとつにまとめて、記事ごとにhonbunListのなかに入れる
articleList =[{"title":"c","text":["センテンス","1-3。"],"url":"http://gendai/001?page=3"},{"title":"b","text":["センテンス","1-2。"],"url":"http://gendai/001?page=2"},{"title":"C","text":["センテンス","2-3。"],"url":"http://gendai/002?page=3"},{"title":"a","text":["センテンス","1-1。"],"url":"http://gendai/001"},{"title":"B","text":["センテンス","2-2。"],"url":"http://gendai/002?page=2"},{"title":"A","text":["センテンス","2-1。"],"url":"http://gendai/002"}]

＝＞

honbunList =["センテンス1-1。センテンス1-2。センテンス1-3。","センテンス2-1。センテンス2-2。",]

#

"""
#articleList =[{"title":"c","text":["センテンス","1-3。"],"url":"http://gendai/001?page=3"},{"title":"b","text":["センテンス","1-2。"],"url":"http://gendai/001?page=2"},{"title":"C","text":["センテンス","2-3。"],"url":"http://gendai/002?page=3"},{"title":"a","text":["センテンス","1-1。"],"url":"http://gendai/001"},{"title":"B","text":["センテンス","2-2。"],"url":"http://gendai/002?page=2"},{"title":"A","text":["センテンス","2-1。"],"url":"http://gendai/002"}]

#articleListが渡される
def make_honbunList(articleList_):
	print("=====================================================================================")
	print("ウィンドウを解析中です...")
	articleList = articleList_
	pickupList=[]
	articleInfoList={}

	#まとめる記事の共通URL部分のリスト（重複なし）を生成
	for i in range(len(articleList)):
		#現代は?で区切られて最初のページ以外はページ番号がつくので
		pickUrl = makeShareUrl(articleList[i]["url"])
		
		if re.search(r'forbesjapan.com',articleList[i]["url"]):
			temp_x = articleList[i]["url"].split('detail/')
			temp_y = temp_x[1].split('/',maxsplit=1)
			pickUrl = temp_x[0] + temp_y[0]
		else:
			before_pickUrl = articleList[i]["url"].split('?')
			pickUrl = before_pickUrl[0]
		
		if pickUrl not in pickupList:
			pickupList.append(pickUrl)

	
	#articleInfoListに記事番号URLをキーにしてarticleListの中身を記事ごとにまとめる
	for l in range(len(pickupList)):
		for k in range(len(articleList)):
			if re.search(r'forbesjapan.com',articleList[k]["url"]):
				temp_a = articleList[k]["url"].split('detail/')
				temp_b = temp_a[1].split('/',maxsplit=1)
				target_url = temp_a[0] + temp_b[0]#http://...detail/12434
			else:
				before_target_url = articleList[k]["url"].split('?')
				target_url = before_target_url[0]#http://...12432
			
			if pickupList[l] == target_url:
				if re.search(r'forbesjapan.com',target_url):
					if len(temp_b) is 1:
						articleList[k]["url"] = articleList[k]["url"]+'/1'
					else:
						temp_c = articleList[k]["url"][:-3]
						articleList[k]["url"] = temp_c
				else:
					if len(before_target_url) is 1:
						#現代で一つしかbefore_target_urlの配列になかったら
						articleList[k]["url"] = articleList[k]["url"]+'?page=1'

				key ="%s" % pickupList[l]
				if key not in articleInfoList.keys():
				#初めての記事なら記事の共通URLをキーにした配列をつくる
					articleInfoList[key] = []
					articleInfoList[key].append(articleList[k])
				else:
					articleInfoList[key].append(articleList[k])

	#articleInfoListに入っている配列を、ページ番号でソート
	sorted_list=[]
	for g in articleInfoList.keys():
		_asc = sorted(articleInfoList[g], key=lambda x: x['url'])
		sorted_list.append(_asc)
	
	#記事ごとにテキストをつないでhonbunListを生成
	honbunList=[]
	for i in range(len(sorted_list)):#i=記事集団がある配列番号
		honbun_all=[]
		for k in range(len(sorted_list[i])):#k=ページが置いてある配列番号
			honbun_page ="".join(sorted_list[i][k]["text"])
			honbun_all.append(honbun_page)
		honbun_text_all= "".join(honbun_all)
		honbunList.append(honbun_text_all)
#================================================================================
	#ウィンドウの集合（記事を２文ごとに区切ったもの）　の集合をつくる
	
	windowsList =[]
	for honbun in honbunList:
		one_windows = windows_make(honbun)#windows_makeでwindowがreturnされる
		windowsList.append(one_windows)
	#すべての記事に対して新たなウィンドウをつくる
	new_window_corpus=[]
	for article_honbun in windowsList:
		make_new_windows(article_honbun,new_window_corpus)
	vectorToText(new_window_corpus,articleList)
	






"""
window= ["センテンス1-1。センテンス1-2。","センテンス1-3。センテンス1-4。","センテンス1-5。センテンス1-6。"]
window= ["センテンス2-1。センテンス2-2。","センテンス2-3。センテンス2-4。"]
.
.
.

=>

windowsList = [["センテンス1-1。センテンス1-2。","センテンス1-3。センテンス1-4。","センテンス1-5。センテンス1-6。"],["センテンス2-1。センテンス2-2。","センテンス2-3。センテンス2-4。"]]

article_honbun[0] = ["センテンス1-1。センテンス1-2。","センテンス1-3。センテンス1-4。","センテンス1-5。センテンス1-6。"]

articleList_kari[0]＝["センテンス1-1。センテンス1-2。","センテンス1-3。センテンス1-4。","センテンス1-5。センテンス1-6。"]


	for i in range(len(articleList)):
		if re.search(r'http://forbesjapan',articleList[i]["url"]):
			pickUrl = articleList[i]["url"]
			if pickUrl not in pickupList:
				pickupList.append(pickUrl)
		else:
			pickUrl = articleList[i]["url"].split('?')
			if pickUrl[0] not in pickupList:
				pickupList.append(pickUrl[0])

"""

