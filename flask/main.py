from flask import Flask, request, jsonify
from utils import Utils
import time

app = Flask(__name__)

items = []

@app.route('/')
def root():
    return {"message": "Welcome to Flask Sample App"}


@app.route("/listItem")
def list_items():
    try:
        return jsonify(items)
    except Exception as e:
        raise(e)

@app.route("/addItem", methods=['POST'])
@Utils.logging_dec
@Utils.profiling_dec
def create_item():
    try:
        reqObj = request.json
        item = {
            "id": len(items)+1,
            "name": reqObj["name"] if "name" in reqObj else "",
            "desc": reqObj["desc"] if "desc" in reqObj else "",
            "price": reqObj["price"] if "price" in reqObj else 0
        }
        items.append(item)
        g = [[f"{x} x {y+1} = {x * (y+1)}" for y in range(10)] for x in range(50000)]
        
        time.sleep(1)

        print(g[1])
        print(items)
        return jsonify(item)
    except Exception as e:
        raise(e)



if __name__ == "__main__": 
    app.run(debug=True)