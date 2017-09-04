from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from . import forms
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from . import tokens
from django.db import transaction

User = get_user_model()

def home(request):
    return render(request, 'home.html', context={'request': request})

@transaction.atomic()
def signup_with_email_verification(request):
    form = forms.SignUpForm()
    if request.method == 'POST':
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.email = form.cleaned_data.get('email', None)
            user.first_name = form.cleaned_data.get('first_name', None)
            user.last_name = form.cleaned_data.get('last_name', None)
            user.username = form.cleaned_data.get('username', None)

            user.contact_no = form.cleaned_data.get('contact_no', None)
            user.save()

            current_site = get_current_site(request)
            subject = 'Activate Your Mysite Account'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.id)),
                'token': tokens.account_activation_token.make_token(user),
            })
            user.email_user(subject, message)

            return redirect('account_activation_sent')
    return render(request, 'signup.html', {'request': request, 'form': form})


def account_activation_sent(request):
    return render(request, 'account_activation_sent.html', context={'request': request})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and tokens.account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'account_activation_invalid.html', context={'request': request})

def change_password(request):

    form = forms.ChangePasswordForm(user=request.user)
    if request.method == 'POST':
        form = forms.ChangePasswordForm(request.POST)
        print(form.is_valid())
        print(form.errors)
        if form.is_valid():
            form.save()
            return render(request, 'password_updated.html')
    return render(request, 'change_password.html', {'form': form})


def view_profile(request, user_id):

    return render(request, 'profile.html', {'request': request})
