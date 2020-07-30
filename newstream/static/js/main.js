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
function resizeVideoIframe() {
    // Resizing JS for responsive video iframe block
    // Vanilla version of FitVids
    // Still licencened under WTFPL
    //
    // Not as robust and fault tolerant as the jQuery version.
    // It's BYOCSS.
    (function (window, document, undefined) {
        "use strict";

        // List of Video Vendors embeds you want to support
        var players = ['iframe[src*="youtube.com"]', 'iframe[src*="vimeo.com"]'];

        // Select videos
        var fitVids = document.querySelectorAll(players.join(","));

        // If there are videos on the page...
        if (fitVids.length) {
            // Loop through videos
            for (var i = 0; i < fitVids.length; i++) {
                // Get Video Information
                var fitVid = fitVids[i];
                var width = parseFloat(fitVid.getAttribute("width"));
                var height = parseFloat(fitVid.getAttribute("height"));
                var aspectRatio = height / width;
                var parentDiv = fitVid.parentNode;
                var containerWidth = parentDiv.parentNode.offsetWidth; // get at container-row
                // Calculate aspectRatio and maxWidth
                if (width < containerWidth) {
                    parentDiv.style.paddingBottom = height + 'px';
                    parentDiv.style.maxWidth = width + 'px';
                } else {
                    parentDiv.style.paddingBottom = aspectRatio * 100 + "%";
                    parentDiv.style.maxWidth = containerWidth + 'px';
                }
            }
        }
    })(window, document);
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

    // resize video iframes: currently just support youtube and vimeo
    resizeVideoIframe();
});
window.addEventListener('resize', function () {
    pushContentDownFromHeader();
    resizeVideoIframe();
});