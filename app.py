from flask import Flask, render_template, request, jsonify
from math import radians, sin, cos, sqrt, atan2

app = Flask(__name__)

# Define the allowed location (latitude & longitude) and radius (meters)
CENTER_LAT = 11.013325
CENTER_LNG = 76.988416
MAX_DISTANCE = 50  # 50 meters

def calculate_distance(lat1, lng1, lat2, lng2):
    """Calculate the distance between two lat/lng points using the Haversine formula."""
    R = 6371000  # Radius of the Earth in meters
    dlat = radians(lat2 - lat1)
    dlng = radians(lng2 - lng1)
    
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlng / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    return R * c  # Distance in meters

@app.route("/")
def index():
    """Render the main page."""
    return render_template("index.html")

@app.route("/check_location", methods=["POST"])
def check_location():
    """API endpoint to verify if the user is within the allowed location."""
    data = request.json
    user_lat = float(data.get("latitude"))
    user_lng = float(data.get("longitude"))
    
    distance = calculate_distance(CENTER_LAT, CENTER_LNG, user_lat, user_lng)
    
    if distance <= MAX_DISTANCE:
        return jsonify({"status": "allowed", "message": "Access granted.", "distance": distance})
    else:
        return jsonify({"status": "denied", "message": "Access denied. You are outside the allowed location.", "distance": distance})

if __name__ == "__main__":
    app.run(debug=True)
