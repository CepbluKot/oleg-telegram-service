from flask import Flask, request, jsonify
import json, typing
from backend.storage import storage, StorageObject
from backend.storage import storage



app = Flask(__name__)


@app.route("/notify", methods=["POST"])
def notify():

    recieved = request.get_data().decode("utf-8")
    parsed = json.loads(recieved)

    to_append = StorageObject(text=parsed["text"], tg_id=parsed["tg_id"])
    storage.append(to_append)

    return jsonify(recieved)
