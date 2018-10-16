function api_call(url) {
    $.get(url).done(function(data) {
        alert(data);
    }).fail(function(data) {
        alert('ERROR: Something went wrong.');
    });
}
$("#signup-btn, #close-btn, #reopen-btn").on("click", function() {
    $(this).prop("disabled", true);
});