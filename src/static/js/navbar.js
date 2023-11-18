window.addEventListener('load', function() {
    var hamburgerMenunav = document.getElementById('hamburger-menunav');
    var navbar = document.getElementsByClassName('listanav')[0];
    var navbarreal = document.getElementById('navbar');
    hamburgerMenunav.addEventListener('click', function() {
        navbar.classList.toggle('expanded');
        hamburgerMenunav.classList.toggle('change');
        navbarreal.classList.toggle('expanded');
        // navbarreal.style.height = "150px";
        // navbarreal.style.overflow = "visible";
    });

    document.addEventListener('click', function(event) {
        if (!navbar.contains(event.target) && !hamburgerMenunav.contains(event.target)) {
            navbar.classList.remove('expanded');
            navbarreal.classList.remove('expanded');
            hamburgerMenunav.classList.remove('change');
            navbarreal.style.height = "";
            navbarreal.style.overflow = "";
        }
    });          
});