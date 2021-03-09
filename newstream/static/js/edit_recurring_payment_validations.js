function registerInvalidListeners() {
    recurringAmountInput = document.getElementById('id_recurring_amount')
    recurringAmountInput.addEventListener('invalid', (event) => {
        resetWhiteLoadingBtn();
    })
}
window.addEventListener('load', function () {
    // register inputs with invalid eventlisteners
    registerInvalidListeners();
});