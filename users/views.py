from django.shortcuts import render,redirect
from .models import CustomUser
from django.contrib import messages
from .forms import SignUpForm
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetView,PasswordResetConfirmView
from django.core.mail import send_mail
from .tokens import account_activation_token

def activeEmail(request, user, to_email):
    context={
        'user':user,
        'domain':get_current_site(request).domain,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token':account_activation_token.make_token(user),
        'protocol':'https' if request.is_secure() else 'http'
    }
    email_content=render_to_string('users/acct_active_email.html', + context)

def signup(request):
    if request.method == 'POST':
        form=SignUpForm(request.POST)
        if form.is_valid():
            email=form.cleaned_data.get('email')
            if CustomUser.objects.filter(email=email).exists():
                messages.error(request, "This email is laready registered, Please use a diffrent email.")
            else:
                user=form.save(commit=False)
                user.is_active=False
                user.save()
                activeEmail(request, user, email)
                messages.success(request, f"New account created: Please check your email to activate your account")
                return redirect('/')
            
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    
    else:
        form=SignUpForm()
    return render(request, 'users/register.html', {'form':form})
            
