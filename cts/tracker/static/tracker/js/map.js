function initMap() {
    const center = {lat: 39.828300, lng: -98.579500};
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 5,
        center: center,
        mapTypeId: 'roadmap'
    });
    geocoder = new google.maps.Geocoder;
    infoWindow = new google.maps.InfoWindow();
    // This event listener will call addMarker() when the map is clicked.
    map.addListener('click', function(event) {
      addMarker(event.latLng);
    });
}