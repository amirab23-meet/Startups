function showDiv() {
   document.getElementById('welcomeDiv').style.display = "block";
   document.getElementById('space').style.display = "block";
   document.getElementById('butt').textContent = "Hide";
   document.getElementById('butt').onclick= function(){ hideDiv(); } ;
}
function hideDiv() {
   document.getElementById('welcomeDiv').style.display = "none";
   document.getElementById('space').style.display = "none";
   document.getElementById('butt').textContent = "Add post";
   document.getElementById('butt').onclick= function(){ showDiv(); } ;
}