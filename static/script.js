const centerLat = 10.939328;
const centerLng = 76.958976;
const maxDistance = 50;

function toRadians(degrees) {
    return degrees * (Math.PI / 180);
}

function calculateDistance(lat1, lng1, lat2, lng2) {
    const R = 6371000; // Earth's radius in meters
    const dLat = toRadians(lat2 - lat1);
    const dLng = toRadians(lng2 - lng1);
    const a = 
        Math.sin(dLat / 2) * Math.sin(dLat / 2) +
        Math.cos(toRadians(lat1)) * Math.cos(toRadians(lat2)) *
        Math.sin(dLng / 2) * Math.sin(dLng / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return R * c; // Distance in meters
}

function displayLocation(lat, lng) {
    const locationDisplay = document.getElementById('location-display');
    locationDisplay.textContent = `Your Location: Lat ${lat.toFixed(6)}, Lng ${lng.toFixed(6)}`;
}

function checkAccess() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(position => {
            const userLat = position.coords.latitude;
            const userLng = position.coords.longitude;

            displayLocation(userLat, userLng);

            const distance = calculateDistance(centerLat, centerLng, userLat, userLng);
            if (distance <= maxDistance) {
                document.getElementById('form-container').innerHTML = `
                    <iframe 
                        src="https://docs.google.com/forms/d/e/1FAIpQLScjIV8PHk4dSK5J_e0AXvmXIxGDSg_FPm4087-D1cj8p8XCjQ/viewform?embedded=true"
                        width="640" height="4179" frameborder="0" marginheight="0" marginwidth="0">
                        Loading…
                    </iframe>`;
            } else {
                document.getElementById('form-container').innerHTML = "<h2>Access Denied: You are not within the allowed location.</h2>";
            }
        }, () => {
            document.getElementById('form-container').innerHTML = "<h2>Location access is required to access this form.</h2>";
        });
    } else {
        document.getElementById('form-container').innerHTML = "<h2>Geolocation is not supported by your browser.</h2>";
    }
}

document.addEventListener('DOMContentLoaded', checkAccess);
