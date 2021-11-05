from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.timezone import now, pytz
from django.conf import settings
import json

from datetime import datetime, timezone

from .problem_generator import *


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    course_step = models.CharField(default='Модуль 1. Арифметика', max_length=20)
    is_course_started = models.BooleanField(default=False)
    is_course_completed = models.BooleanField(default=False)
    problems = models.CharField(default=json.dumps({"Модуль 1. Арифметика": [], "Модуль 2. Линейные уравнения": [],
                                                    "Модуль 3. Квадратный трехчлен": [], "Модуль 4. Системы": [],
                                                    "Модуль 5. Замена переменной": [], "Модуль 6. Производная": [],
                                                    "Модуль 7. Неравенства": []}), max_length=100000)
    solved_problems = models.CharField(
        default=json.dumps({"Модуль 1. Арифметика": [], "Модуль 2. Линейные уравнения": [],
                            "Модуль 3. Квадратный трехчлен": [], "Модуль 4. Системы": [],
                            "Модуль 5. Замена переменной": [], "Модуль 6. Производная": [],
                            "Модуль 7. Неравенства": []}), max_length=100000)
    unsolved_problems = models.CharField(
        default=json.dumps({"Модуль 1. Арифметика": [], "Модуль 2. Линейные уравнения": [],
                            "Модуль 3. Квадратный трехчлен": [], "Модуль 4. Системы": [],
                            "Модуль 5. Замена переменной": [], "Модуль 6. Производная": [],
                            "Модуль 7. Неравенства": []}), max_length=100000)
    course_start_datetime = models.DateTimeField(default=datetime(1970, 1, 1, tzinfo=pytz.timezone(settings.TIME_ZONE)))
    course_end_datetime = models.DateTimeField(default=datetime(1970, 1, 1, tzinfo=pytz.timezone(settings.TIME_ZONE)))

    def __str__(self):
        return self.user.username

    def generate_course_problems(self):
        problems_dict = {"Модуль 1. Арифметика": [], "Модуль 2. Линейные уравнения": [],
                         "Модуль 3. Квадратный трехчлен": [], "Модуль 4. Системы": [],
                         "Модуль 5. Замена переменной": [], "Модуль 6. Производная": [],
                         "Модуль 7. Неравенства": []}
        for problem_number in range(3):
            problems_dict['Модуль 1. Арифметика'].append([problem_number] + generate_arithmetic())
            problems_dict['Модуль 2. Линейные уравнения'].append([problem_number] + generate_linear())
            problems_dict['Модуль 3. Квадратный трехчлен'].append([problem_number] + generate_quadratic())
            problems_dict['Модуль 4. Системы'].append([problem_number] + generate_system())
            problems_dict['Модуль 5. Замена переменной'].append([problem_number] + generate_replacement())
            problems_dict['Модуль 6. Производная'].append([problem_number] + generate_derivative())
            problems_dict['Модуль 7. Неравенства'].append([problem_number] + generate_inequality())
        self.problems = json.dumps(problems_dict)
        self.solved_problems = json.dumps({"Модуль 1. Арифметика": [], "Модуль 2. Линейные уравнения": [],
                                "Модуль 3. Квадратный трехчлен": [], "Модуль 4. Системы": [],
                                "Модуль 5. Замена переменной": [], "Модуль 6. Производная": [],
                                "Модуль 7. Неравенства": []})
        self.unsolved_problems = json.dumps({"Модуль 1. Арифметика": [], "Модуль 2. Линейные уравнения": [],
                                  "Модуль 3. Квадратный трехчлен": [], "Модуль 4. Системы": [],
                                  "Модуль 5. Замена переменной": [], "Модуль 6. Производная": [],
                                  "Модуль 7. Неравенства": []})

    def create_profile(sender, **kwargs):
        user = kwargs["instance"]
        if kwargs["created"]:
            user_profile = Account(user=user)
            user_profile.save()

    post_save.connect(create_profile, sender=User)
