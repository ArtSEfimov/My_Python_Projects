number = int(input())


def calculate_n(num):
    tail = 0
    tmp = 0
    rest = 0
    for n in range(1, 50 + 1):
        tmp += n * 9 * pow(10, (n - 1))
        if num <= tmp:
            return n, rest
        else:
            rest = tmp


def calculate_number_in_thr_string(number):
    n, tail = calculate_n(number)
    s=0
    for i in range(1, n):
        s += 9 * pow(10, (i - 1))
    expression = (number - tail) // n
    rest = (number - tail) % n
    if rest == 0:
        expression = s + expression
        # return expression
        return str(expression)[::-1][-1]
    else:
        expression += s + 1
        tmp_string = str(expression)[::-1]
        # return expression
        return tmp_string[rest - 1]
        return tmp_string


# #
# for i in range(1, 200):
#     print(i, '\t', calculate_number_in_thr_string(i))
print(calculate_number_in_thr_string(number))
