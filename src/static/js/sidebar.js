window.addEventListener ('load', function() {
    var hamburgerMenu = document.getElementById('hamburger-menu');
    var sidebar = document.getElementById('sidebar');
    var links = sidebar.getElementsByTagName('a');
    hamburgerMenu.addEventListener('click', function() {
        sidebar.classList.toggle('expanded');
        hamburgerMenu.classList.toggle('change');
    });
    for (var i = 0; i < links.length; i++) {
        links[i].addEventListener('click', function() {
            sidebar.classList.remove('expanded');
        });
    }

    document.addEventListener('click', function(event) {
        if (!sidebar.contains(event.target) && !hamburgerMenu.contains(event.target)) {
            sidebar.classList.remove('expanded');
            hamburgerMenu.classList.remove('change');
        }
    });          
});