
function clickToggleDropdown(elementId) {
    var e = document.getElementById(elementId);
    if (e.className.indexOf("w3-show") == -1){
        e.className += " w3-show";
    }
    else{
        e.className = e.className.replace(" w3-show", "");
    }
}
