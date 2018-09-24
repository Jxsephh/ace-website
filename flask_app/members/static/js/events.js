function signup(url) {
    $.get(url).success(function(data) {
        alert(data);
    }).fail(function() {
        alert('ERROR: Could not find event.');
    });
}