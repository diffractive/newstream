window.onload = () => {
    (($) => {
        var firstTab = $('.tab-nav li a').first();
        if (firstTab) {
            setTimeout(() => firstTab.tab('show'), 10);
            window.history.replaceState(null, null, $(firstTab).attr('href'));
        }
    })(window.jQuery)
}