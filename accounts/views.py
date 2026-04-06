from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

def login_view(request):
    if request.method == "POST":
        user = authenticate(
            username=request.POST['username'],
            password=request.POST['password']
        )

        if user:
            login(request, user)

            if user.role == 'admin':
                return redirect('admin_dashboard')
            else:
                return redirect('manager_dashboard')

    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')