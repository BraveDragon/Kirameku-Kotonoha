from flask import Flask, request, jsonify
from flask_cors import CORS
import CreatePoem
import pickle
import urllib.parse
import NPclassifier

app = Flask(__name__)
CORS(app, supports_credentials=True)

with open("model.pkl",mode="rb") as model:
        model = pickle.load(model)

@app.route("/",methods=["GET"])
def index():
    return app.send_static_file("index.html")

@app.route("/poem",methods=["GET"])
def getPoem():
    Req = request.args
    FirstPoem = CreatePoem.CreatePoem(urllib.parse.unquote(Req["firstTop"]),model)
    SecondPoem = CreatePoem.CreatePoem(urllib.parse.unquote(Req["secondTop"]),model)
    print("first : "+urllib.parse.unquote(Req["firstTop"]))
    print("second : "+urllib.parse.unquote(Req["secondTop"]))
    positiveFlag = NPclassifier.GetIsPositive(Req["firstTop"]+Req["secondTop"])
    return jsonify({"firstPoem":FirstPoem,"secondPoem":SecondPoem,"positiveFlag":positiveFlag})

if __name__ == "__main__":
    app.run(port=8080)