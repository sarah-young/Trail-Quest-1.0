
// Logic for submitting reviews on mytrails pages
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

// Logic to remove trail from mytrails page
$('.removetrail').click(function() {
   console.log('banana');
  $.post('/remove_trail', {'trail_id' : this.name },

    function(result) {
      console.log(result);
    });
    let trail_id = this.name;
    $("#div-"+trail_id).remove();

            });
