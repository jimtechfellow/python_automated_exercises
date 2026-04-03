import threading
import time

from flask import Flask, jsonify, request

from auth_ex2 import APIExtractionMachine

app = Flask(__name__)


@app.route("/login", methods=["POST"])
def login():
    body = request.get_json(silent=True) or {}
    if body.get("user") == "admin" and body.get("pass") == "123":
        return jsonify({"token": "mock_valid_token"})
    return jsonify({"error": "unauthorized"}), 401


@app.route("/data")
def data():
    auth = request.headers.get("Authorization")
    if auth != "Bearer mock_valid_token":
        return "", 401
    return jsonify({"status": "success", "payload": "classified_data"})


if __name__ == "__main__":
    server = threading.Thread(
        target=lambda: app.run(host="127.0.0.1", port=5000, use_reloader=False),
        daemon=True,
    )
    server.start()
    time.sleep(1)

    machine = APIExtractionMachine(
        login_url="http://127.0.0.1:5000/login",
        credentials={"user": "admin", "pass": "123"},
    )
    data_url = "http://127.0.0.1:5000/data"
    result = machine.fetch_data_with_retry(data_url)
    print(result)
