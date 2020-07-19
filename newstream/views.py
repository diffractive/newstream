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
from newstream.functions import evTokenGenerator, generateIDSecretHash
from newstream.forms import PersonalInfoForm, ChangePasswordForm, DeleteAccountForm
# from allauth.account.views import SignupView
User = get_user_model()


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
            # then, mark linked donors to linked_user_deleted=True
            # then, todo: cancel all recurring payments
            # lastly, deletes the account
            user = request.user
            logout(request)
            donors = Donor.objects.filter(linked_user=user).all()
            for donor in donors:
                donor.email = 'deleted_' + str(donor.id) + '_' + donor.email
                donor.linked_user_deleted = True
                donor.linked_user = None
                donor.save()
            user.delete()
            messages.add_message(request, messages.SUCCESS,
                                 'Your account is deleted.')
            return redirect('/')
    else:
        form = DeleteAccountForm()
    return render(request, 'profile_settings/delete_account.html', {'form': form, 'confirm_text': DeleteAccountForm.CONFIRM_TEXT})
