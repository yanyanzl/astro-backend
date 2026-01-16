from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from astro import calculate_chart

app = Flask(__name__)
CORS(app)  # Allow requests from Netlify frontend

@app.route("/", methods=["GET"])
def health_check():
    """
    Health check endpoint
    """
    return jsonify({
        "status": "ok",
        "service": "Swiss Ephemeris Astrology Backend"
    })


@app.route("/chart", methods=["POST"])
def chart():
    """
    Calculate a natal or transit chart using Swiss Ephemeris

    Expected JSON payload:
    {
      "datetime": "1990-05-17T14:30",
      "lat": 40.7,
      "lon": -74.0
    }
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "Missing JSON body"}), 400

        dt = datetime.fromisoformat(data["datetime"])
        lat = float(data["lat"])
        lon = float(data["lon"])

        chart_data = calculate_chart(dt, lat, lon)

        return jsonify({
            "success": True,
            "chart": chart_data
        })

    except KeyError as e:
        return jsonify({
            "error": f"Missing required field: {str(e)}"
        }), 400

    except Exception as e:
        return jsonify({
            "error": "Chart calculation failed",
            "details": str(e)
        }), 500


if __name__ == "__main__":
    # Render requires host 0.0.0.0 and a fixed port
    app.run(host="0.0.0.0", port=10000)
