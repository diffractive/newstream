###
# This file contains shortcut functions that will perform certain things, such as creating a subscription
# or creating a single donation, that are required by some tests, that are not necessarily testing these
# steps, or steps within them.
#

from diffractive.selenium import wait_element


def create_subscription(driver, app, data):
    """
    Creates a new user and a new subscription attached to that user
    data - user data e.g. {
        "email": test_user123@newstream.com'
        "first_name": 'Test'
        "last_name": 'User'
        "password": 'strongpwd'
        "name": 'Test User'
        "card_number": '4242424242424242'
        "card_expiry": '1133'
        "cvc": '123'
    }
    """
    app.go()
    app.link('Donation Form').click()

    # Cannot go to the signup page without setting a value into the custom amount or choosing a default from selector
    app.dropdown('id_donation_amount').select('HKD $100')
    app.dropdown('id_donation_frequency').select('Monthly')
    app.dropdown('id_payment_gateway').select('Stripe')

    # We need to first sign up with an account in order to use a user payment
    app.button('Register or Login').click()

    app.link('Continue with Email Sign up').click()

    app.input('id_email').fill(data['email'])
    app.input('id_first_name').fill(data['first_name'])
    app.input('id_last_name').fill(data['last_name'])
    app.input('id_password1').fill(data['password'])
    app.input('id_password2').fill(data['password'])
    app.button('Continue').click()

    app.button('Confirm Donation').click()

    wait_element(driver, '//input[@id="cardNumber"]')

    app.input('cardNumber').fill(data['card_number'])
    app.input('cardExpiry').fill(data['card_expiry'])
    app.input('cardCvc').fill(data['cvc'])
    app.input('billingName').fill(data['name'])
    app.button('Pay').click()
    wait_element(driver, '//h1[text()="Thank you!"]')


def create_paypal_subscription(driver, app, data):
    """
    Creates a new user and a new subscription attached to that user
    data - user data e.g. {
        "email": test_user123@newstream.com'
        "first_name": 'Test'
        "last_name": 'User'
        "password": 'strongpwd'
        "name": 'Test User'
        "card_number": '4242424242424242'
        "card_expiry": '1133'
        "cvc": '123'
    }
    """
    app.go()
    app.link('Donation Form').click()

    # Cannot go to the signup page without setting a value into the custom amount or choosing a default from selector
    app.dropdown('id_donation_amount').select('HKD $100')
    app.dropdown('id_donation_frequency').select('Monthly')
    app.dropdown('id_payment_gateway').select('PayPal')

    # We need to first sign up with an account in order to use a user payment
    app.button('Register or Login').click()

    app.link('Continue with Email Sign up').click()

    app.input('id_email').fill(data['email'])
    app.input('id_first_name').fill(data['first_name'])
    app.input('id_last_name').fill(data['last_name'])
    app.input('id_password1').fill(data['password'])
    app.input('id_password2').fill(data['password'])
    app.button('Continue').click()

    app.button('Confirm Donation').click()

    wait_element(driver, '//input[@id="username"]')
    app.link('secondary-btn').click()

    wait_element(driver, '//input[@id="card_number"]')
    app.input('card_number').fill(data['card_number'])
    app.input('card_expiry').fill(data['card_expiry'])
    app.input('cvc').fill(data['cvc'])
    app.input('primary-btn').click()

    wait_element(driver, '//input[@value="agree & subscribe"]')
    app.input('primary-btn').click()

    wait_element(driver, '//h1[text()="Thank you!"]')

def create_single_payment(driver, app, data):
    """
    Creates a user and creates a one time donation with the user. Ends at thank you page.
    data - user data e.g. {
        "email": test_user123@newstream.com'
        "first_name": 'Test'
        "last_name": 'User'
        "password": 'strongpwd'
        "name": 'Test User'
        "card_number": '4242424242424242'
        "card_expiry": '1133'
        "cvc": '123'
    }
    """
    app.go()

    app.link('Donation Form').click()

    # Cannot go to the signup page without setting a value into the custom amount or choosing a default from selector
    app.dropdown('id_donation_amount').select('HKD $100')
    app.dropdown('id_payment_gateway').select('Stripe')

    # We need to first sign up with an account in order to use a user payment
    app.button('Register or Login').click()
    app.link('Continue with Email Sign up').click()

    app.input('id_email').fill(data['email'])
    app.input('id_first_name').fill(data['first_name'])
    app.input('id_last_name').fill(data['last_name'])
    app.input('id_password1').fill(data['password'])
    app.input('id_password2').fill(data['password'])
    app.button('Continue').click()
    app.button('Confirm Donation').click()

    # Wait until redirecting finishes
    wait_element(driver, '//input[@id="cardNumber"]')

    app.input('cardNumber').fill(data['card_number'])
    app.input('cardExpiry').fill(data['card_expiry'])
    app.input('cardCvc').fill(data['cvc'])
    app.input('billingName').fill(data['name'])
    app.button('Pay').click()
    wait_element(driver, '//h1[text()="Thank you!"]')

