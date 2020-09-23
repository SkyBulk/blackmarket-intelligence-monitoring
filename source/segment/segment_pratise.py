from os import path
import jieba.analyse as analyse

d = path.dirname(__file__)

text_path = "../data/test_message.txt"
text = open(path.join(d, text_path)).read()

for key in analyse.extract_tags(text,50, withWeight=False):
# 使用jieba.analyse.extract_tags()参数提取关键字,默认参数为50
    print(key)