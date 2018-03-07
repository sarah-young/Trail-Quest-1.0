
// Logic for submitting reviews on mytrails pages
$('.trailcompleted').click(function() {

  $.post('/submit_review', {'trail_id' : this.name,
                            'review_text' : document.getElementById((this.name+'-text')).value},
    function(result) {
      console.log(result);
    })
    let trail_id = this.name;
    console.log("In second part of function");
    $("#"+trail_id).hide();
    $("#"+trail_id+"-text").hide();
    $("#completed-"+trail_id).attr('disabled', true);
    document.getElementById("completed-"+trail_id).innerHTML = ('Trek logged!');
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
