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