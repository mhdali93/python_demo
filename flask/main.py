from flask import Flask, request, jsonify
from utils import Utils

app = Flask(__name__)

items = []

@app.route('/')
def root():
    return {"message": "Welcome to Flask Sample App"}


@app.route("/listItem")
def list_items():
    return jsonify(items)

@app.route("/addItem", methods=['POST'])
@Utils.profiling_dec
def create_item():
    reqObj = request.json
    item = {
        "id": len(items)+1,
        "name": reqObj["name"] if "name" in reqObj else "",
        "desc": reqObj["desc"] if "desc" in reqObj else "",
        "price": reqObj["price"] if "price" in reqObj else 0
    }
    # Utils.hi_print(f"Item to be added: {item}")
    items.append(item)
    # Utils.hi_print(f"final list after adding item: {items}")
    return dict(item)


if __name__ == "__main__": 
    app.run(debug=True)