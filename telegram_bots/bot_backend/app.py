from flask import Flask, request, jsonify
import json
from bot_modules.notifications.input_output_realisation import notifications_abs
import bot_backend.storag
app = Flask(__name__)

@app.route("/notify", methods=["POST"])
def hello_world():

    text = json.loads(request.get_data().decode('utf-8'))
    
    to_append = bot_backend.storag.StorObj()
    to_append.text = text['text']
    to_append.userid = text['user_id']
    bot_backend.storag.stor.append(to_append)

    return jsonify('done')
