
window.addEventListener("load", (event) => {
    // only show loader when site is loading
    document.querySelector('.loader-container').style.display ="none";
    // Add active class to nav-links
    const activePage = window.location.pathname;
    var general = true;
    // Not on home
    if (!(activePage === '/')) {
        document.querySelectorAll('.nav-link').forEach(link => {
        // Specify on type of oeuvre link 
        if (activePage == '/oeuvre/') {
            general = false;
        }
        if (link.href.includes(`${activePage}`) && (general == true)){
            link.classList.add('active');
        } else if (link.href.includes(`${window.location.search}`) && (general == false) ){
            link.classList.add('active');
            }
        })
    }
});