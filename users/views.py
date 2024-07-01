from django.shortcuts import render,redirect
from .models import CustomUser
from django.contrib import messages,auth
from .forms import SignUpForm,LoginForm
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetView,PasswordResetConfirmView
from django.core.mail import send_mail,EmailMessage
from .tokens import account_activation_token
from django.contrib.auth import get_user_model,authenticate,login,logout
User=get_user_model()
from django.http import HttpResponse
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
            
def send_custom_password_reset_email(request,user):
    context={
        'name':user,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token':default_token_generator.make_token(user),
        'protocol':'https' if  request.is_secure() else 'http',
        'domain':get_current_site(request).domain
    }
    subject='Password Reset'
    from_email=''
    to_email=user.email
    email_content=render_to_string('users/password_reset_email.html',context)

    msg=EmailMessage(
        subject,email_content,from_email,to_email
    )
    msg.content_subtype='html'
    msg.send()
class CustomPasswordResetView(PasswordResetView):
    template_name='users/password_reset_form.html'
    email_template_name='users/password/reset_email.html'
    
    def form_valid(self, form):
        response=super().form_valid(form)
        users=list(form.get_users(form.cleaned_data['email']))
        user=users[0]  if users else None
        if  user:
            uidb64=urlsafe_base64_encode(force_bytes(user.pk))
            token=default_token_generator.make_token(user)
            protocol='https' if  self.request.is_secure() else  'http'
            send_custom_password_reset_email(user,uidb64,token , protocol,domain=self.request.get_host())
            return response
        

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name='users/password_reset_confirm.html'

    def get_context_data(self, **kwargs):
       context=super().get_context_data(**kwargs)
       context['uidb64']=self.kwargs['uidb64']
       context['token']=self.kwargs['token']
       return context
    
    def form_valid(self,form):
        form.save()
        messages.success(self.request, 'Your password has been reset successfully.')
        return super().form_valid(form)
    
def custom_login(request):
    if request.method == "POST":
        form=LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request,email=email,password=password)
            if user:
                login(request, user)
                messages.success(request,'login was successfully')
                return redirect('index')

def custom_logout(request):
    logout(request)
    messages.success(request,f'You have been logged out.')
    return redirect('login')  


def index(request):
    return HttpResponse("Hello World!")