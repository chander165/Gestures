var myIndex = 0;
carousel();

function carousel() {
    var i;
    var x = document.getElementsByClassName("mySlides");
    for (i = 0; i < x.length; i++) {
       x[i].style.display = "none";  
    }
    myIndex++;
    if (myIndex > x.length) {myIndex = 1}    
    x[myIndex-1].style.display = "block";  
    setTimeout(carousel, 4000);    
}
function myFunction() {
    var x = document.getElementById("navDemo");
    if (x.className.indexOf("w3-show") == -1) {
        x.className += " w3-show";
    } else { 
        x.className = x.className.replace(" w3-show", "");
    }
};

var canvas = document.getElementById('canvas');
var context = document.getContext('2d');
var video = document.getElementById('video');
document.getElementById("snap").addEventListener('click', function(){
    
})
// When the user clicks anywhere outside of the modal, close it
// var modal = document.getElementById('ticketModal');
// window.onclick = function(event) {
//   if (event.target == modal) {
//     modal.style.display = "none";
//   }
// };

// function myMap() {
//   myCenter=new google.maps.LatLng(430.2672, -97.7431);
//   var mapOptions= {
//     center:myCenter,
//     zoom:12, scrollwheel: false, draggable: false,
//     mapTypeId:google.maps.MapTypeId.ROADMAP
//   };
//   var map=new google.maps.Map(document.getElementById("googleMap"),mapOptions);

//   var marker = new google.maps.Marker({
//     position: myCenter,
//   });
//   marker.setMap(map);
// }

// tableau graph for the studies page
// var divElement = document.getElementById('viz1531268821426');
// var vizElement = document.getElementsByTagName('object')[0];                    
//   vizElement.style.minWidth='620px';
//   vizElement.style.maxWidth='1250px';
//   vizElement.style.width='100%';
//   vizElement.style.minHeight='587px';
//   vizElement.style.maxHeight='887px';
//   vizElement.style.height=(divElement.offsetWidth*0.75)+'px';                    
// var scriptElement = document.createElement('script');                    
//   scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    
//   vizElement.parentNode.insertBefore(scriptElement, vizElement);                
