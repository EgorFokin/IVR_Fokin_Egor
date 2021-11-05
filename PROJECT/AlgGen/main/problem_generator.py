import random


# operations:
# 1.addition/substraction
# 2.multiplication
# 3.division
# 4.square root

def __get_divisors(n):
    ans = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            ans.append(d)
            n //= d
        else:
            d += 1
    if n > 1:
        ans.append(n)
    return ans


def generate_arithmetic():
    text = '`'
    ans = random.randint(-40, 40)
    stage_ans = ans
    stages = random.randint(1, 3)
    suffix = ''
    for stage_number in range(stages):
        available_operations = {1, 2, 3, 4}
        divisors = __get_divisors(abs(stage_ans))
        if len(divisors) < 2:
            available_operations.remove(2)
        if stage_ans == 0:
            available_operations.remove(3)
        if stage_ans < 0 or stage_ans > 15:
            available_operations.remove(4)
        operation = list(available_operations)[random.randint(0, len(available_operations) - 1)]
        if operation == 1:
            second_term = random.randint(1, 20) * ([-1, 1][random.randint(0, 1)])
            if (text and text[-1] == '+') and second_term < 0:
                text = text[:-1]
            text += f'{second_term}+'
            stage_ans = stage_ans - second_term
        if operation == 2:
            second_multiplier = divisors[random.randint(0, len(divisors) - 1)]
            if (text and text[-1] == '+') and second_multiplier < 0:
                text = text[:-1]
            text += f'{second_multiplier}*'
            if stage_number != stages - 1:
                text += '('
                suffix += ')'
            stage_ans = stage_ans // second_multiplier
        if operation == 3:
            division_number = random.randint(2, 5) * ([-1, 1][random.randint(0, 1)]) * stage_ans
            if (text and text[-1] == '+') and division_number < 0:
                text = text[:-1]
            text += f'{division_number}/'
            if stage_number != stages - 1:
                text += '('
                suffix += ')'
            stage_ans = division_number // stage_ans
        if operation == 4:
            if text[-1] == '(':
                text = text[:-1]
                suffix = suffix[:-1]
            text += f'sqrt('
            suffix += ')'
            stage_ans = stage_ans ** 2
    if (text and text[-1] == '+') and stage_ans < 0:
        text = text[:-1]
    text += str(stage_ans)
    text += suffix + '`'
    # print(text,ans)
    return [text, str(ans), str(ans)]


def generate_linear():
    a = random.randint(2, 20)
    b = random.randint(2, 20)
    c = a * b
    return [f'`{b}x-{c}=0`', str(a), f'`{c}/{b}={a}`']


def generate_quadratic():
    x1 = random.randint(1, 15) * [1, -1][random.randint(0, 1)]
    x2 = random.randint(1, 15) * [1, -1][random.randint(0, 1)]
    a = random.randint(1, 5) * [1, -1][random.randint(0, 1)]
    b = -(x1 + x2) * a
    c = x1 * x2 * a
    solution = f'1. `D={b}^2-4*{a}*{c}={b ** 2 - (4 * a * c)}`;' \
               f' 2. `x1=({-b}+sqrt({b ** 2 - (4 * a * c)}))'f'/(2*{a})={int((-b + (b ** 2 - (4 * a * c)) ** 0.5) / (2 * a))}`;' \
               f' 3. `x2=({-b}-sqrt({b ** 2 - (4 * a * c)}))/(2*{a})={int((-b - (b ** 2 - (4 * a * c)) ** 0.5) / (2 * a))}`'
    if a == 1: a = ''
    if a == -1: a = '-'
    if b == 1: b = ''
    if b == -1: b = '-'
    print(f'{min(x1, x2)} {max(x1, x2)}')
    return [f'`{a}x^2+{b}x+{c}=0`'.replace('+-', '-'), f'{min(x1, x2)} {max(x1, x2)}', solution]


def generate_system():
    a1 = random.randint(1, 10) * [1, -1][random.randint(0, 1)]
    a2 = random.randint(1, 10) * [1, -1][random.randint(0, 1)]
    b1 = random.randint(1, 10) * [1, -1][random.randint(0, 1)]
    b2 = random.randint(1, 10) * [1, -1][random.randint(0, 1)]
    x = random.randint(1, 10) * [1, -1][random.randint(0, 1)]
    y = random.randint(1, 10) * [1, -1][random.randint(0, 1)]
    c1 = a1 * x + b1 * y
    c2 = a2 * x + b2 * y
    solution = f'Домножив 2ое неравенство на `{a1} / {a2}` и вычев 2ое из 1ого, получаем `({b1 - b2 * a1 / a2})y = {c1 - c2 * a1 / a2}`, ' \
               f'Отсюда: `y = {y}`, значит `x = {x}`'
    if a1 == 1: a1 = ''
    if a1 == -1: a1 = '-'
    if b1 == 1: b1 = ''
    if b1 == -1: b1 = '-'
    if a2 == 1: a2 = ''
    if a2 == -1: a2 = '-'
    if b2 == 1: b2 = ''
    if b2 == -1: b2 = '-'
    return [f'`{{({a1}x+{b1}y={c1}),({a2}x+{b2}y={c2}):}}`'.replace('+-', '-'), f'{x} {y}', solution]


def generate_replacement():
    NUMBERS = {2, 3, 4, 5, 7}
    divisors = []
    for i in range(3):
        divisors.append(random.choice(list(NUMBERS)))
        NUMBERS.remove(divisors[-1])
    c = divisors[0] * divisors[1] * divisors[2]
    x1 = divisors[0]
    x2 = c // x1
    b1 = -(x1 + x2)
    c1 = divisors[1]
    c2 = c // c1
    c3 = divisors[2]
    c4 = c // c3
    t = c1 + c2 - b1
    c5 = t * (t + (c3 + c4 - c1 - c2))
    solution = f'Преобразуем равенство, перемножив первые две скобки и последние две скобки:' \
               f' `(x^2 + {c1 + c2}x+{c1 * c2})(x^2 + {c3 + c4}x+{c3 * c4})={c5}x^2`;' \
               f' Поделим обе части на `x^2`, проверив, что он не равен 0, получим: ' \
               f'`(x + {c1 + c2}+{c1 * c2}/x)(x + {c3 + c4}+{c3 * c4}/x)={c5}`; ' \
               f'Сделаем замену `t = x + {c1 + c2}+{c1 * c2}/x`: `t(t+{c3 + c4-c1 - c2}) = {c5}`; ' \
               f'Отсюда `t^2+{c3 + c4-c1 - c2}t-{c5}=0`; `t1 = {(-(c3 + c4-c1 - c2) + ((c3 + c4-c1 - c2)**2+4*c5)**0.5)/2},' \
               f't2 = {(-(c3 + c4-c1 - c2) - ((c3 + c4-c1 - c2)**2+4*c5)**0.5)/2}`; ' \
               f'Выразим через x: `x + {c1 + c2}+{c1 * c2}/x = {(-(c3 + c4-c1 - c2) + ((c3 + c4-c1 - c2)**2+4*c5)**0.5)/2}`' \
               f' или `x + {c1 + c2}+{c1 * c2}/x = {(-(c3 + c4-c1 - c2) - ((c3 + c4-c1 - c2)**2+4*c5)**0.5)/2}`; ' \
               f'Домножив на x получаем 2 квадратных уравнения: ' \
               f'`x^2 +{-(-(c3 + c4-c1 - c2) + ((c3 + c4-c1 - c2)**2+4*c5)**0.5)/2}x+{c1 + c2+c1 * c2} = 0` и ' \
               f'`x^2 +{-(-(c3 + c4-c1 - c2) - ((c3 + c4-c1 - c2)**2+4*c5)**0.5)/2}x+{c1 + c2+c1 * c2} = 0`; ' \
               f'Отсюда ответ: {min(x1, x2)},{max(x1, x2)}'.replace('+-', '-').replace('.0','')

    return [f'`(x+{c1})(x+{c2})(x+{c3})(x+{c4})={c5}x^2`'.replace('+-', '-'), f'{min(x1, x2)} {max(x1, x2)}', solution]


def generate_derivative():
    length = random.randint(3, 6)
    text = '`'
    a = random.randint(2, 5) * [1, -1][random.randint(0, 1)]
    ans = 0
    solution = ''
    for i in range(length):
        factor = random.randint(1, 10) * [1, -1][random.randint(0, 1)]
        if i != 0:
            text += '+'
            if i != length - 1:
                solution += '+'
        if i != length - 1:
            if factor == 1:
                text += 'x'
                if i != length - 2:
                    solution += str(length - i - 1) + 'x'
            elif factor == -1:
                text += '-' + str(length - i - 1) + 'x'
                if i != length - 2:
                    solution += '-x'
            else:
                text += str(factor) + 'x'
                if i != length - 2:
                    solution += str(factor * (length - i - 1)) + 'x'
            if i != length - 2:
                text += '^' + str(length - i - 1)
                if i != length - 3:
                    solution += '^' + str(length - i - 2)

            ans += (length - i - 1) * factor * (a ** (length - i - 2))
        else:
            text += str(factor)
        if i == length - 2:
            solution += str(factor * (length - i - 1))
    text += f';x={a}`'
    return [text.replace('+-', '-'), str(ans),
            f"Используя `f'(x^n)=n*x^(n-1)`, получаем: `{solution.replace('+-', '-')}`; Подставив x={a}, получаем {ans}"]


def generate_inequality():
    x1 = random.randint(1, 15) * [1, -1][random.randint(0, 1)]
    x2 = random.randint(1, 15) * [1, -1][random.randint(0, 1)]
    a = random.randint(1, 5) * [1, -1][random.randint(0, 1)]
    b = -(x1 + x2) * a
    c = x1 * x2 * a
    if a == 1: a = ''
    if a == -1: a = '-'
    if b == 1: b = ''
    if b == -1: b = '-'
    return [f'`{a}x^2+{b}x+{c}>=0`'.replace('+-', '-'), f'{min(x1, x2)} {max(x1, x2)}',
            f'Решив квадратное уравнение, получим:'
            f'` {a}x^2+{b}x+{c}=(x+{-x1})(x+{-x2})`, '
            f'Отсюда по методу интервалов ответ: {min(x1, x2)};{max(x1, x2)}'.replace('+-', '-')]
