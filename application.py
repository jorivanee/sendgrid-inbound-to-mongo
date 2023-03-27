from flask import Flask, request, jsonify
import json
from pymongo import MongoClient
import werkzeug

with open('config.json') as config_file:
    config = json.load(config_file)


app = Flask(__name__)
app.db_client = MongoClient(config['mongo']['host'], config['mongo']['port'])
app.database = app.db_client[config['mongo']['database']]


@app.errorhandler(werkzeug.exceptions.NotFound)
def handle_error(e):
    return jsonify({"error": True, "message": "Not Found", "code": 404}), 404


@app.route("/", methods=['GET'])
def index():
    return handle_error(None)


@app.route("/", methods=['POST'])
def store_email():
    raw_email = request.form.to_dict()
    headers = {k: v.strip() for k, v in [line.split(
        ":", 1) for line in raw_email['headers'].splitlines() if ":" in line]}
    entry = {"headers": headers, "text": raw_email['text'].strip(
    ), "subject": raw_email['subject'], "to": raw_email['to'], "html": raw_email["html"], "sender_ip": raw_email['sender_ip'], "from": raw_email['from'], "envelope": json.loads(raw_email['envelope'])}
    app.database.emails.insert_one(entry)
    return jsonify({"success": True}), 202


if __name__ == "__main__":
    app.run(port=5000, debug=True)