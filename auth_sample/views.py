from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from . import forms
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from . import tokens

def signup(request):
	if request.method == 'POST':
		form = forms.SignUpForm(request.POST)
		if form.is_valid():
			user = form.save()
			user.refresh_from_db()
			user.profile.birth_date = form.cleaned_data.get('birth_date')
			user.profile.about = form.cleaned_data.get('about')
			user.save()
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password1')
			user  = authenticate(username = username, password = password)
			login(request, user)
			return redirect('home')
	else:
		form = forms.SignUpForm()
	return render(request, 'signup.html', {'form':form})

def home(request):
	return render(request, 'home.html')

def signup_with_email_verification(request):
	form = forms.SignUpForm()
	if request.method == 'POST':
		form = forms.SignUpForm(request.POST)
        if form.is_valid():
        	user = form.save(commit = False)
        	user.is_active = False
        	user.save()
        	current_site = get_current_site(request)
        	subject = 'Activate Your Mysite Account'
        	message = render_to_string('account_activation_email.html',{
        		'user': user,
        		'domain': current_site.domain,
        		'uid': urlsafe_base64_encode(force_bytes(user.id)),
        		'token': tokens.account_activation_token.make_token(user),
        		})
        	user.email_user(subject, message)
        	return redirect('account_activation_sent')
 	return render(request, 'signup.html', {'form': form})	

def account_activation_sent(request):
    return render(request, 'account_activation_sent.html')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and tokens.account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirm= True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'account_activation_invalid.html')