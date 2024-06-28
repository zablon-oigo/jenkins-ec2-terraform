from django.shortcuts import render,redirect
from .models import CustomUser
from django.contrib import messages,auth
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
from django.contrib.auth import get_user_model
User=get_user_model()

def activate(request, uidb64, token):
    User=auth.get_user_model()
    try:
        uid=force_str(urlsafe_base64_decode(uidb64))
        user=User.objects.get(pk=uid)
    
    except:
        user=None
    
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active=True
        user.save()
        messages.success(
            request,
            'Thank you for your email confirmation. Now you can login !'
        )
        return redirect('login')
    else:
        messages.error(request, 'Activation Link is Invalid!')
    
    return redirect('index')
    


def activeEmail(request, user, to_email):
    context={
        'user':user,
        'domain':get_current_site(request).domain,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token':account_activation_token.make_token(user),
        'protocol':'https' if request.is_secure() else 'http'
    }
    email_content=render_to_string('users/acct_active_email.html',context)
    email_subject='Activate your account.'
    recipient_list=[to_email]
    from_email=''
    success=send_mail(
        email_subject,
        '',
        from_email,
        recipient_list,
        html_message=email_content,
        fail_silently=False

    )
    if success > 0:
        messages.success(
            request,
            f"Dear {user}, Please go to your email '{to_email}' inbox and click on"
            f"check your activation to confirm and complete the registration"
        )
    else:
        messages.error(request, f"There was a problem sending email to {to_email}, please make sure your email was spelt correctly.")

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
            
def send_custom_password_reset_email(user, uid, token, protocol,domain):
    subject='Password Reset'
    from_email=''
    to_email=user.email

    context={
        'name':user,
        'uid':uid,
        'token':token,
        'protocol':protocol,
        'domain':domain
    }
    html_content=render_to_string('users/password_reset_email.html',context)

    msg=send_mail(
        subject,html_content,from_email,[to_email]
    )