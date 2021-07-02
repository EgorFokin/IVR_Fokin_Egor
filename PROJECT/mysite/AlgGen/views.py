from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt

from .forms import CreateUserForm

from .problem_generator import *

from .confirmation_tokens import account_activation_token

NUMBER_OF_PROBLEMS = 5


def index(request):
    if request.user.is_authenticated:
        problem_type = request.GET.get('type')
        if not problem_type:
            problem_type = 'arithmetic'
        problems = []
        for problem_number in range(NUMBER_OF_PROBLEMS):
            if problem_type == 'arithmetic':
                problems.append(generate_arithmetic())
            if problem_type == 'linear':
                problems.append(generate_linear())
            if problem_type == 'quadratic':
                problems.append(generate_quadratic())
            if problem_type == 'system':
                problems.append(generate_system())
            if problem_type == 'replacement':
                problems.append(generate_replacement())
            if problem_type == 'derivative':
                problems.append(generate_derivative())
            if problem_type == 'inequality':
                problems.append(generate_inequality())
        context = {'problems': problems, 'problem_type': problem_type}
        return render(request, 'index.html', context)
    else:
        return redirect('login')


def registerUser(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                mail_subject = 'Активируйте ваш AlgGen аккаунт.'
                t = account_activation_token.make_token(user)
                print(t)
                message = render_to_string('registration/acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': t,
                })
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.send()
                return redirect('login')
        context = {'form': form}
        return render(request, 'registration/register.html', context)


def loginUser(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        context = {}
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                context['errors'] = 'Неправильный логин или пароль'
        return render(request, 'registration/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')

def activate_account(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    print(token)
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('index')
    else:
        return HttpResponse('Неверная ссылка активации!')