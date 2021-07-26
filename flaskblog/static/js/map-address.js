console.log("it works ");

let autocomplete;

function initAutocomplete() {
  console.log("autocomplete");
  // Create the autocomplete object, restricting the search to geographical
  // location types.
  autocomplete = new google.maps.places.Autocomplete(
    (document.getElementById("autocomplete")),
    { types: ["geocode"] }
  );

  // When the user selects an address from the dropdown, populate the address
  // fields in the form.
  autocomplete.addListener("place_changed", onPlaceChanged);
  let mylat = parseFloat(document.getElementById("lat").value)
  let mylng = parseFloat(document.getElementById("lng").value)
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 52.52, lng: 13.405 },
    zoom: 12,
    streetViewControl: false,
    mapTypeControl: false,
    scaleControl: false,
    rotateControl: false,
    fullscreenControl: false,
  });
  map.setCenter({lat:mylat, lng:mylng});
  var marker = new google.maps.Marker({
    map:map,
    position: {lat:mylat, lng:mylng}
  });
}

function onPlaceChanged() {
  let place = autocomplete.getPlace();
  console.log(place);
  console.log(place.formatted_address);
  console.log(place.geometry.location.lat());
  console.log(place.geometry.location.lng());

  if (!place.geometry) {
    //User did not select a predicition; reset the input field
    document.getElementById("autocomplete").placeholder = "Enter your address";
  } else {
    //Display detials about the valid place
    document.getElementById("lat").value = place.geometry.location.lat();
    document.getElementById("lng").value = place.geometry.location.lng();
    document.getElementById("address").value = place.formatted_address;
    
    var marker = new google.maps.Marker({
      map:map,
      position: place.geometry.location
    });
    if (place.geometry.viewport) {
      map.fitBounds(place.geometry.viewport);
    } else {
      map.setCenter(place.geometry.location);
      map.setZoom(17);
    }
  }
}
// Bias the autocomplete object to the user's geographical location,
// as supplied by the browser's 'navigator.geolocation' object.
function geolocate() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function (position) {
      var geolocation = {
        lat: position.coords.latitude,
        lng: position.coords.longitude,
      };
      var circle = new google.maps.Circle({
        center: geolocation,
        radius: position.coords.accuracy,
      });
      autocomplete.setBounds(circle.getBounds());
    });
  }
}

//google.maps.event.addDomListener(window, "load", initAutocomplete);
