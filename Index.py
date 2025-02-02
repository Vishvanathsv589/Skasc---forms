from flask import Flask, render_template_string

app = Flask(__name__)

@app.route("/")
def google_form():
    center_lat = 10.939328   # Your target latitude
    center_lng = 76.958976   # Your target longitude    
    max_distance =   50# Radius in meters

    return render_template_string(f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Google Form</title>
        <style>
            #location-display {{
                position: fixed;
                top: 10px;
                right: 10px;
                background: rgba(255, 255, 255, 0.8);
                padding: 10px;
                border-radius: 8px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                font-family: Arial, sans-serif;
                font-size: 14px;
            }}
            #form-container iframe {{
                border: none;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                width: 100%;
                max-width: 700px;
                height: 520px;
            }}
            #form-container h2 {{
                text-align: center;
                font-family: Arial, sans-serif;
                color: #333;
            }}
        </style>
        <script>
            const centerLat = {center_lat};
            const centerLng = {center_lng};
            const maxDistance = {max_distance}; // in meters

            function toRadians(degrees) {{
                return degrees * (Math.PI / 180);
            }}

            function calculateDistance(lat1, lng1, lat2, lng2) {{
                const R = 6371000; // Earth's radius in meters
                const dLat = toRadians(lat2 - lat1);
                const dLng = toRadians(lng2 - lng1);
                const a = 
                    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
                    Math.cos(toRadians(lat1)) * Math.cos(toRadians(lat2)) *
                    Math.sin(dLng / 2) * Math.sin(dLng / 2);
                const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
                return R * c; // Distance in meters
            }}

            function displayLocation(lat, lng) {{
                const locationDisplay = document.getElementById('location-display');
                locationDisplay.textContent = `Your Location: Lat ${{lat.toFixed(6)}}, Lng ${{lng.toFixed(6)}}`;
            }}

            function checkAccess() {{
                if (navigator.geolocation) {{
                    navigator.geolocation.getCurrentPosition(position => {{
                        const userLat = position.coords.latitude;
                        const userLng = position.coords.longitude;

                        displayLocation(userLat, userLng);

                        const distance = calculateDistance(centerLat, centerLng, userLat, userLng);
                        if (distance <= maxDistance) {{
                            document.getElementById('form-container').innerHTML = `
                                <iframe 
                                    src="https://docs.google.com/forms/d/e/1FAIpQLScjIV8PHk4dSK5J_e0AXvmXIxGDSg_FPm4087-D1cj8p8XCjQ/viewform?embedded=true"
                                    width="640" height="4179" frameborder="0" marginheight="0" marginwidth="0">
                                    Loading…
                                </iframe>`;
                        }} else {{
                            document.getElementById('form-container').innerHTML = "<h2>Access Denied: You are not within the allowed location.</h2>";
                        }}
                    }}, () => {{
                        document.getElementById('form-container').innerHTML = "<h2>Location access is required to access this form.</h2>";
                    }});
                }} else {{
                    document.getElementById('form-container').innerHTML = "<h2>Geolocation is not supported by your browser.</h2>";
                }}
            }}

            document.addEventListener('DOMContentLoaded', checkAccess);
        </script>
    </head>
    <body>
        <div id="location-display">Detecting your location...</div>
        <div id="form-container" style="display: flex; justify-content: center; align-items: center; min-height: 100vh; font-family: Arial, sans-serif;">
            <h2>Loading...</h2>
        </div>
    </body>
    </html>
    """)

if __name__ == "__main__":
    app.run(debug=True)