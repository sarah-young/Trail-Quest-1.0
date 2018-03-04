





function initMap2() {

  let trailheadLat = parseFloat(document.getElementById('trailheadlat').value);
  console.log(trailheadLat);
  let trailheadLong = parseFloat(document.getElementById('trailheadlong').value);
  console.log(trailheadLong);
  let trailId = document.getElementById('trailid')
  let infoWindow = new google.maps.InfoWindow({
    width: 150
  });
  let html;
  let location = {lat: trailheadLat, lng: trailheadLong};
  let map = new google.maps.Map(document.getElementById('map'), {
    zoom: 20,
    center: location,
    mapTypeId: 'satellite'
    // mapTypeId: 'terrain'
  }); // end of jQuery statement

  // let marker = new google.maps.Marker({ //NOTE: Leaving this out for now. Only trailheadMarker is needed at this time.
  //   position: location,
  //   map: map
  // }); // end of marker statement
    // markerPlacement(input); NOTE: Does not seem to be needed.
  let trailheadMarker; // adding marker as a variable in the namespace
  trailheadMarker = new google.maps.Marker({
  position: new google.maps.LatLng(trailheadLat, trailheadLong),
  map: map,
  title: 'Selected Trek',
  icon: '/static/img/hikingIcon.png',
  animation: google.maps.Animation.DROP,
  });
    // TODO: mock input, and then maybe test to see if the input name (i.e. input[j].name ) is in the text
  html = ('<div class="window-content"><input type="text" id="origin" placeholder="Starting Address"><br><input type="text" id="phonenumber" placeholder="Enter your phone number"><br><button type="button" id="getdirxns" name="'+trailId+'">Text Directions Link to Trailhead</button ></div>');
  // sent to the backend where a google maps api is called and trail info and a link to dirxns is sent to phone!


  bindInfoWindow(trailheadMarker, map, infoWindow, html);
  toggleBounce(trailheadMarker);
} //end of initMap2 function

function toggleBounce(trailMarker) { //cute BOUNCE when markers drop <3
	if (trailMarker.getAnimation() !== null) {
		trailMarker.setAnimation(null);
	} //end of if
	else {
		trailMarker.setAnimation(google.maps.Animation.BOUNCE);
	} //end of else
} //end of toggleBounce function

function bindInfoWindow(trailMarker, map, infoWindow, html) {
        google.maps.event.addListener(trailMarker, 'click', function () {
            infoWindow.close();
            infoWindow.setContent(html);
            infoWindow.open(map, trailMarker);
        });
} //end of bindInfoWindow function

initMap2()

$(document).on('click', '#trailid-add', function() {
  console.log(document.getElementById('trailid').value);
  $.post('/trek', {'chosentrail' : document.getElementById('trailid').value },

  function(result) {
    console.log(result);
  })
});

$(document).on('click', '#getdirxns', function(){
  let lat = document.getElementById('trailheadlat').value
  let lng = document.getElementById('trailheadlong').value

  $.post('/directions', {'trail_id' : this.name,
                         'origin' : document.getElementById('origin').value,
                         'destination' : lat+','+lng,
                         'phone_number' : document.getElementById('phonenumber').value,
                         'trail_name' : document.getElementById("trail_name").value},
    function(result) {
      console.log(result);
      // showTrek(result);
    })
});



function getDirxns() {
  console.log("getdirxns button working!!!");
  if (document.getElementById("startingaddress").value === "") {
    alert("Please enter a valid address.");
    console.log('In alert function');

  } // end of if statement
  else {
    console.log(document.getElementById("startingaddress").value);
    console.log(document.getElementById("trailhead_coordinates").value);
    $.post('/dirxns', {'startingaddress' : document.getElementById("startingaddress").value,
                       'startingcity' : document.getElementById('startingcity').value,
                       'startingstate': document.getElementById('startingstate').value,
                       'trailhead_coordinates': document.getElementById("trailhead_coordinates").value,
                       'trail_name' : document.getElementById("trail_name").value },
      function(result) {
      console.log(result);
    }) //end of post statement

  } //end of else statement


} // end of getDirxns function
