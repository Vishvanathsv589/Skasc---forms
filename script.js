function getLocationAndCheckAccess() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(position => {
            const userLat = position.coords.latitude;
            const userLng = position.coords.longitude;

            document.getElementById("location-display").textContent = `Your Location: Lat ${userLat.toFixed(6)}, Lng ${userLng.toFixed(6)}`;

            fetch("/check_location", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ latitude: userLat, longitude: userLng })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === "allowed") {
                    document.getElementById("form-container").innerHTML = `
                        <iframe src="https://docs.google.com/forms/d/e/1FAIpQLScjIV8PHk4dSK5J_e0AXvmXIxGDSg_FPm4087-D1cj8p8XCjQ/viewform?embedded=true"
                        width="640" height="4179" frameborder="0" marginheight="0" marginwidth="0">
                        Loading…
                        </iframe>`;
                } else {
                    document.getElementById("form-container").innerHTML = `<h2>${data.message}</h2>`;
                }
            })
            .catch(() => {
                document.getElementById("form-container").innerHTML = "<h2>Error checking access. Try again later.</h2>";
            });

        }, () => {
            document.getElementById("form-container").innerHTML = "<h2>Location access is required to access this form.</h2>";
        });
    } else {
        document.getElementById("form-container").innerHTML = "<h2>Geolocation is not supported by your browser.</h2>";
    }
}

document.addEventListener("DOMContentLoaded", getLocationAndCheckAccess);
