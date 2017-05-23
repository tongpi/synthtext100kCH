# __*__ coding: utf-8 __*__
from __future__ import division
from collections import Counter
import cPickle
import codecs
import sys

reload(sys)
sys.setdefaultencoding('utf8')

filename = 'E:/opensource_project/SynthText-master/test/newsgroup.txt'
with codecs.open(filename,'r',encoding='utf-8') as f:
# with open(filename, 'r') as f:
	c = Counter()
	for x in f:
		c += Counter(x.strip())
		# print c
d = dict(c)
print d
res_dict = {}
# total_char_freq = 0
# for value in d.values():
# 	total_char_freq += value
for key in d.keys():
	if not res_dict.has_key(key) and key != ' ':
		key1 = key.decode('utf-8', errors='replace').encode('utf-8')
		res_dict[key1] = d[key] / sum(d.values())
	else:
		continue
for k, v in res_dict.iteritems():
	print k,v
	# decode的作用是将其他编码的字符串转换成unicode编码，如str1.decode('gb2312')，表示将gb2312编码的字符串转换成unicode编码。
	# encode的作用是将unicode编码转换成其他编码的字符串，如str2.encode('gb2312')，表示将unicode编码的字符串转换成gb2312编码。
with codecs.open("freq4.cp", 'wb',encoding='utf-8') as f:
	# pickle.dump(d, f)
	cPickle.dump(res_dict, f)
