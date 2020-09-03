function modal(){
    var modal = document.getElementById("myModal");

// Get the button that opens the modal
    var btn = document.getElementById("myBtn");

// Get the <span> element that closes the modal
    var span = document.getElementsByClassName("close")[0];

// When the user clicks on the button, open the modal
   
    modal.style.display = "block";
    modal.style.width = "650px";
    modal.style.height = "200px"
    modal.style.overflowY = "auto";
    modal.style.textAlign = "center";  
    modal.style.backgroundColor = "white";
    modal.style.borderRadius = "10px";
    modal.style.padding = "25px";
    modal.style.fontSize = "15px";
  



// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
} 
}