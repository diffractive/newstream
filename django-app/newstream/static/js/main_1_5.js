// Common functions
function toggleSidenav() {
    document.body.classList.toggle('sidenav-active');
    document.body.classList.toggle('noscroll');
}
function escapeHtml(unsafe) {
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Close the popup menus if click elsewhere
// We convert these query lists to Arrays for the sake of compatibility with older browsers
window.addEventListener("click", function () {
    //Hide the menus if visible
    for (let ckbox of Array.from(document.getElementsByClassName("dropdown-toggle-checkbox"))) {
        ckbox.checked = false;
    }
});
for (let wrapper of Array.from(document.getElementsByClassName("dropdown-div-wrapper"))) {
    wrapper.addEventListener("click", function (event) {
        event.stopPropagation();
    });
}
for (let wrapper of Array.from(document.getElementsByClassName("dropdown-toggle-label"))) {
    wrapper.addEventListener("click", function (event) {
        // such that other toggled popup menus can be hidden
        for (ckbox of Array.from(document.getElementsByClassName("dropdown-toggle-checkbox"))) {
            if (ckbox.id != this.previousElementSibling.id) {
                ckbox.checked = false;
            }
        }
    });
}

// Hide the messages after 3 seconds
// We convert these query lists to Arrays for the sake of compatibility with older browsers
(() => {
    setTimeout(() => {
        for (let msg of Array.from(document.querySelectorAll('.message:not(.static-notif)'))) {
            msg.classList.add('opacity-0');
        }
    }, 3000);
    setTimeout(() => {
        for (let msg of Array.from(document.querySelectorAll('.message:not(.static-notif)'))) {
            msg.classList.add('out-of-sight');
        }
    }, 4000); // invisible transition is 1s
    setTimeout(() => {
        for (let msg of Array.from(document.querySelectorAll('.message:not(.static-notif)'))) {
            msg.classList.add('hidden');
        }
    }, 4000); // invisible transition is 1s
})();

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
// We convert these query lists to Arrays for the sake of compatibility with older browsers
function resetWhiteLoadingBtn() {
    for (let btn of Array.from(document.getElementsByClassName('need-white-loading-btn'))) {
        btn.disabled = false;
        btn.classList.remove('white-loading-btn');
    }
}
function resetBlackLoadingBtn() {
    for (let btn of Array.from(document.getElementsByClassName('need-black-loading-btn'))) {
        btn.disabled = false;
        btn.classList.remove('black-loading-btn');
    }
}
function whiteLoadingBtnEvent(event) {
    el = event.currentTarget;
    el.disabled = true;
    el.classList.add('white-loading-btn');
    // submit form
    if (el.closest('form.action-form')) {
        var submit_form = el.closest('form.action-form');
        if (el.getAttribute('name')) {
            var hidden_input = document.createElement("input");
            hidden_input.setAttribute('type', 'hidden');
            hidden_input.setAttribute('name', el.getAttribute('name'));
            hidden_input.setAttribute('value', el.getAttribute('value'));
            submit_form.appendChild(hidden_input);
        }
        submit_form.submit();
    }
}
function blackLoadingBtnEvent(event) {
    el = event.currentTarget;
    el.disabled = true;
    if (el.classList.contains('adhoc-right-pad')) {
        el.style.paddingRight = '3rem'; // reserving space for the loading gif
    }
    el.classList.add('black-loading-btn');
    // submit form
    if (el.closest('form.action-form')) {
        var submit_form = el.closest('form.action-form');
        if (el.getAttribute('name')) {
            var hidden_input = document.createElement("input");
            hidden_input.setAttribute('type', 'hidden');
            hidden_input.setAttribute('name', el.getAttribute('name'));
            hidden_input.setAttribute('value', el.getAttribute('value'));
            submit_form.appendChild(hidden_input);
        }
        submit_form.submit();
    }
}
function registerLoadingButtons() {
    // We convert these query lists to Arrays for the sake of compatibility with older browsers
    for (let btn of Array.from(document.getElementsByClassName('need-white-loading-btn'))) {
        btn.addEventListener('click', whiteLoadingBtnEvent);
    }
    for (let btn of Array.from(document.getElementsByClassName('need-black-loading-btn'))) {
        btn.addEventListener('click', blackLoadingBtnEvent);
    }
}
window.addEventListener('load', function () {
    // resize video iframes: currently just support youtube and vimeo
    resizeVideoIframe();

    // register need loading buttons eventlisteners
    registerLoadingButtons();
});
window.addEventListener('resize', function () {
    resizeVideoIframe();
});

window.addEventListener('load', function () {
    // Add toggle event listeners:
    const sidebarEls = document.querySelectorAll(".cover, #nav-toggle, #close-nav-toggle")
    for (let sidebarEl of Array.from(sidebarEls)) {
        sidebarEl.addEventListener("click", toggleSidenav)
    }
})
