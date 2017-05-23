# __*__ coding:utf-8 __*__

import jieba
import sys

reload(sys)
sys.setdefaultencoding('utf8')

stopword_path = r'E:\opensource_project\Chinese-master\stopwords.dat'
class seg_word(object):
	def __init__(self, inputpath, outputpath):
		self.inputpath = inputpath
		self.outputpath = outputpath

	def cut_data(self):
		with open(inputpath, 'r') as fr:
			res = jieba.cut(fr.read())
		return res

	def output_file(self):
		outcome = self.filter_data()
		with open(outputpath, 'w') as fw:
			fw.write(' '.join(outcome).encode('utf-8'))

	def filter_data(self):
		with open(stopword_path,'r') as f:
			stopword_list = f.read()
		seg_res = self.cut_data()
		res_list = [word.strip() for word in seg_res if word not in stopword_list]
		return res_list





if __name__ == '__main__':
	inputpath = r'E:\opensource_project\SynthText-master\test\people.txt'
	outputpath = r'E:\opensource_project\SynthText-master\test\seg_people1.txt'
	c = seg_word(inputpath, outputpath)
	c.output_file()
