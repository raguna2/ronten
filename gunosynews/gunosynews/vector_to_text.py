#-*- encoding: utf-8 -*-
import os
import MeCab
import re
import numpy,scipy
#from article import *
from gunosynews.stopwordlist import *
from sklearn.feature_extraction.text import TfidfVectorizer
import itertools
from gunosynews.make_new_windows import *

#summery
#新たに作られたウィンドウのtf-idf値を計算し、ベクトル化
#新たなウィンドウ同士を総当たりで類似度を計算
#sim_tanin_list =[{"0,1":"0.00","0,2":"0.032",...},{"1,0":"0.00","1,2":"0.032",...},{"2,0":"0.00","2,1":"0.032",...},...]のそれぞれの集合に対し、値（類似度）でソートをかけ、0.05を超えるものが２つ以上なら、マッチしたウィンドウの内容を表示

def printResult(num0,num1,url,title,str):
	print("%d番のウィンドウと%d番のウィンドウがマッチしました。"%(num0,num1))
	print("%sウィンドウのURL:%s" % (str,url) )
	print("%sウィンドウのタイトル:%s"% (str,title) )
	print("%sウィンドウのテキスト" % str)



def makeShareUrl(url):#,before_arg,share_num,url_share
	if re.search(r'forbes',url):
		before_arg = url.split('detail/')
		share_num = before_arg[0].split('/',maxsplit=1)
		url_share = before_arg[0]+share_num[0]
	else:
		before_arg = url.split('?')
		url_share = before_arg[0]

	return url_share

def searchArticleList(articleList,text_sentou):
	for i in range(len(articleList)):
		if re.search(r'%s' % text_sentou,str(articleList[i]["text"])):
			global moto_url
			global moto_title
			moto_url = articleList[i]["url"]
			moto_title = articleList[i]["title"]
	return moto_url,moto_title







	#新たに作られたウィンドウのtf-idf値を計算し、ベクトル化
def vectorToText(new_window_corpus,articleList):
	new_window_corpus_size = len(new_window_corpus)

	new_tfidf_vect = TfidfVectorizer(stop_words=stoplist)
	new_X_tfidf = new_tfidf_vect.fit_transform(new_window_corpus)
	new_array_X = new_X_tfidf.toarray()

	#新たなウィンドウ同士を総当たりで類似度を計算
	sim_all={}
	#number = window_separate_times -1

	for arg1,arg2 in itertools.permutations(range(len(new_array_X)),2):
		#print("%d 番目と%d番目の類似度=%f" % (arg1,arg2,cos_similarity(new_array_X[arg1],new_array_X[arg2])))
		sim_all["%d,%d" % (arg1,arg2)] = cos_similarity(new_array_X[arg1],new_array_X[arg2])


	#配列の中に、複数の辞書型配列が入っている。sim_tanin_list =[{"0,1":"0.00","0,2":"0.032",...},{"1,0":"0.00","1,2":"0.032",...},{"2,0":"0.00","2,1":"0.032",...},...]
	sim_tanin_list=[]
	for k in range(new_window_corpus_size):
		sim_tanin={}
		for i in range(new_window_corpus_size):
			if i is not k:
				sim_tanin["%d,%d" % (k,i)] = sim_all["%d,%d" % (k,i)]
		sim_tanin_list.append(sim_tanin)
	#print("=====================================================================================")
	#print(sim_tanin_list)


	#sim_tanin_list =[{"0,1":"0.00","0,2":"0.032",...},{"1,0":"0.00","1,2":"0.032",...},{"2,0":"0.00","2,1":"0.032",...},...]のそれぞれの集合に対し、値（類似度）でソートをかけ、0.05を超えるものが２つ以上なら、マッチしたウィンドウの内容を表示

	#
	for s in range(new_window_corpus_size):
		_asc_sim_tanin =sorted(sim_tanin_list[s].items(),key=lambda x:x[1],reverse=True)
		cos_filter = 0.12 #類似度がいくつ以上なら良いか？
		match_filter = 10 #何個以上高い類似度のものがあれば良いか？
		match_count = 0
		match_key = []
		count = 0
		for j in range(new_window_corpus_size-1):
			#print("=====================================================================================")
			#print(float(_asc_sim_tanin[j][1]))
			if float(_asc_sim_tanin[j][1]) > cos_filter:
				#print("表示＝%f" % float(_asc_sim_tanin[j][1]) )
				match_key.append(_asc_sim_tanin[j][0])
				match_count += 1
		#print("=====================================================================================")
		#print("match_countは%dです" % match_count)

		if match_count > match_filter:
			print("=====================================================================================")
			print("match_countは%dです" % match_count)
			for key in match_key:
				num = key.split(",")
				print("マッチしたキー：%s" % key )
				if count is 0:
					text_sentou_moto = text_okiba[int(num[0])][:25]
					moto_url,moto_title = searchArticleList(articleList,text_sentou_moto)
					count =+1
					moto_url_share = makeShareUrl(moto_url)
					printResult(int(num[0]),int(num[1]),moto_url,moto_title,"参照元")
					print(text_okiba[int(num[0])])

				text_sentou_match = text_okiba[int(num[1])][:25]
				match_url,match_title = searchArticleList(articleList,text_sentou_match)
				match_url_share = makeShareUrl(match_url)

				if moto_url_share is not match_url_share:
					pass
					print("------------------------------------------------------------------------------------------------")
					printResult(int(num[0]),int(num[1]),match_url,match_title,"マッチした")
					print(text_okiba[int(num[1])])
				else:
					#print("同じ記事なのでエスケープされました。")
					pass


"""


	for j in range(5):
		kireme.append(_asc[j][0])#一番低い類似度を持つキー番号　＝＞６番目と７番目のテキストで区切る
	_asc_kireme = sorted(map(lambda x:int(x),kireme))

window_separate_times-1個のウィンドウ数

			print("マッチしたキー：%s" % key )
			
		print("-------------------------------------------------")



"""
