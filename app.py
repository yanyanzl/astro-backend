from flask import Flask, request, jsonify
from flask_cors import CORS
from astro import calculate_chart
from datetime import datetime

app = Flask(__name__)
CORS(app)

@app.route("/chart", methods=["POST"])
def chart():
    data = request.json

    dt = datetime.fromisoformat(data["datetime"])
    lat = float(data["lat"])
    lon = float(data["lon"])

    result = calculate_chart(dt, lat, lon)
    return jsonify(result)

@app.route("/")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
