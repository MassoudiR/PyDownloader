// ---------Responsive-navbar-active-animation-----------
function test() {
    var tabsNewAnim = $('#navbarSupportedContent');
    var selectorNewAnim = $('#navbarSupportedContent').find('li').length;
    var activeItemNewAnim = tabsNewAnim.find('.active');
    var activeWidthNewAnimHeight = activeItemNewAnim.innerHeight();
    var activeWidthNewAnimWidth = activeItemNewAnim.innerWidth();
    var itemPosNewAnimTop = activeItemNewAnim.position();
    var itemPosNewAnimLeft = activeItemNewAnim.position();
    $(".hori-selector").css({
        "top": itemPosNewAnimTop.top + "px",
        "left": itemPosNewAnimLeft.left + "px",
        "height": activeWidthNewAnimHeight + "px",
        "width": activeWidthNewAnimWidth + "px"
    });

    $("#navbarSupportedContent").on("click", "li", function(e) {
        $('#navbarSupportedContent ul li').removeClass("active");
        $(this).addClass('active');
        var activeWidthNewAnimHeight = $(this).innerHeight();
        var activeWidthNewAnimWidth = $(this).innerWidth();
        var itemPosNewAnimTop = $(this).position();
        var itemPosNewAnimLeft = $(this).position();
        $(".hori-selector").css({
            "top": itemPosNewAnimTop.top + "px",
            "left": itemPosNewAnimLeft.left + "px",
            "height": activeWidthNewAnimHeight + "px",
            "width": activeWidthNewAnimWidth + "px"
        });

    });
}
$(document).ready(function() {
    setTimeout(function() {
        test();
    });
});
$(window).on('resize', function() {
    setTimeout(function() {
        test();
    }, 500);
});
$(".navbar-toggler").click(function() {
    $(".navbar-collapse").slideToggle(300);
    setTimeout(function() {
        test();
    });
});



// --------------add active class-on another-page move----------
jQuery(document).ready(function($) {
    // Get current path and find target link
    var path = window.location.pathname.split("/").pop();

    // Account for home page with empty path
    if (path == '') {
        path = 'index.html';
    }

    var target = $('#navbarSupportedContent ul li a[href="' + path + '"]');
    // Add active class to target link
    target.parent().addClass('active');
});




// Add active class on another page linked
// ==========================================
// $(window).on('load',function () {
//     var current = location.pathname;
//     console.log(current);
//     $('#navbarSupportedContent ul li a').each(function(){
//         var $this = $(this);
//         // if the current path is like this link, make it active
//         if($this.attr('href').indexOf(current) !== -1){
//             $this.parent().addClass('active');
//             $this.parents('.menu-submenu').addClass('show-dropdown');
//             $this.parents('.menu-submenu').parent().addClass('active');
//         }else{
//             $this.parent().removeClass('active');
//         }
//     })
// });
//# sourceURL=pen.js


// Icon Switch

const url = document.getElementById('url');
const icon = document.getElementById('icon');


const inputHandler = function(e) {
    icon.src = "icon/load.png"

    var tmp = document.createElement('a');
    tmp.href = e.target.value;
    domainName = tmp.hostname;
    var iconImage

    if (domainName.includes("youtu")) {
        iconImage = "icon/youtube.png"

    } else if (domainName.includes("facebook")) {
        iconImage = "icon/facebook.png"

    } else if (domainName.includes("insta")) {
        iconImage = "icon/instagram.png"

    } else if (domainName.includes("twitter")) {
        iconImage = "icon/twitter.png"

    } else if (domainName.includes("tiktok")) {
        iconImage = "icon/tiktok.png"

    } else if (domainName.includes("linked")) {
        iconImage = "icon/linkedin.png"

    } else {
        iconImage = "icon/web.png"

    }
    icon.src = iconImage;


}

url.addEventListener('input', inputHandler);
url.addEventListener('propertychange', inputHandler);


function removevideo(e) {
    $(e).parent('.imgbox').parent('.video-item').addClass("fadeout")
    setTimeout(function() {
        $(e).parent('.imgbox').parent('.video-item').remove();
    }, 2000);

}