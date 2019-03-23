
// Toggles mobile navbar when item selected
//$('.navbar-collapse ul li a').click(function() {
//    $('.navbar-toggle:visible').click();
//});

// Set inverval between carousel transitions
$("#carousel").carousel();

// smooth scrolling for anchor links
$('a[href*="#"]')
  // Remove links that don't actually link to anything
  .not('[href="#"]')
  .not('[href="#0"]')
  .click(function(event) {
    // On-page links
    if (
      location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') 
      && 
      location.hostname == this.hostname
    ) {
      // Figure out element to scroll to
      var target = $(this.hash);
      target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
      // Does a scroll target exist?
      if (target.length) {
        // Only prevent default if animation is actually gonna happen
        event.preventDefault();
        $('html, body').animate({
          scrollTop: target.offset().top
        }, 1000, function() {
          // Callback after animation
          // Must change focus!
          var $target = $(target);
          $target.focus();
          if ($target.is(":focus")) { // Checking if the target was focused
            return false;
          } else {
            $target.attr('tabindex','-1'); // Adding tabindex for elements not focusable
            $target.focus(); // Set focus again
          };
        });
      }
    }
  });

// Fixes background jump on mobile
$(function(){

  var $w = $(window),
      $background = $('#background');

  // Fix background image jump on mobile
  if ((/Android|iPhone|iPad|iPod|BlackBerry/i).test(navigator.userAgent || navigator.vendor || window.opera)) {
    $background.css({'top': 'auto', 'bottom': 0});

    $w.resize(sizeBackground);
    sizeBackground();
  }

  function sizeBackground() {
     $background.height(screen.height);
  }
});
