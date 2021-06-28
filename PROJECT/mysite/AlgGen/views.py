from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.forms import UserCreationForm

from .problem_generator import *

NUMBER_OF_PROBLEMS = 5


def index(request):
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

def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form':form}
    return render(request, 'accounts/register.html', context)
def loginPage(request):
    context = {}
    return render(request, 'accounts/login.html', context)