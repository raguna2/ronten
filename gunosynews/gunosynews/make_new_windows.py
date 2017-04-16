#-*- encoding: utf-8 -*-
import os
import MeCab
import re
import numpy,scipy
#from article import *
from gunosynews.stopwordlist import *
from sklearn.feature_extraction.text import TfidfVectorizer
import itertools
#重要な変数
window_separate_times = 3#3 #いくつの新しいウィンドウにきりわけるか決める変数
text_okiba=[]

#article_honbun[kizi_size]=["article1の文章全て","article2の文章全て","article3の文章全て","article4の文章全て"]
def cos_similarity(v1,v2):
	cos_sim = numpy.dot(v1,v2) / (numpy.linalg.norm(v1) * numpy.linalg.norm(v2))
	return cos_sim

def textToWordSpace(article_honbun,corpus):
	for i in range(len(article_honbun)):#
		mecab =MeCab.Tagger("-Ochasen")
		mecab_result = mecab.parse(article_honbun[i])
		info_of_words =mecab_result.split("\n")
		words=[]
		for info in info_of_words:#私\tワタシ\t私\t名詞-代名詞-一般\n
			o = info.split("\t")
			if o[0] == 'EOS' or o[0] =='':
				break
			else:	
				if re.search(r'名詞',o[3]):
					words.append(o[0])
		words_space =" ".join(words)
		corpus.append(words_space)
		#指定したコーパスリストに、単語だけ抽出されスペースで区切られたウィンドウが追加される
		#ここまでtextToWordSpace


#ここからfor文で記事ごとに新たなウィンドウ生成
def make_new_windows(article_honbun,new_window_corpus):
	new_window_wordspace=[]
	window_corpus=[]
	textToWordSpace(article_honbun,window_corpus)#article_honbun[kizi_size]
	tfidf_vect = TfidfVectorizer(stop_words=stoplist)
	X_tfidf = tfidf_vect.fit_transform(window_corpus)
	array_X = X_tfidf.toarray()

	#ある記事の本文の、前後のウィンドウ同士の類似度を計算
	sim_zengo = {}
	for i in range(1,len(array_X)+1):
		if i is not len(array_X):
			#print("%d 番目のウィンドウと%d番目のウィンドウのコサイン類似度=%f" % (i,i+1,cos_similarity(array_X[i-1],array_X[i])))
			sim_zengo["%d" % i] = cos_similarity(array_X[i-1],array_X[i])
	#print(sim_zengo)

	#類似度をソートして新たなウィンドウを作るための切れ目を見つける
	_asc = sorted(sim_zengo.items(),key=lambda x:x[1])
	kireme=[]
	for j in range(window_separate_times):
		kireme.append(_asc[j][0])#一番低い類似度を持つキー番号　＝＞６番目と７番目のテキストで区切る
	_asc_kireme = sorted(map(lambda x:int(x),kireme))

	#見つけた切れ目に従い、新たなウィンドウを生成
	#len(article_honbun)は元のウィンドウの数
	new_window=[]
	before_key =1
	count = 0
	for g in _asc_kireme:
		#最初の切れ目以外のときはbefore_keyをセット
		if g is not _asc_kireme[0]:
			before_key =int(_asc_kireme[count])
			count += 1

		#最後のウィンドウを作るとき
		if g is _asc_kireme[-1]:
			temp =[]
			for i in range(int(g)-1,len(article_honbun)):
				temp.append(article_honbun[i])
			new_window_text="".join(temp)
			new_window.append(new_window_text)
			break

		if g is 1:#一番最初のウィンドウだったら
			new_window.append(article_honbun[0])
		elif g is len(article_honbun):#一番最後のウィンドウだったら
			new_window.append(article_honbun[-1])
		else:
			temp =[]
			for i in range(before_key,g):
				temp.append(article_honbun[i])#
			new_window_text="".join(temp)
			new_window.append(new_window_text)

	#新たに作られたウィンドウから単語だけ抽出し、スペースで区切ったものをnew_window_wordspaceに入れる
	for final_window in new_window:
		text_okiba.append(final_window)
	textToWordSpace(new_window,new_window_wordspace)
	#ここまでfor文で記事ごとに新たなウィンドウ生成
	#new_window_corpus=[]
	for i in range(len(new_window_wordspace)):
		new_window_corpus.append(new_window_wordspace[i])


	#print(new_window_corpus)
#ここまでmake_new_windows
	
#==================================================================================
"""
for z in range(len(new_window_corpus)):
	print("-------------------------------")
	print(new_window_corpus[z])

	_asc = sorted(sim_zengo.items(),key=lambda x:x[1])
	kireme=[]





"""

"""
_asc=[('4', 0.062867152368739479), ('3', 0.10298298604778208),
('1', 0.17822393487047242), ('0', 0.1915686630372446), ('2', 0.19273521515796033)]
"""

"""
#1 => 1番目のウィンドウを表示 => article_honbun[kizi_size][kizi_size][0]
#3 => 2〜3番目のウィンドウをつなげて表示 => article_honbun[kizi_size][kizi_size][前のキー番号(1)]〜article_honbun[kizi_size][kizi_size][キー番号-1(2)]
#8 => 4〜8番目のウィンドウをつなげて表示 => article_honbun[kizi_size][kizi_size][前のキー番号(3)]〜article_honbun[kizi_size][kizi_size][キー番号-1(7)]
#10 =>　9〜10番目のウィンドウをつなげて表示 => article_honbun[kizi_size][kizi_size][前のキー番号(8)]〜article_honbun[kizi_size][kizi_size][キー番号-1(9)]
#last => 11〜12番目のウィンドウをつなげて表示 => article_honbun[kizi_size][kizi_size][前のキー番号(10)]〜article_honbun[kizi_size][kizi_size][-1]
"""
#article_honbun[0][0] ='日本の「新幹線ビジネス」関係者は今、来年1月20日に誕生するトランプ米政権に熱い眼差しを向けている。ドナルド・トランプ次期大統領は大統領選期間中、大統領に就任すれば道路、鉄道、港湾施設など国内のインフラ整備に1兆ドル（約110兆円）投じて雇用を生み出すと、繰り返し言明してきた。そのインフラ整備の中に新幹線建設構想が含まれているのだ。'

#article_honbun[0] = ['日本の「新幹線ビジネス」関係者は今、来年1月20日に誕生するトランプ米政権に熱い眼差しを向けている。ドナルド・トランプ次期大統領は大統領選期間中、大統領に就任すれば道路、鉄道、港湾施設など国内のインフラ整備に1兆ドル（約110兆円）投じて雇用を生み出すと、繰り返し言明してきた。そのインフラ整備の中に新幹線建設構想が含まれているのだ。', '日本のメディアは全く報道しなかったが、奇しくも大統領選本選の11月8日、米紙ニューヨーク・タイムズは、メリーランド州運輸局がニューヨーク～ワシントン間約370㎞のマグレブ（リニア新幹線）建設のための調査費2億8000万ドル（約30億円）を計上したと報じた。総事業費約200億ドル（約2兆4000億円）のテキサス州ダラス～ヒューストン間約400㎞の高速鉄道（テキサス新幹線）建設は既にFS（事業調査）を終えて、来年夏には着工する。JR東海、日立製作所、三井物産などがコンソーシアムを組み、事業主体はJR東海の葛西敬之名誉会長の肝いりで設立された米日高速鉄道社（USJHSR）である。', '同社の社長は、次期駐日大使候補として名前が上がっているリチャード・ローレス元国防副次官である。トランプ政権誕生のタイミングに合わせたわけではないが、実はサンフランシスコ～ロサンゼルス郊外のアナハイム間約837㎞の高速鉄道計画も復活しているのだ。総事業費が676億ドル（約8兆1100億円）という巨額であること、そして距離が長すぎるということで一度は頓挫した経緯がある。', '2015年4月、オバマ大統領との首脳会談を終えた安倍晋三首相は首都ワシントンからサンフランシスコに立ち寄り、ブラウン・カリフォルニア州知事と会談、自ら新幹線セールスを行っている。こちらはJR東日本、川崎重工などがコンソーシアムを組んでいる。テキサス、カリフォルニア両州の高速鉄道計画に日本の新幹線の主力車両を改造した「N700-1Bullet」を売り込む。', '新幹線工場を現地に建設して雇用促進を図ることでトランプ次期大統領の期待に応えるのだ。今秋、国内の主要金融機関・建設会社のトップは米国西海岸を視察したが、サンフランシスコ郊外に建設中の巨大駐車場は将来、高速鉄道が敷設された暁には鉄道ターミナルに転用するとの説明を受けたという。新幹線のトップセールスは何も米国だけではない。', '安倍首相は11月11日、来日したインドのモディ首相と会談した。インドの高速鉄道計画（同国最大都市ムンバイ～グジャラート州アーメダバード間約500㎞）に日本の新幹線方式を採用することで合意した。と同時に、2018年着工、23年開業を正式決定した。', '次は、マレーシアである。来日したナジブ首相は同16日に安倍首相と会談し、10年後の26年に開業予定の首都クアラルンプール～シンガポール間約350㎞の高速鉄道計画入札に日本が参加するよう正式に申し入れた。同計画には、アジアインフラ投資銀行（AIIB）融資を前面に押し出す中国や韓国も自国技術の採用を働きかけている。', 'しかし、タッグを組むJR東日本、三菱重工、住友商事連合がほぼ間違いなく受注できるという。総事業費約110億ドル（約1兆3000億円）。5月21日に開かれた第21回国際交流会議「アジアの未来」（日本経済新聞社と日本経済研究センター共催）で、安倍首相は今後5年間でアジア開発銀行（ADB）と連携してアジアのインフラ整備に約1100億ドル（約13兆円）を投じると言明した。', 'いま日本は、「トランプ現象」の恩恵で空前の円安・株高を享受している。年末には東京株式市場の日経平均株価が1万9000円台、為替の対ドル円レートは115～117円を窺うとの見方が証券業界で支配的である。だが、安心できる状況ではない。', '12月4日のイタリアの国民投票はレンツィ政権の事実上の信任投票である。仮にレンツィ首相退陣となると、イタリア発の“EU離脱ショック”のドミノが来年夏までにオーストリア、オランダ、フランスに波及する心配がある。そのような事態は、円高リスクの再来となって日本経済を直撃する。']


"""
["センテンス1-1。センテンス1-2。(article_honbun[kizi_size][kizi_size])","センテンス1-3。センテンス1-4。","センテンス1-5。センテンス1-6。"]

=>

[センテンス　1 - 1 。 センテンス 1 - 2 ........](corpus[0])
.
.
.

=>

[ 0.34633852  0.39972684  0.46287182  0.46287182  .......0.54015502 0.39972684]
.
.
.

=>

前後のウィンドウ同士で類似度を比較

"""