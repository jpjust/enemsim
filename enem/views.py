from MySQLdb import IntegrityError
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Root view
def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')

# Log in
def login_user(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'GET':
        return render(request, 'login.html')
    
    if request.method == 'POST':
        data = request.POST

        # Authenticate user
        user = authenticate(request, username=data['email'], password=data['pwd'])

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        
        else:
            return render(request, 'login.html', {
                'data': data,
                'error_message': 'Erro de autenticação.'
            })

# Log out
@login_required
def logout_user(request):
    logout(request)
    return redirect('index')

# Sign up
def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    
    if request.method == 'POST':
        data = request.POST

        # Check all fields
        if not data['first_name'] or not data['last_name'] or not data['email'] \
           or not data['school'] or not data['pwd1'] or not data['pwd2']:
            return render(request, 'signup.html', {
                'data': data,
                'error_message': 'Todos os campos precisam ser preenchidos.'
            })
        
        # Check passwords
        if data['pwd1'] != data['pwd2']:
            return render(request, 'signup.html', {
                'data': data,
                'error_message': 'As senhas digitadas não coincidem.'
            })
        
        # Form data is OK
        try:
            user = User.objects.create_user(
                username=data['email'],
                email=data['email'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                password=data['pwd1']
            )
            user.save()
        except IntegrityError:
            return render(request, 'signup.html', {
                'data': data,
                'error_message': 'O e-mail fornecido já está cadastrado.'
            })

        return render(request, 'login.html', {
            'info_message': 'Cadastro efetuado com sucesso!'
        })

# Dashboard
@login_required
def dashboard(request):
    return render(request, 'dashboard.html')
