from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt

import json

import os

from datetime import datetime

from .forms import CreateUserForm

from .problem_generator import *

from .confirmation_tokens import account_activation_token

COURSE_STEPS = ["Модуль 1. Арифметика", "Модуль 2. Линейные уравнения", "Модуль 3. Квадратный трехчлен",
                "Модуль 4. Системы",
                "Модуль 5. Замена переменной", "Модуль 6. Производная", "Модуль 7. Неравенства"]


def index(request):
    NUMBER_OF_PROBLEMS = 5
    if request.user.is_authenticated:
        problem_type = request.GET.get('type')
        if not problem_type:
            problem_type = 'arithmetic'
        problems = []
        for problem_number in range(NUMBER_OF_PROBLEMS):
            if problem_type == 'arithmetic':
                problems.append([problem_number] + generate_arithmetic())
            if problem_type == 'linear':
                problems.append([problem_number] + generate_linear())
            if problem_type == 'quadratic':
                problems.append([problem_number] + generate_quadratic())
            if problem_type == 'system':
                problems.append([problem_number] + generate_system())
            if problem_type == 'replacement':
                problems.append([problem_number] + generate_replacement())
            if problem_type == 'derivative':
                problems.append([problem_number] + generate_derivative())
            if problem_type == 'inequality':
                problems.append([problem_number] + generate_inequality())
        context = {'problems': problems, 'problem_type': problem_type}
        return render(request, 'index.html', context)
    else:
        return redirect('login')


def courses(request):
    user = request.user
    if request.method == 'POST':
        if 'review_text' in request.POST:

            review_text = request.POST['review_text']
            with open('main/reviews.txt','r+') as f:
                reviews = json.load(f) if os.stat('main/reviews.txt').st_size != 0 else []
                reviews.append(review_text)
                f.seek(0)
                f.truncate(0)
                f.write(json.dumps(reviews))

        if 'solved_problems[]' in request.POST:
            solved_problems = json.loads(user.account.solved_problems)
            for problem in request.POST.getlist('solved_problems[]'):
                if int(problem) not in solved_problems[user.account.course_step]:
                    solved_problems[user.account.course_step].append(int(problem))
            user.account.solved_problems = json.dumps(solved_problems)
        if 'unsolved_problems[]' in request.POST:
            unsolved_problems = json.loads(user.account.unsolved_problems)
            for problem in request.POST.getlist('unsolved_problems[]'):
                if int(problem) not in unsolved_problems[user.account.course_step]:
                    unsolved_problems[user.account.course_step].append(int(problem))
            user.account.unsolved_problems = json.dumps(unsolved_problems)
        if 'next_module' in request.POST:
            if COURSE_STEPS.index(user.account.course_step) != len(COURSE_STEPS) - 1:
                user.account.course_step = COURSE_STEPS[COURSE_STEPS.index(user.account.course_step) + 1]
            else:
                user.account.is_course_completed = 1
                user.account.course_end_datetime = datetime.now()
                with open('main/average_solved_problems.txt', "r+") as f:

                    average_solved_problems = json.loads(f.read()) if os.stat(
                        'main/average_solved_problems.txt').st_size != 0 else {"Модуль 1. Арифметика": [0, 0],
                                                                               "Модуль 2. Линейные уравнения": [0,
                                                                                                                0],
                                                                               "Модуль 3. Квадратный трехчлен": [
                                                                                   0, 0],
                                                                               "Модуль 4. Системы": [0, 0],
                                                                               "Модуль 5. Замена переменной": [0,
                                                                                                               0],
                                                                               "Модуль 6. Производная": [0, 0],
                                                                               "Модуль 7. Неравенства": [0, 0]}
                    solved_problems = json.loads(user.account.solved_problems)
                    for module in COURSE_STEPS:
                        average_solved_problems[module][0] += len(solved_problems[module])
                        average_solved_problems[module][1] += 1
                    f.seek(0)
                    f.truncate(0)
                    f.write(json.dumps(average_solved_problems))

        if 'previous_module' in request.POST:
            if COURSE_STEPS.index(user.account.course_step) != 0:
                user.account.course_step = COURSE_STEPS[COURSE_STEPS.index(user.account.course_step) - 1]
        if 'start_course' in request.POST:
            user.account.course_start_datetime = datetime.now()
            user.account.course_step = COURSE_STEPS[0]
            user.account.is_course_completed = 0
            user.account.is_course_started = 1
            user.account.generate_course_problems()
        user.account.save()
        return redirect('courses')
    NUMBER_OF_PROBLEMS = 3
    course_step = user.account.course_step
    user_problems = json.loads(user.account.problems)
    solved_problems = json.loads(user.account.solved_problems)
    unsolved_problems = json.loads(user.account.unsolved_problems)
    solved_problems_stats = []
    average_solved = []
    with open('main/average_solved_problems.txt') as f:
        average_solved_problems = json.load(f) if os.stat(
            'main/average_solved_problems.txt').st_size != 0 else {"Модуль 1. Арифметика": [0, 0],
                                                                   "Модуль 2. Линейные уравнения": [0,
                                                                                                    0],
                                                                   "Модуль 3. Квадратный трехчлен": [
                                                                       0, 0],
                                                                   "Модуль 4. Системы": [0, 0],
                                                                   "Модуль 5. Замена переменной": [0,
                                                                                                   0],
                                                                   "Модуль 6. Производная": [0, 0],
                                                                   "Модуль 7. Неравенства": [0, 0]}
        for module in COURSE_STEPS:
            solved_problems_stats.append(str(len(solved_problems[module])))
            if (average_solved_problems[module][1] == 0):
                average_solved.append('0')
            else:
                average_solved.append(f'{average_solved_problems[module][0] / average_solved_problems[module][1]:.2f}')
    time_spent = str(user.account.course_end_datetime - user.account.course_start_datetime)

    context = {"course_step": course_step, 'problems': user_problems[course_step],
               'solved_problems': solved_problems[course_step], 'unsolved_problems': unsolved_problems[course_step],
               'is_course_started': user.account.is_course_started,
               'is_course_completed': user.account.is_course_completed,
               'solved_problems_stats': solved_problems_stats,
               'time_spent': time_spent,
               'average_solved':average_solved}
    return render(request, 'courses.html', context)


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
