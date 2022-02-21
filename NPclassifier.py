#coding:"utf-8"
#ポジネガ判別する
from asari.api import Sonar

def GetIsPositive(text:str):
    sonar = Sonar()
    if sonar.ping(text)["top_class"] == "positive":
        return True
    else: 
        return False