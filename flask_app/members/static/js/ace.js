
// Toggles mobile navbar when item selected
//$('.navbar-collapse ul li a').click(function() {
//    $('.navbar-toggle:visible').click();
//});

// Set inverval between carousel transitions
//  $('.carousel').carousel({
//    interval: 1000*6
//  });

// Smooth scrolling on anchor links
$("nav a[href^='#']").on('click', function(e) {
   // prevent default anchor click behavior
   e.preventDefault();
   // store hash
   var hash = this.hash;
   // animate
   $('html, body').animate({
       scrollTop: $(hash).offset().top
     }, 500, function(){
       // when done, add hash to url
       // (default click behaviour)
       window.location.hash = hash;
     });

});

// Active navbar link based on scroll location

// Cache selectors
var topMenu = $(".navbar-default"),
    topMenuHeight = topMenu.outerHeight()+15,
    // All list items
    menuItems = topMenu.find('a[href^="#"]'),
    // Anchors corresponding to menu items
    scrollItems = menuItems.map(function(){
      var item = $($(this).attr("href"));
      if (item.length) { return item; }
    });

// Bind to scroll
$(window).scroll(function(){
   // Get container scroll position
   var fromTop = $(this).scrollTop()+topMenuHeight; // +100;

   // Get id of current scroll item
   var cur = scrollItems.map(function(){
     if ($(this).offset().top < fromTop)
       return this;
   });
   // Get the id of the current element
   cur = cur[cur.length-1];
   var id = cur && cur.length ? cur[0].id : "";
   // Set/remove active class
   menuItems
     .parent().removeClass("active")
     .end().filter("[href='#"+id+"']").parent().addClass("active");
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
