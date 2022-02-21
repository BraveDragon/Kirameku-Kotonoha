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
  
def CreatePoem(firstText:str,result:dict):
    first_token = firstText
    numOfChars = [5,12,17]
    partCount = 0
    poem = first_token
    while partCount < 3:
        while CountSounds(poem) <= numOfChars[partCount]:
            if first_token in result.keys():
                next_candidates = result[first_token]
                if 0 >= len(next_candidates):
                    next_token = next_candidates[0]
                else:
                    next_token = next_candidates[np.random.randint(0,len(next_candidates))]
                poem = poem + next_token
            else:
                #モデルにない文字がやってきた時はランダムに1つ選ぶ
                next_token = list(result.keys())[np.random.randint(0,len(result.keys()))]
            first_token = next_token
        partCount += 1
        
    return poem
    

#以下は実行テスト・デバッグ用のコード
if __name__ == "__main__":
    with open("model.pkl",mode="rb") as model:
        model = pickle.load(model)
        print(CreatePoem("我",model))








