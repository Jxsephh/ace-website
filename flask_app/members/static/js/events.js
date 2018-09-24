function signup(url) {
    $.get(url).done(function(data) {
        alert(data);
    }).fail(function() {
        alert('ERROR: Could not find event.');
    });
}