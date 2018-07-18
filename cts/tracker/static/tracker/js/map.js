function initMap() {
    const center = {lat: 39.828300, lng: -98.579500};
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 5,
        center: center,
        mapTypeId: 'roadmap'
    });
    geocoder = new google.maps.Geocoder;
    infoWindow = new google.maps.InfoWindow();
}


// Change Browse button text to filename
$(function() {
    $("#id_file").change(function() {
        let input = $(this),
            label = input.val().replace(/\\/g, '/').replace(/.*\//, '');
        allowUpload(label);
    });

    function allowUpload(label) {
        if (label.split('.')[1] !== 'gpx') {
            alert("You must select a valid GPX file.")
        } else {
            $("#label-text").text(label);
            $('#upload-btn').toggleClass('disabled');
        }
    }
});


function updateGeometry(currentObject, waypoint) {
    let newLat = $(this).latLng.lat();
    let newLng = $(this).latLng.lng();
    currentObject.find('span.geometry').replaceWith(newLat + ', ' + newLng);
    waypoint.lat = newLat;
    waypoint.lng = newLng;
    $('#saveWaypoints').css('display', 'block');
}


function searchWaypoints(searchURL) {
    geocoder.geocode({
        'address': $('#address').val()
    }, function (results, status) {
        if (status === google.maps.GeocoderStatus.OK) {
            let position = results[0].geometry.location;
            $.get(searchURL, {
                lat: position.lat(),
                lng: position.lng()
            }, function (data) {
                if (data.isOK) {
                    $('#waypoints').html(data.content);
                    waypointByID = data.waypointByID;
                    activateWaypoints();
                } else {
                    alert(data.message);
                }
            }, 'json');
        } else {
            alert('Could not find geocoordinates for the following reason: ' + status);
        }
    });
}

// Adds a marker to the map and push to the array.
function addMarker(location, addMarkerURL) {
    const marker = new google.maps.Marker({
        position: location,
        map: map,
        draggable: true
    });
    marker.addListener("click", function () {
        infoWindow.setContent('<p>Latitude: ' + marker.position.lat() + '</p>' +
            '<p>Longitude: ' + marker.position.lng() + '</p>');
        infoWindow.open(map, marker);
    });
    $.ajax({
        url: addMarkerURL,
        data: {
            'name': 'User marker added ' + Date.now(),
            'lat': marker.position.lat(),
            'lng': marker.position.lng()
        },
        dataType: 'json',
        success: function (data) {
            document.getElementById("waypointWindow").innerHTML = data.content;
        }
    });
}

// Escapes HTML characters in a template literal string, to prevent XSS.
// See https://www.owasp.org/index.php/XSS_%28Cross_Site_Scripting%29_Prevention_Cheat_Sheet#RULE_.231_-_HTML_Escape_Before_Inserting_Untrusted_Data_into_HTML_Element_Content
function sanitizeHTML(strings) {
    const entities = {'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'};
    let result = strings[0];
    for (let i = 1; i < arguments.length; i++) {
        result += String(arguments[i]).replace(/[&<>'"]/g, (char) => {
            return entities[char];
        });
        result += strings[i];
    }
    return result;
}

$(document).ready(function () {
    console.log('document ready.');
    $("#pstz_slider").parent().change(load_pstz);
    function load_pstz() {
        console.log('click detected on pstz slider.');
        if (loading === false && pstz === false && $("#pstz_slider").parent().hasClass("switch-on")) {
            loading = true;
            console.log('the slider is on so fetching json data...');
            map.data.loadGeoJson("{% static 'tracker/data/provision_seed_zones/psz.geojson' %}");

            const pszColors = {
                "<0 Deg. F. / < 2": "#895943",
                "<0 Deg. F. / 2 - 3": "#cc8865",
                "<0 Deg. F. / 3 - 6": "#f67677",
                "<0 Deg. F. / 6 - 12": "#d7b19e",
                ">55 Deg. F. / 2 - 3": "#ffffff",  // cross-hatch
                ">55 Deg. F. / 3 - 6": "#ffffff",  // cross-hatch #}
                "0 - 5 Deg. F. / < 2": "#007370",
                "0 - 5 Deg. F. / 12 - 30": "#c6e7dc",
                "0 - 5 Deg. F. / 2 - 3": "#029b98",
                "0 - 5 Deg. F. / 3 - 6": "#59c39d",
                "0 - 5 Deg. F. / 6 - 12": "#8cd2c7",
                "10 - 15 Deg. F. / < 2": "#314c21",
                "10 - 15 Deg. F. / 12 - 30": "#d6eab9",
                "10 - 15 Deg. F. / 2 - 3": "#3a8e40",
                "10 - 15 Deg. F. / 3 - 6": "#69a042",
                "10 - 15 Deg. F. / 6 - 12": "#aed463",
                "15 - 20 Deg. F. / < 2": "#73164d",
                "15 - 20 Deg. F. / 12 - 30": "#f3bfd5",
                "15 - 20 Deg. F. / 2 - 3": "#a61f85",
                "15 - 20 Deg. F. / 3 - 6": "#d43498",
                "15 - 20 Deg. F. / 6 - 12": "#de7bb2",
                "20 - 25 Deg. F. / < 2": "#676c2c",
                "20 - 25 Deg. F. / 12 - 30": "#e9f0bc",
                "20 - 25 Deg. F. / 2 - 3": "#99aa38",
                "20 - 25 Deg. F. / 3 - 6": "#b5d335",
                "20 - 25 Deg. F. / 6 - 12": "#d3e26d",
                "25 - 30 Deg. F. / < 2": "#734d1c",
                "25 - 30 Deg. F. / > 30": "#ffe9ad",
                "25 - 30 Deg. F. / 12 - 30": "#ffd17c",
                "25 - 30 Deg. F. / 2 - 3": "#a67028",
                "25 - 30 Deg. F. / 3 - 6": "#e79821",
                "25 - 30 Deg. F. / 6 - 12": "#ffa916",
                "30 - 35 Deg. F. / < 2": "#710d0f",
                "30 - 35 Deg. F. / > 30": "#f9bbbe",
                "30 - 35 Deg. F. / 12 - 30": "#f67a7c",
                "30 - 35 Deg. F. / 2 - 3": "#a71d1d",
                "30 - 35 Deg. F. / 3 - 6": "#e71a21",
                "30 - 35 Deg. F. / 6 - 12": "#f11f20",
                "35 - 40 Deg. F. / < 2": "#000000",
                "35 - 40 Deg. F. / > 30": "#e1e1df",
                "35 - 40 Deg. F. / 12 - 30": "#cccccc",
                "35 - 40 Deg. F. / 2 - 3": "#4d4d4d",
                "35 - 40 Deg. F. / 3 - 6": "#828282",
                "35 - 40 Deg. F. / 6 - 12": "#b3b3b3",
                "40 - 45 Deg. F. / < 2": "#4b2270",
                "40 - 45 Deg. F. / > 30": "#dbbedc",
                "40 - 45 Deg. F. / 12 - 30": "#b57bb6",
                "40 - 45 Deg. F. / 2 - 3": "#7c2e94",
                "40 - 45 Deg. F. / 3 - 6": "#894b9e",
                "40 - 45 Deg. F. / 6 - 12": "#954da1",
                "45 - 50 Deg. F. / < 2": "#4b2270",
                "45 - 50 Deg. F. / 12 - 30": "#bfe3f9",
                "45 - 50 Deg. F. / 2 - 3": "#0585ac",
                "45 - 50 Deg. F. / 3 - 6": "#00abde",
                "45 - 50 Deg. F. / 6 - 12": "#7fd4f3",
                "5 - 10 Deg. F. / < 2": "#21316d",
                "5 - 10 Deg. F. / 12 - 30": "#c1d0ed",
                "5 - 10 Deg. F. / 2 - 3": "#114da3",
                "5 - 10 Deg. F. / 3 - 6": "#3b60ae",
                "5 - 10 Deg. F. / 6 - 12": "#80acd9",
                "50 - 55 Deg. F. / 12 - 30": "#a5a835",
                "50 - 55 Deg. F. / 2 - 3": "#fef9bf",
                "50 - 55 Deg. F. / 3 - 6": "#e6e415",
                "50 - 55 Deg. F. / 6 - 12": "#babd32"
            };

            map.data.setStyle(function (feature) {
                const seedZone = feature.getProperty('seed_zone');
                return {
                    fillColor: pszColors[seedZone],
                    strokeWidth: 1,
                    strokeOpacity: 0.3
                }
            });

            map.data.addListener('click', function (event) {
                const seed_zone = event.feature.getProperty('seed_zone');
                const content = sanitizeHTML`
                      <div>
                        <h2><strong>Seed Zone</strong>: ${seed_zone}</h2>
                      </div>
                    `;

                infoWindow.setContent(content);
                infoWindow.setPosition(event.latLng);
                infoWindow.open(map);
            });
        }
    }
});

function activateWaypoints() {
    // Loop over the waypoints
    $(".waypoint").each(function () {
        const waypoint = waypointByID[$(this).find('input:first').attr('id')];
        let new_center = new google.maps.LatLng(waypoint.lat, waypoint.lng);
        const userMarker = new google.maps.Marker({map: map, position: new_center, draggable: true});
        userMarker.addListener('dragend', updateGeometry($(this), waypoint));

        $(this).click(function() {
            map.panTo(new_center);
        }).hover(
            function () {this.className = this.className.replace('OFF', 'ON');},
            function () {this.className = this.className.replace('ON', 'OFF');}
        );
    });
}

$(document).ready(function () {
    $('#address').keydown(function(e) {
        if (e.keyCode === 13) searchWaypoints();
    });

});
