// JS file supporting mytrails!

// Create event listener for marking trail as complete.
// Send information to backend for processing:
// > Add to database by modifying current record: http://fellowship.hackbrightacademy.com/materials/f21a/lectures/sql-2/
// > Process trail badge logic

$('.trailcompleted').click(function() {

  $.post('/submit_review', {'trail_id' : this.name,
                            'review_text' : document.getElementById((this.name+'-text')).value},
    function(result) {
      console.log(result);
    })
    let trail_id = this.name;
    $("#div-"+trail_id).removeClass("trek-details");
    $("#div-"+trail_id).addClass("review-trails");
    $("#"+trail_id+"-text").hide();
});

$('.removetrail').click(function() {
   console.log('banana');
  $.post('/remove_trail', {'trail_id' : this.name },

    function(result) {
      console.log(result);
    });
    let trail_id = this.name;
    $("#div-"+trail_id).remove();

            });







// Set up jquery onClick event on the button that has the name of the trail_id
// save this.id to a variable
// append that to "div-" to reference the div by id
// change the visibility setting on the div
