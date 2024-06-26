from django.shortcuts import render,redirect
from .models import CustomUser
from django.contrib import messages
from .forms import SignUpForm
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
            
