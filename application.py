from aiohttp import ClientError
from flask import Flask, request, jsonify
import json
from pymongo import MongoClient
import werkzeug
import time

with open('config.json') as config_file:
    config = json.load(config_file)


app = Flask(__name__)
app.db_client = MongoClient(
    config['mongo']['host'], config['mongo']['port'], connect=False)
app.database = app.db_client[config['mongo']['database']]
if config['store_attachments']:
    import boto3
    kwargs = {}
    if "s3" in config:
        kwargs = {"endpoint_url": config['s3']['endpoint'],
                  "aws_access_key_id": config['s3']['access_key'],
                  "aws_secret_access_key": config['s3']['secret_key'],
                  "aws_session_token": None,
                  "config": boto3.session.Config(
            signature_version='s3v4'),
            "verify": False}
    app.s3 = boto3.client('s3', **kwargs)

    try:
        app.s3.head_bucket(Bucket=config['s3']['bucket'])
    except ClientError:
        app.s3.create_bucket(Bucket=config['s3']['bucket'])


@app.errorhandler(werkzeug.exceptions.NotFound)
def handle_error(_):
    return jsonify({"error": True, "message": "Not Found", "code": 404}), 404


@app.route(config['webhook_path'], methods=['GET'])
def index():
    return handle_error(None)


@app.route(config['webhook_path'], methods=['POST'])
def store_email():
    timestamp = int(time.time())
    raw_email = request.form.to_dict()
    headers = {k: v.strip() for k, v in [line.split(
        ":", 1) for line in raw_email['headers'].splitlines() if ":" in line]}
    entry = {"headers": headers, "envelope": json.loads(raw_email['envelope'])}
    for e in ['text', 'html', 'subject', 'to', 'sender_ip', 'from']:
        if e in raw_email:
            entry[e] = raw_email[e]
    entry['timestamp'] = timestamp
    if config['store_attachments']:
        files = []
        for f in request.files:
            file = request.files[f]
            print(file.mimetype)
            filename = str(timestamp)+"/"+file.filename
            app.s3.upload_fileobj(
                file.stream, config['s3']['bucket'], filename, ExtraArgs={'ContentType': file.mimetype})
            files.append(config['s3']['bucket'] + "/"+filename)
        entry['files'] = files
    app.database.emails.insert_one(entry)
    return jsonify({"success": True}), 202


if __name__ == "__main__":
    app.run(port=5000, debug=True)
