// JavaScript
window.onload = function() {
    var hamburgerMenu = document.getElementById('hamburger-menu');
    var sidebar = document.getElementById('sidebar');
    var links = sidebar.getElementsByTagName('a');
    hamburgerMenu.addEventListener('click', function() {
        // In the event handler, toggle the 'expanded' class on the sidebar
        sidebar.classList.toggle('expanded');
        hamburgerMenu.classList.toggle('change');
    });
    // Add a click event listener to the document
    for (var i = 0; i < links.length; i++) {
        links[i].addEventListener('click', function() {
            // In the event handler, remove the 'expanded' class from the sidebar
            sidebar.classList.remove('expanded');
        });
    } // This closing brace was missing

    document.addEventListener('click', function(event) {
        // Check if the click event's target is not the sidebar and not the hamburger menu
        if (!sidebar.contains(event.target) && !hamburgerMenu.contains(event.target)) {
            // If the condition is true, remove the 'expanded' class from the sidebar
            sidebar.classList.remove('expanded');
        }
    });          
}