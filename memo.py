#タスク



#ただの文章を3つ用意
#句点で区切ってウィンドウごとに配列に入れる
#配列に入った文章をmecabで形態素解析
#ウィンドウごとに特徴語のベクトルのTF-IDFベクトルを作成する
#["今朝","早く","起きた"]=>[0.0443,0.5433.0....]（この時ウィンドウ内の単語ごとにTF-IDF）
#前後のウィンドウ同士でTF-IDFベクトルを比較（類似度を出す、この時IDが必要）
#類似度をソート＝＞低いものを見つける（idで）
#idの場所で新たなウィンドウを生成　＝＞配列に入れる
#ウィンドウごとに特徴語のベクトルのTF-IDFベクトルを作成する
#["今朝","早く","起きた"]=>[0.0443,0.5433.0....]（この時ウィンドウ内の単語ごとにTF-IDF）
#全てのウィンドウ同士でTF-IDFベクトルを比較（類似度を出す、この時IDが必要）
#一つのnewウィンドウごとに類似度をソートできるようにする
#類似度をソート＝＞高いものを見つける（idで）
#類似度がx以上のものが、y個見つかったら該当の記事を取って来る

#同じ記事だったら除外する
#表示











"""
#!/usr/bin/ruby

testdata = [{"title"=>"c", "text"=>["センテンス", "1-3。"], "url"=>"http://gendai/001?page=3"},
{"title"=>"b", "text"=>["センテンス", "1-2。"], "url"=>"http://gendai/001?page=2"},
{"title"=>"C", "text"=>["センテンス", "2-3。"], "url"=>"http://gendai/002?page=3"},
{"title"=>"a", "text"=>["センテンス", "1-1。"], "url"=>"http://gendai/001"},
{"title"=>"B", "text"=>["センテンス", "2-2。"], "url"=>"http://gendai/002?page=2"},
{"title"=>"A", "text"=>["センテンス", "2-1。"], "url"=>"http://gendai/002"}]

keys = {}

testdata.each { |x|
  (key, page) = x["url"].split("?")
  if (page == nil) then
    x["url"] = "#{key}?page=1" 
  end
  keys[key] = []
}

testdata.each { |x|
  key = x["url"].split("?")[0]
  keys[key].push({"text"=>x["text"], "url"=>x["url"]})
}

keys.each { |key,value|
  p value
}


"""
#トークン＝＞最小単位(彼、私　etc)、パース＝＞構文解析、ノード＝＞節（I know/that he is honest）


#match.pyより
"""
for i in range(len(array)):
  match1 = re.search(r'(^.{7})',array[i]["title"])
  #print(match1.group())
  for k in range(len(array)):
    if k is not i:#{i=0,k=2,4} =>まっち
      match2 = re.search(r'(^.{7})',array[k]["title"])
      if match2.group() == match1.group():#k番目とtitleマッチ
        #array[i]["text"]+array[k][text]
        before_honbun =''.join(array[i]["text"]+array[k]["text"])
        #articleInfoList.append(before_honbun)
        print("最初")
        print(before_honbun)
        #before_honbun =''.join()
        #articleInfoList.append(before_honbun)
        #print("次")
        #print(articleInfoList)

kousei1 =[]
  for add_times in range(window_size):#0-2
    kousei1.append(window_all[k+add_times])
  window_text =''.join(kousei1)
  window.append(window_text)


import re

array=[{"title":"aaaaaaa","text":"dafdafdsafa","url":"adaf.com"},{"title":"aaaaaai","text":"dafdafdsafa","url":"adaf.com"},{"title":"aaaaaaa","text":"dafdafdsafa","url":"adaf.com"},{"title":"aadaaaa","text":"dafdafdsafa","url":"adaf.com"},{"title":"aadaaaa","text":"dafdafdsafa","url":"adaf.com"},{"title":"aaaaaaa","text":"dafdafdsafa","url":"adaf.com"},{"title":"aadaaaad","text":"dafdafdsafa","url":"adaf.com"}]
dict1 =array[1]
match1= re.search(r'([\w\s]{3})',dict1["title"])
print match1.group()



for i in range(len(array)):
  match1 =re.search(r'([\w{7}]+)',array[i]["title"])
  #0 ->array[0]["text"]
  for k in range(i+1,len(array)):
    match2 =re.search(r'([\w{3}]+)',array[k]["title"])
  print "match="+str(i)+"and"+str(k)
"""
"""
i=0 =>range(1,4),k=1=>p1 k=2=>p2 k=3=>p3
i=1 =>range(2,4),k=2=>p2 k=3=>p3
i=0 =>k=123
i=1 =>k=23
if re.search(r'([\w{7}]+)',array[i]["title"])

  def if_articleNum_match(self):
    if self.match_box[0].group(2) == self.match_box[1].group(2):
      okiba =[]
      okiba.append(self.match_box[0].group(3))
      okiba.append(self.match_box[1].group(3))
      if self.match_box[0].group(2) == self.match_box[2].group(2):
        okiba.append(self.match_box[2].group(3))
        print("置き場")
        print(okiba)
        self.save_for_connect(okiba)
      else:
        self.save_for_connect(okiba)

  before_honbun =["","","","",""]
  honbun =[]
  match_box=[]
  pattern = r'([\w\W\s\S]+)articles/[-/]{0,2}[detail/]{0,7}([\w\W\s\S]{5})[?]?([\w\W\s\S]+)?'
  
  for x in range(len(array)):
    match_box.append(re.search(pattern,array[x]["url"]))

  #print("match_box[0].group(2)="+match_box[0].group(2))#1 =>元ネタ　2=>記事番号　3=>ページ
  #print("match_box[1].group(2)="+match_box[1].group(2))
  #print("match_box[2].group(2)="+match_box[2].group(2))
  #print(str(match_box[0].group(1)))
  def main(self):
  #urlが現代の時
    if self.match_box[0].group(1) == "http://gendai.ismedia.jp/":
      self.if_articleNum_match()
  #urlがフォーブスの時
    elif self.match_box[0].group(1) == 'http://forbesjapan.com/articles/':
      print("hello")


  def if_articleNum_match(self):
    if self.match_box[0].group(2) == self.match_box[1].group(2):
      okiba =[]
      okiba.append(self.match_box[0])
      okiba.append(self.match_box[1])
      if self.match_box[0].group(2) == self.match_box[2].group(2):
        okiba.append(self.match_box[2])
        print("置き場")
        print(okiba)
        self.save_for_connect(okiba)
      else:
        self.save_for_connect(okiba)
#0-1,0-2,0-3
#1-2,1-3
#2-3

  def save_for_connect(self,okiba):
    for i in range(len(okiba)):
      if okiba[i].group(3) == "page=2":
        self.before_honbun[1] =''.join(self.array[1]["text"])#1
      elif okiba[i].group(3) == "page=3":
        self.before_honbun[2] =''.join(self.array[0]["text"])#0
      elif okiba[i].group(3) == "page=4":
        self.before_honbun[3] =''.join(None)
      elif okiba[i].group(3) == "page=5":
        self.before_honbun[4] =''.join(None)
      elif okiba[i].group(3) is None:
        self.before_honbun[0] =''.join(self.array[2]["text"])#2
      else:
        print("else")
    print("ビフォー本文")
    print(self.before_honbun)
    print("本文")
    self.honbun = ''.join(self.before_honbun)
    print(self.honbun)

l = MatomeClass()
l.main()

  before_honbun =["","","","",""]
  honbun =[]
  match_box=[]
  pattern = r'([\w\W\s\S]+)articles/[-/]{0,2}[detail/]{0,7}([\w\W\s\S]{5})[?]?([\w\W\s\S]+)?'
  
  for x in range(len(array)):
    match_box.append(re.search(pattern,array[x]["url"]))

  #print("match_box[0].group(2)="+match_box[0].group(2))#1 =>元ネタ　2=>記事番号　3=>ページ
  #print("match_box[1].group(2)="+match_box[1].group(2))
  #print("match_box[2].group(2)="+match_box[2].group(2))
  #print(str(match_box[0].group(1)))
  def main(self):
  #urlが現代の時
    if self.match_box[0].group(1) == "http://gendai.ismedia.jp/":
      self.if_articleNum_match()
  #urlがフォーブスの時
    elif self.match_box[0].group(1) == 'http://forbesjapan.com/articles/':
      print("hello")


  def if_articleNum_match(self):
    if self.match_box[0].group(2) == self.match_box[1].group(2):
      okiba =[]
      okiba.append(self.match_box[0])
      okiba.append(self.match_box[1])
      if self.match_box[0].group(2) == self.match_box[2].group(2):
        okiba.append(self.match_box[2])
        print("置き場")
        print(okiba)
        self.save_for_connect(okiba)
      else:
        self.save_for_connect(okiba)
#0-1,0-2,0-3
#1-2,1-3
#2-3

  def save_for_connect(self,okiba):
    for i in range(len(okiba)):
      if okiba[i].group(3) == "page=2":
        self.before_honbun[1] =''.join(self.array[1]["text"])#1
      elif okiba[i].group(3) == "page=3":
        self.before_honbun[2] =''.join(self.array[0]["text"])#0
      elif okiba[i].group(3) == "page=4":
        self.before_honbun[3] =''.join(None)
      elif okiba[i].group(3) == "page=5":
        self.before_honbun[4] =''.join(None)
      elif okiba[i].group(3) is None:
        self.before_honbun[0] =''.join(self.array[2]["text"])#2
      else:
        print("else")
    print("ビフォー本文")
    print(self.before_honbun)
    print("本文")
    self.honbun = ''.join(self.before_honbun)
    print(self.honbun)

l = MatomeClass()
l.main()
"""

#mecab_analysisより
#mecab =MeCab.Tagger("-Owakati")
#analysis = mecab.parse(article5)
#print(analysis)
#japanese_mecab_ipadic_neologd_vectorizer = TfidfVectorizer(analyzer=japanese_token_stemming2, min_df=1, max_df=50, stop_words=stop_word_list)

"""
mecab =MeCab.Tagger("-Ochasen")
analysis = mecab.parse(article5)
for l in analysis.split("\n"):#私\tワタシ\t私\t名詞-代名詞-一般\n
  o = l.split("\t")
  if len(o) >= 6:
    print("===========")
    print("word= ", o[0])
    print("yomi= ", o[1])
    print("orgn= ", o[2])
    print("type= ", o[3])
    print("?1 ", o[4])#五段・サ行
    print("?2 ", o[5])#連用形
"""




"""
def extract_words(article5):#単語だけ抽出
  mecab = MeCab.Tagger("")
  node = mecab.parseToNode(article5)
  words=[]
  while node:
    fs = node.feature.split(",")
    if (node.surface is not None) and node.surface != "" and fs[0] in ['名詞']:
      words.append(node.surface)
    node = node.next
  return words

print(extract_words(article5))
"""





"""サンプル
#分かち書きを表示
mecab =MeCab.Tagger("-Ochasen")
analysis = mecab.parse(article5)
for l in analysis.split("\n"):#私\tワタシ\t私\t名詞-代名詞-一般\n
  o = l.split("\t")
  if len(o) >= 6:
    print("===========")
    print("word= ", o[0])
    print("yomi= ", o[1])
    print("orgn= ", o[2])
    print("type= ", o[3])
    print("?1 ", o[4])#五段・サ行
    print("?2 ", o[5])#連用形

def extract_words(article5):#単語だけ抽出
  mecab =MeCab.Tagger("")
  node = mecab.parseToNode(article5)
  words=[]
  while node:
    fs = node.feature.split(",")
    if (node.surface is not None) and node.surface != "" and fs[0] in [u'名詞']:
      words.append(node.surface)
    node = node.next
  return words
print(extract_words(article5))


#テキストデータからTF_IDF特徴ベクトルを生成する・（CountVectorizerで）
#要はドキュメントを単語出現頻度の行列に変換する
from sklearn.feature_extraction.text import CountVectorizer

vectorizer = CountVectorizer(min_df=1)

text_owakati_list = [”週明け 日経平均株価 後場 大幅な 上昇 記録 市場関係者 先週 金曜日 FRB FOMC 声明 発表 好感”, ”大相撲 千秋楽 勝越丸 今場所 初めて 土 一敗”]

X = vectorizer.fit_transform(text_owakati_list)
vectorizer.get_feature_names()
print(X.toarray().transpose())

#sklearnでナイーブベイズによるテキスト分類にチャレンジ@Qiita
#ストップワードの参考
import numpy as np
from sklearn.datasets import fetch_20newsgroups
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
import nltk

def stopwords():
    symbols = ["'", '"', '`', '.', ',', '-', '!', '?', ':', ';', '(', ')', '*', '--', '\\']
    stopwords = nltk.corpus.stopwords.words('english')
    return stopwords + symbols

newsgroups_train = fetch_20newsgroups(subset='train', remove=('headers', 'footers', 'quotes'))
newsgroups_test  = fetch_20newsgroups(subset='test', remove=('headers', 'footers', 'quotes'))

vectorizer = CountVectorizer(stop_words=stopwords())
vectorizer.fit(newsgroups_train.data)

# Train
X = vectorizer.transform(newsgroups_train.data)
y = newsgroups_train.target
print(X.shape)

clf = MultinomialNB()
clf.fit(X, y)
print(clf.score(X,y))

# Test
X_test = vectorizer.transform(newsgroups_test.data) 
y_test = newsgroups_test.target

print(clf.score(X_test, y_test))


#article5 ="今年6月、中国ファーウェイ(華為技術)のリチャード・ユーCEOは、カンファレンスの席上で「アップルやサムスンを追い抜き、世界トップのスマホメーカーになる」と宣言した。その時、会場に居合わせた人々は誰もその発言を真剣には捉えなかった。ファーウェイにとって勝利までの道のりはまだ長いと思われる。しかし、同社は現時点で一定の成果を収めたことが明らかになった。調査企業Strategy Analyticsの最新データによると、ファーウェイは利益ベースでサムスンを追い抜き、アップルに次いで世界2位のスマホメーカーのポジションを獲得したのだ。ファーウェイの躍進はサムスンがNote 7 の発火問題に続くリコールで、直近の四半期の業績を大きく落としたことによるものだ。同社の2位の座は一時的なもので終わる可能性も高い。ファーウェイの今年第3四半期の利益は2億ドル(約226億円)。全スマホメーカーの利益、94億ドル(約1兆円)と比較すると、その2.4%にしか過ぎない。対するアップルは85億ドル(約9,600億円)の利益を生み出し、利益ベースで91%のシェアを獲得している。"

"""
