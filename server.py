from flask import Flask, render_template, jsonify, request, session
from datetime import timedelta

import boto3
from boto3.session import Session


PUBLIC_IP = "********"
PRIVATE_IP = "192.168.0.8"
PORT = "7480"


access_key = "*******"
secret_key = "********"

app = Flask(__name__)
app.config["SECRET_KEY"] = "bigdataprocessing"
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=3)

@app.route("/", methods=["GET"])
def index():
    return render_template("login.html")

@app.route("/player", methods=["GET"])
def player():
    return render_template("player.html")

@app.route("/login", methods=["POST"])
def login():
    ak = request.form["ak"]
    sk = request.form["sk"]
    client = Session(ak, sk).client("s3", endpoint_url=f"http://{PRIVATE_IP}:{PORT}/")
    try:
        client.list_buckets()
        session["ak"] = ak
        session["sk"] = sk
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"status": "error", "errmsg": str(e)})

@app.route("/videoslist", methods=["GET"])
def videoslist():
    ak = session.get("ak")
    sk = session.get("sk")
    host = f"http://{PRIVATE_IP}:{PORT}/"
    client = Session(ak, sk).client("s3", endpoint_url=host)
    try:
        response = {
            "status": "ok",
            "data": {
                "host": f"http://{PUBLIC_IP}:{PORT}",
                "videos": []
            }
        }
        video_list = [v["Key"] for v in client.list_objects(Bucket="videos")["Contents"]]
        for video_key in video_list:
            metadata = client.head_object(Bucket="videos", Key=video_key)["Metadata"]
            response["data"]["videos"].append({
                "title": metadata.get("title", "No desc"),
                "desc": metadata.get("desc", "No description"),
                "src": f"/videos/{video_key}",
                "cover": f"/images/{metadata.get('cover', 'default')}"
            })
        return jsonify(response)
    except Exception as e:
        response = {
            "status": "error",
            "errmsg": str(e)
        }
        return jsonify(response)


if __name__ == '__main__':
    app.run(host=PRIVATE_IP, port=80, debug=True)
