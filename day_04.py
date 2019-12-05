def is_number_sorted(number):
    return all(number[i] <= number[i+1] for i in range(len(number)-1))


def check_double(password, only_doubles):
    number_count = 0
    number = None
    for i in password:
        if i is not number:
            if not only_doubles and number_count >= 2 or only_doubles and number_count == 2:
                return True
            number = i
            number_count = 1
        else:
            number_count += 1
    if not only_doubles and number_count >= 2 or only_doubles and number_count == 2:
        return True
    return False


def count_password_possibilities(password_range, only_doubles):
    result = 0
    for password in password_range:
        password = str(password)
        if check_double(password, only_doubles) and is_number_sorted(password):
            result += 1
    return result


print(count_password_possibilities(range(193651, 649729), False))
print(count_password_possibilities(range(193651, 649729), True))
