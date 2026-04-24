from django.shortcuts import render, redirect
from .forms import UserRegisterForm

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            return render(request, 'users/account_inactive.html')
    else:
        form = UserRegisterForm()
        
    return render (request, 'users/register.html', {'form': form})