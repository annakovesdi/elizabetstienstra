
window.addEventListener("load", (event) => {
    // Add active class to nav-links
    const activePage = window.location.pathname;
    const specialPage = window.location.search;
    var general = true;
    // Not on home
    if (!(window.location.pathname === '/')) {
        document.querySelectorAll('.nav-link').forEach(link => {
        // Specify on type of oeuvre link 
        if (activePage == '/oeuvre/') {
            general = false;
        }
        if (link.href.includes(`${activePage}`) && (general == true)){
            link.classList.add('active');
        } else if (link.href.includes(`${specialPage}`) && (general == false) ){
            link.classList.add('active');
            }
        })
    }
});