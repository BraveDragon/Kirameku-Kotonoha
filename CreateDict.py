from janome.tokenizer import Tokenizer
import numpy as np
import pykakasi
import pickle

#音数をカウント
def CountSounds(text:str):
    converter = pykakasi.kakasi()
    raw_result = converter.convert(text)
    full_kana = ""
    for result in raw_result:
        full_kana = full_kana + result["hira"]
    return len(full_kana) - (full_kana.count("ゃ")+full_kana.count("ぃ")+full_kana.count("ゅ")+full_kana.count("ぇ")+full_kana.count("ょ")) 


#形態素解析して俳句を品詞ごとに分割
def Split(text:str):
    spliter = Tokenizer()
    tokenized_texts = spliter.tokenize(text)
    tokenized_text_list =[tokenized_text.surface for tokenized_text in tokenized_texts]
    return tokenized_text_list

def CreateModel(tokenized:list):
    Result = {}
    tokenlength = len(tokenized) - 1
    for i in range(tokenlength):
        #改行は終了の意味なので、マルコフ連鎖のディクショナリのキーに入れない
        if tokenized[i] != "\n":
            #ディクショナリにない項目は新規追加、ある項目はappend()する
            #いずれの場合も、改行以外である場合のみ格納する
            if tokenized[i] not in Result:
                if tokenized[i+1] != "\n":
                    Result[tokenized[i]] = [tokenized[i+1]]
            elif tokenized[i+1] != "\n":
                Result[tokenized[i]].append(tokenized[i+1])
    return Result

#AllText.txtに、今回学習に使用した正岡子規の俳句が全て入っている
with open("AllText.txt",mode="r",encoding="utf-8") as textFile:
    texts = textFile.read()
    texts.replace("\n","")
    each_poem = Split(texts)
    Result = CreateModel(each_poem)
    with open("model.pkl",mode="wb") as model:
        pickle.dump(Result,model)
 
    








