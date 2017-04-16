# -*- coding: utf-8 -*-

import numpy
#from article import *
import re
"""

"センテンス1-1。センテンス1-2。センテンス1-3。センテンス1-4。センテンス1-5。センテンス1-6。センテンス1-7。"

=>
この例では3文ずつ分けた

window_all=
["センテンス1-1。センテンス1-2。センテンス1-3。","センテンス1-4。センテンス1-5。センテンス1-6。","センテンス1-7。"]

"""

#honbunListから一つずつ取り出されたものがhonbunという変数に渡され、windows_makeの引数になる
def windows_make(honbun):
	window_size =3# #一つの記事を何個の文（句点でくぎられた塊）でわけるか？
	target = honbun
	sentence_sum = len(re.findall(r'([\w]+。)',target))
	windows_sum = sentence_sum % window_size
	#記事を句点で区切って配列に入れる
	window_all = re.findall(r'([^\n][\w\s\W][^\。]+。)',target)
	#ウィンドウサイズ数の文のかたまりを作って配列に追加する
	window =[]
	for i in range(sentence_sum // window_size):
		if i is not 0:#1=>3,2=>6,3=>9
			k = i*window_size
		else:
			k = i

		kousei1 =[]
		for add_times in range(window_size-1):#0-2
			kousei1.append(window_all[k+add_times])
		window_text =''.join(kousei1)
		window.append(window_text)
		#window.append(window_all[k]+window_all[k+1]+window_all[k+2])みたいなことをしている
	
	#ウィンドウサイズ以下の塊があるとき
	if windows_sum is not 0:
		kousei2 =[]
		for x in range(1,windows_sum + 1):#rangeは最後−1までなので＋1しとく windows_sum+1=2
			toridasi = -(window_size - 1)#-2
			if windows_sum + 1 is 2 and x is 1:
				kousei2.append(window_all[-1])
			else:
				if x is 1:
					kousei2.append(window_all[toridasi])
				elif x is not 1:
					toridasi = toridasi + 1 * (x-1)
					kousei2.append(window_all[toridasi])
		window_text2 =''.join(kousei2)
		window.append(window_text2)
	return window
	#print("ウィンドウの中身")
	#print(window)
	