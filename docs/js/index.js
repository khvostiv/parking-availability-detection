// Load the Google Maps JavaScript API
const loadGoogleMaps = () => {
  const script = document.createElement('script');
  script.src = `https://maps.googleapis.com/maps/api/js?key=AIzaSyAaRAKhr9yrCSEP2eA9vgxyulHEE638b_k&callback=initMap&libraries=places&v=weekly`;
  script.async = true;
  script.defer = true;
  document.head.appendChild(script);
};

// Initialize the map
window.initMap = function () {
  const defaultCenter = { lat: 43.6834, lng: -79.7663 }; // Default location
  const infoWindow = new google.maps.InfoWindow();
  const markers = []; // Array to store markers

  // Create the map
  const map = new google.maps.Map(document.getElementById('map'), {
    zoom: 14,
    center: defaultCenter,
  });

  let userLocationMarker = null; 
  let searchedLocationMarker = null; 

  // Check if geolocation is available and use it to set map center
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        const userLocation = {
          lat: position.coords.latitude,
          lng: position.coords.longitude,
        };

        // Update map to the user's location
        map.setCenter(userLocation);
        infoWindow.setPosition(userLocation);
        infoWindow.setContent("You are here.");
        infoWindow.open(map);

        // Add user location marker
        if (userLocationMarker) {
          userLocationMarker.setMap(null);
        }
        userLocationMarker = new google.maps.Marker({
          position: userLocation,
          map: map,
          title: "Your Location",
          icon: {
            url: "./assets/icons/pin.png", 
            scaledSize: new google.maps.Size(30, 30),
          }
        });

        // Search for parking nearby the user's current location
        searchParkingNearby(userLocation, map, infoWindow, markers);
      },
      () => {
        // If geolocation fails, use default location
        handleLocationError(true, infoWindow, defaultCenter, map);
      }
    );
  } else {
    // If geolocation is not available, use default location
    handleLocationError(false, infoWindow, defaultCenter, map);
  }

  // Create Autocomplete for search input
  const autocomplete = new google.maps.places.Autocomplete(document.getElementById("autocomplete"));
  autocomplete.bindTo("bounds", map);

  autocomplete.addListener("place_changed", () => {
    const place = autocomplete.getPlace();
    if (!place.geometry || !place.geometry.location) {
      window.alert("No details available for the selected location!");
      return;
    }

    // Set the map center to the selected place's location
    map.setCenter(place.geometry.location);
    map.setZoom(14);

    // Clear previous markers and search for new parking nearby the selected location
    clearMarkers(markers);

    // Add a marker for the searched location
    if (searchedLocationMarker) {
      searchedLocationMarker.setMap(null); 
    }

    searchedLocationMarker = new google.maps.Marker({
      position: place.geometry.location,
      map: map,
      title: place.name,
      icon: {
        url: "./assets/icons/placeholder.png", 
        scaledSize: new google.maps.Size(30, 30), 
      }
    });

    // Call function to search for parking nearby the searched location
    searchParkingNearby(place.geometry.location, map, infoWindow, markers);
  });
};

// Function to handle location errors
function handleLocationError(browserHasGeolocation, infoWindow, pos, map) {
  infoWindow.setPosition(pos);
  infoWindow.setContent(
    browserHasGeolocation
      ? "Error: The Geolocation service failed."
      : "Error: Your browser doesn't support geolocation."
  );
  infoWindow.open(map);
}

// Function to clear markers from previous searches
function clearMarkers(markers) {
  markers.forEach(marker => marker.setMap(null)); // Remove markers from the map
  markers.length = 0; // Clear the markers array
}

// Function to search for nearby parking lots
function searchParkingNearby(location, map, infoWindow, markers) {
  const service = new google.maps.places.PlacesService(map);
  const request = {
    location: location,
    radius: 5000,
    type: ['parking'],
  };

  service.nearbySearch(request, (results, status) => {
    if (status === google.maps.places.PlacesServiceStatus.OK) {
      results.forEach(place => {
        const marker = new google.maps.Marker({
          position: place.geometry.location,
          map: map,
          title: place.name,
          icon: {
            url: "./assets/icons/parking.png",
            scaledSize: new google.maps.Size(30, 30),
          }
        });

        markers.push(marker); 

        // Add event listener inside the marker's click event handler
        marker.addListener("click", () => {

          console.log("Clicked parking lot place_id:", place.place_id);
          infoWindow.setContent(`
            <div>
              <h3>${place.name}</h3>
              <p>${place.vicinity}</p>
              <button id="availability-btn" class="see-availability-button">Check Availability</button>
            </div>
          `);
          infoWindow.open(map, marker); 

          // Add event listener for the "Availability" button
          google.maps.event.addListenerOnce(infoWindow, 'domready', () => {
            const availabilityButton = document.getElementById("availability-btn");
            if (availabilityButton) {
              availabilityButton.addEventListener("click", () => {

                const onLocalHost =
                  window.location.hostname === "localhost" ||
                  window.location.hostname === "127.0.0.1";
                window.location.href = onLocalHost
                  ? "http://localhost:5000"
                  : "camera.html";
              });
            }
          });
          
        });
      });
    }
  });
}


// Load the Google Maps API script
loadGoogleMaps();
