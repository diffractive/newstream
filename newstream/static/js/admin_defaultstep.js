window.onload = () => {
    (($) => {
        $(".is-default-amount-step input").change(function() {
            $(".is-default-amount-step input").not(this).prop('checked', false);
        });
    })(window.jQuery)
}