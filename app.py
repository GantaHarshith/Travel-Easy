from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory

from script import places

PROJECT_DIR = Path(__file__).resolve().parent
app = Flask(__name__)


@app.route("/")
def home():
    return send_from_directory(PROJECT_DIR, "index.html")


@app.route("/style.css")
def stylesheet():
    return send_from_directory(PROJECT_DIR, "style.css")


@app.route("/api/search", methods=["GET"])
@app.route("/search", methods=["GET"])
def search_hotels():

    location = request.args.get("city", request.args.get("location", "")).strip().lower()

    if not location:
        return jsonify([])

    results = [place for place in places if location in place["city"]]

    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True)