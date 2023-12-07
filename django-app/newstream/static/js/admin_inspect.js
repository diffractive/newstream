window.onload = () => {
    (($) => {
        var firstTab = $('.tab-nav li a').first();
        if (firstTab) {
            setTimeout(() => $(firstTab).show(), 10);
            window.history.replaceState(null, null, $(firstTab).attr('href'));
        }
    })(window.jQuery)
}
