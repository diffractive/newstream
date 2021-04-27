window.onload = () => {
    (($) => {
        $(document).on('change', '.is-default-amount-step input', function() {
            $(".is-default-amount-step input").not(this).prop('checked', false);
        });
    })(window.jQuery)
}