
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

$(document).ready(function() {
    $("#growlink").click(function() {
      // disable button
      $(this).prop("hidden", true);
      $("#growlink1").prop("hidden", false)
    });
});