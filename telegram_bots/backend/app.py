from flask import Flask, request, jsonify
import json
import bot_backend.storag

app = Flask(__name__)


@app.route("/notify", methods=["POST"])
async def notify():

    text = json.loads(request.get_data().decode("utf-8"))

    to_append = bot_backend.storag.StorObj()
    to_append.text = text["text"]
    to_append.userid = text["user_id"]
    bot_backend.storag.stor.append(to_append)

    return jsonify("done")
