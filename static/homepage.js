let slider1 = document.getElementById("radius-selection");
let output1 = document.getElementById("radius");
output1.innerHTML = slider1.value; // Display the default slider value

slider1.oninput = function() {
    output1.innerHTML = this.value;
} //end of slider value <span> number for radius slidecontainer

let slider2 = document.getElementById("trek_length_selection");
let output2 = document.getElementById("trek_length");
output2.innerHTML = slider2.value; // Display the default slider value

// Update the current slider value (each time you drag the slider handle)
slider2.oninput = function() {
    output2.innerHTML = this.value;
} //end of slider value <span> number for trail length
// REFERENCE: https://www.w3schools.com/howto/howto_js_rangeslider.asp

// $(document).on('click', '#getdirxns', getDirxns);
$(document).on('click', '#chosentrek', getTrek);
// Because button does not exist when the page loads!!!

$('#asynchronousClick').on('click', getTrails); // Trail Selector
// When button clicked, trail selected and more information displayed.

function getTrek(evt) {
  console.log("***In getTrek function!***");
  console.log($('#chosentrek').data('trailId'));
  $.post('/trek', {'chosentrail' : $('#chosentrek').data('trailId')}, function(result) {
      console.log(result);
    })
} //end of getTrek function


function getTrails(evt) {

      console.log($('#trailSelector').serialize());
			$.ajax({
				url: "/trails_asychronous",
				type: "POST",
				data: $('#trailSelector').serialize(),
				processData: false,
				success: function(response) {
            $(".error-message").hide();
            $("#map").show();
						initMap(response);
					}, // Calling initMap function to display Google Map
				 // end of response function
			  error: function(error) {
					console.log(error);
			  } // end of error handling function
      }); // end of AJAX deets section



function initMap(input) {
		let trailLong = input[0].city_long;
		let trailLat = input[0].city_lat;
		let infoWindow = new google.maps.InfoWindow({
        width: 150
		});
		let html;
	  let location = {lat: trailLat, lng: trailLong}; //latitude and longitude for city
	  let map = new google.maps.Map(document.getElementById('map'), {
	    zoom: 10,
	    center: location,
      mapTypeId: 'satellite'
		}); // end of jQuery statement

	  let marker = new google.maps.Marker({
	    position: location,
	    map: map
		}); // end of marker statement
		let trailMarker; // adding marker as a variable in the namespace

		for (let j = 0; j < input.length; j += 1) {
			trailMarker = new google.maps.Marker({
			position: new google.maps.LatLng(input[j].latitude, input[j].longitude),
			map: map,
			title: 'Trail: ' + input[j].name,
			icon: '/static/img/hikingIcon.png',
			animation: google.maps.Animation.DROP,
			});
			// TODO: mock input, and then maybe test to see if the input name (i.e. input[j].name ) is in the text
			html = ('<div class="window-content">' + '<br>' +
              '<p><b>Trail name: </b>' + input[j].name + '</p>' + '<p>' +
              '<p><b>Trail description: </b>' + input[j].summary + '</p>' + '<p>' +
              '<p><b>Trail length: </b>' + input[j].length +'</p><p>'+
              '<button type="button" id="chosentrek" name="chosentrek" data-trail-id='
              + input[j].id +' >Add to My Trails</button><form action="/trail/'
              +input[j].id+'" method="get" id="get-more-details"></form><button type="submit" form="get-more-details" value="Submit" style="display:inline-block">More Details</button></div>');

			bindInfoWindow(trailMarker, map, infoWindow, html);
		} // end of trailMarker for loop
		drop(input);
		toggleBounce(trailMarker);
} //end of initMap function

function drop(input) { //marker animation for REASONS
  for (let k = 0; k < input.length; k++) {
    setTimeout(function() {
    }, k * 200);
  }
} //end of drop function

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
