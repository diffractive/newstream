from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.contrib.auth import login
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from omp.functions import evTokenGenerator
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
        login(request, user)
    return render(request, 'registration/email_verified.html')
