from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.contrib.auth import login, logout
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
# from django.contrib.auth.forms import PasswordChangeForm
from donations.functions import sendVerificationEmail
from donations.models import Donor
from omp.functions import evTokenGenerator, generateIDSecretHash
from omp.forms import PersonalInfoForm, ChangeEmailForm, ChangePasswordForm, DeleteAccountForm
User = get_user_model()


def verify_email(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and evTokenGenerator.check_token(user, token):
        user.is_email_verified = True
        user.save()
        # in case this is an existing user changing into an existing donor's email
        # if not above case, the following linking would be redundant
        # because a fresh email verification means a linked donor already, but i'll just leave this for now
        try:
            donor = Donor.objects.get(email=user.email)
            donor.linked_user = user
            donor.save()
        except Donor.MultipleObjectsReturned as e1:
            # This must not be allowed as donors should have unique emails
            # todo: Try not to re-raise Exception?
            raise e1
        except Donor.DoesNotExist:
            # This simply means the new email isn't used by existing donors
            pass

        login(request, user)
    return render(request, 'registration/email_verified.html')


def unsubscribe(request, email, hash):
    failure = False
    try:
        user = User.objects.get(email=email)
        # check hash validity
        generated_hash = generateIDSecretHash(user.id)
        if hash == generated_hash:
            user.opt_in_mailing_list = False
            user.save()
        else:
            failure = True
    except Exception as e:
        print(str(e), flush=True)
        failure = True
    return render(request, 'unsubscription.html', {'failure': failure, 'email': email})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(
                request, 'Your password was successfully updated!')
            return redirect('security')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = ChangePasswordForm(request.user)
    return render(request, 'profile_settings/change_password.html', {
        'form': form
    })


@login_required
def change_email_address(request):
    if request.method == 'POST':
        form = ChangeEmailForm(request.POST)
        if form.is_valid():
            # process the data in form.cleaned_data as required
            user = request.user
            user.email = form.cleaned_data['email']
            user.is_email_verified = False
            user.save()
            # send the verification email
            sendVerificationEmail(request, user)
            messages.add_message(request, messages.INFO,
                                 'Verification email is resent to {}, please check your mailbox.'.format(user.email))
            return redirect('personal-info')
    else:
        form = ChangeEmailForm()
    return render(request, 'profile_settings/change_email.html', {'form': form})


@login_required
def resend_verification_email(request):
    user = request.user
    if not user.is_email_verified:
        sendVerificationEmail(request, user)
        messages.add_message(request, messages.SUCCESS,
                             'Verification email is resent to {}, please check your mailbox.'.format(user.email))
    else:
        messages.add_message(request, messages.WARNING,
                             'Your email {} is already verified.'.format(user.email))
    return redirect('personal-info')


@login_required
def personal_info(request):
    if request.method == 'POST':
        form = PersonalInfoForm(request.POST, request=request)
        if form.is_valid():
            # process the data in form.cleaned_data as required
            user = request.user
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.opt_in_mailing_list = form.cleaned_data['opt_in_mailing_list']
            user.save()
            messages.add_message(request, messages.SUCCESS,
                                 'Personal Info Updated.')
            return redirect('personal-info')
    else:
        form = PersonalInfoForm(request=request)
    return render(request, 'profile_settings/personal_info.html', {'form': form})


@login_required
def security(request):
    return render(request, 'profile_settings/security.html')


@login_required
def advanced_settings(request):
    return render(request, 'profile_settings/advanced_settings.html')


@login_required
def delete_account(request):
    if request.method == 'POST':
        form = DeleteAccountForm(request.POST)
        if form.is_valid():
            # proceed to logout user
            # then, todo: cancel all recurring payments
            # lastly, deletes the account
            user = request.user
            logout(request)
            user.delete()
            messages.add_message(request, messages.SUCCESS,
                                 'Your account is deleted.')
            return redirect('/')
    else:
        form = DeleteAccountForm()
    return render(request, 'profile_settings/delete_account.html', {'form': form, 'confirm_text': DeleteAccountForm.CONFIRM_TEXT})
