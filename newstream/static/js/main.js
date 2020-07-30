// Close the popup menus if click elsewhere
window.addEventListener("click", function () {
    //Hide the menus if visible
    for (ckbox of document.getElementsByClassName("dropdown-toggle-checkbox")) {
        ckbox.checked = false;
    }
});
for (wrapper of document.getElementsByClassName("dropdown-div-wrapper")) {
    wrapper.addEventListener("click", function (event) {
        event.stopPropagation();
    });
}
for (wrapper of document.getElementsByClassName("dropdown-toggle-label")) {
    wrapper.addEventListener("click", function (event) {
        // such that other toggled popup menus can be hidden
        for (ckbox of document.getElementsByClassName("dropdown-toggle-checkbox")) {
            if (ckbox.id != this.previousElementSibling.id) {
                ckbox.checked = false;
            }
        }
    });
}

// Hide the messages after 3 seconds
(() => {
    setTimeout(() => {
        for (msg of document.getElementsByClassName('messages')) {
            msg.classList.add('opacity-0');
        }
    }, 3000);
    setTimeout(() => {
        for (msg of document.getElementsByClassName('messages')) {
            msg.classList.add('hidden');
        }
    }, 4000); // invisible transition is 1s
})();

function pushContentDownFromHeader() {
    // calculate drop distance for content below fixed header
    headerHeight = document.getElementById('newstream-topnav').offsetHeight;
    document.getElementById('base-content-wrapper').style.paddingTop = headerHeight + 'px';
}
window.addEventListener('load', function () {
    // mobile hamburger toggle function
    var hamburger_anchor = document.getElementById('nav-toggle');
    hamburger_anchor.addEventListener('click', function (e) {
        let el = document.getElementById('nav-toggle');
        let mobile_nav = document.getElementById('newstream-mobile-mainmenu');

        el.classList.toggle('menu-open');
        mobile_nav.classList.toggle('hidden');
    })
    pushContentDownFromHeader();
});
window.addEventListener('resize', function () {
    pushContentDownFromHeader();
});