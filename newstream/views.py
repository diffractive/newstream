from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.utils import translation

from donations.models import Subscription, STATUS_ACTIVE, STATUS_PROCESSING, STATUS_PAUSED
from donations.email_functions import sendAccountDeletedNotifToAdmins, sendAccountDeletedNotifToDonor
from newstream.functions import generateIDSecretHash, process_user_meta
from newstream.forms import PersonalInfoForm, DeleteAccountForm
User = get_user_model()


def maintenance(request):
    return render(request, 'maintenance.html')


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
        form = PersonalInfoForm(request.POST, user=request.user)
        if form.is_valid():
            # process meta data
            user_metas = process_user_meta(request.POST)

            # process the data in form.cleaned_data as required
            user = request.user
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.opt_in_mailing_list = form.cleaned_data['opt_in_mailing_list']
            user.language_preference = form.cleaned_data['language_preference']
            # translation.activate(user.language_preference)
            # request.LANGUAGE_CODE = translation.get_language()
            user.metas = user_metas
            user.save()
            messages.add_message(request, messages.SUCCESS,
                                 _('Personal Info Updated.'))

            response = redirect('personal-info')
            response.set_cookie(
                settings.LANGUAGE_COOKIE_NAME, user.language_preference)
            return response
    else:
        form = PersonalInfoForm(user=request.user)
    return render(request, 'profile_settings/personal_info.html', {'form': form})


@login_required
def security(request):
    return render(request, 'profile_settings/security.html')


@login_required
def advanced_settings(request):
    # check if user can delete account or not
    cannot_delete_text = _('You need to cancel all your recurring donations before you are allowed to delete your account.')
    subs = Subscription.objects.filter(user=request.user, recurring_status__in=[STATUS_ACTIVE, STATUS_PAUSED, STATUS_PROCESSING], deleted=False)
    if len(subs) > 0:
        deletable = False
    else:
        deletable = True
    return render(request, 'profile_settings/advanced_settings.html', {'deletable': deletable, 'cannot_delete_text': cannot_delete_text})


@login_required
def delete_account(request):
    if request.method == 'POST':
        form = DeleteAccountForm(request.POST)
        if form.is_valid():
            user = request.user
            # email notifications
            sendAccountDeletedNotifToAdmins(user)
            sendAccountDeletedNotifToDonor(user)

            # proceed to logout user
            # lastly, deletes the account
            logout(request)
            user.delete()
            messages.add_message(request, messages.SUCCESS,
                                 _('Your account is deleted.'))
            return redirect('/')
    else:
        form = DeleteAccountForm()
    return render(request, 'profile_settings/delete_account.html', {'form': form, 'confirm_text': DeleteAccountForm.CONFIRM_TEXT})
