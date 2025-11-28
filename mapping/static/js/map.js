document.addEventListener("DOMContentLoaded", function() {
    var map = L.map('map').setView([27.73613, 85.30592], 13);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '© OpenStreetMap contributors'
}).addTo(map);

var markersLayer = L.layerGroup().addTo(map);

if (typeof L.control.locate === "function") {
    L.control.locate({
        position: "topleft",
        setView: "once",
        drawMarker: false,
        showPopup: false,
        strings: { title: "Go to my current location" }
    }).addTo(map);
} else {
    console.warn("LocateControl plugin is not loaded!");
}




// Load markers from JSON
const pointJsonElement = document.getElementById('point_json');

if (!pointJsonElement) {
  console.error("point_json element not found");
} else {
  try {
    let parks = JSON.parse(pointJsonElement.textContent);
    if (!Array.isArray(parks) || parks.length === 0) {
      console.warn("No valid park data to display markers");
    } else {
      parks.forEach((park, index) => {
        if (park.latitude == null || park.longitude == null || isNaN(park.latitude) || isNaN(park.longitude)) {
          console.error(`Invalid coordinates at index ${index}:`, park);
          return;
        }
        const marker = L.marker([park.latitude, park.longitude])
          .addTo(map)
          .bindPopup(`Name: ${park.name} <br> Park ID: ${park.id}<br>Lat: ${park.latitude}<br>Lng: ${park.longitude}`);
        
        marker.parkId = park.id;

        marker.on('click', function () {
          if (deleteMarkerMode) {
            if (confirm("Do you want to delete this park?")) {
              fetch(`/api/delete-park/${marker.parkId}/`, {
                method: 'DELETE',
                headers: { 'X-CSRFToken': getCsrfToken() }
              })
              .then(response => {
                if (!response.ok) throw new Error("Failed to delete from server");
                map.removeLayer(marker);
                alert("Marker deleted successfully!");
              })
              .catch(error => {
                console.error("Error deleting marker:", error);
                alert("Failed to delete marker.");
              });
            }
          } else if (editMarkerMode) {
            const clickedMarker = this;
            clickedMarker.dragging.enable();
            clickedMarker.on('dragend', function () {
              if (confirm("Do you want to edit marker?")) {
                const { lat, lng } = clickedMarker.getLatLng();
                fetch(`/api/edit-park/${park.id}/`, {
                  method: 'PUT',
                  headers: {
                    'X-CSRFToken': getCsrfToken(),
                    'Content-Type': 'application/json'
                  },
                  body: JSON.stringify({ latitude: lat, longitude: lng })
                })
                .then(response => {
                  if (!response.ok) throw new Error("Failed to edit from server");
                })
                .catch(error => {
                  console.error("Error updating marker:", error);
                  alert("Failed to update marker.");
                });
              } else {
                clickedMarker.dragging.disable();
              }
            });
          }
        });
      });
    }
  } catch (e) {
    console.error("Error parsing point_json:", e);
  }
}

// Map click to add markers
map.on('click', function(e) {
  if (addMarkerMode) {
    const { lat, lng } = e.latlng;
    const marker = L.marker([lat, lng]).addTo(map);

    fetch('/api/add-park/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCsrfToken(),
      },
      body: JSON.stringify({ latitude: lat, longitude: lng })
    })
    .then(response => response.json())
    .then(data => {
      if (data.error) {
        console.error("Error saving marker:", data.error);
        alert("Failed to save marker: " + data.error);
      } else {
        console.log("Marker saved successfully:", data);
      }
    })
    .catch(error => {
      console.error("Error saving marker:", error);
      alert("Failed to save marker: Network error");
    });

    addMarkerMode = false;
    console.log("Add marker mode disabled.");
  }

  if(editMarkerMode){
    console.log("You can now edit markers");
  }
});
});