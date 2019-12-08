from util.Iterator import LoopingIterator as Iterator
from util.IntComputer import Computer


def generate_phase_settings(result, possible_digits, digits):
    if len(possible_digits) == 2:
        result.append(digits + [possible_digits[0], possible_digits[1]])
        result.append(digits + [possible_digits[1], possible_digits[0]])
        return result
    else:
        remaining_digits = possible_digits.copy()
        for digit in possible_digits:
            remaining_digits.remove(digit)
            digits.append(digit)
            generate_phase_settings(result, remaining_digits, digits)
            remaining_digits.append(digit)
            digits.remove(digit)
        return result


def execute(phase_settings, feedback_mode, filename="data/input_day_07.txt"):
    with open(filename, 'r') as input_file:
        program = list(map(int, input_file.read().split(",")))
    result = 0
    amplifiers = list()
    for phase_setting in phase_settings:
        computer = Computer(program.copy(), feedback_mode)
        _, result = computer.run(phase_setting, result)
        amplifiers.append(computer)
    if feedback_mode:
        i = iter(Iterator(0, 4))
        finished = False
        next_amp = next(i)
        while not finished or next_amp != 0:
            finished, result = amplifiers[next_amp].run(result)
            next_amp = next(i)
    return result


def find_phase_settings(phase_range, feedback_mode):
    best_result = 0, None
    phase_settings = generate_phase_settings(list(), phase_range, list())
    for phase_setting in phase_settings:
        result = execute(phase_setting, feedback_mode)
        if result > best_result[0]:
            best_result = result, phase_setting
    return best_result


print(execute([9, 7, 8, 5, 6], True, filename="data/test_day_07.txt"))
print(find_phase_settings([i for i in range(5)], False))
print(find_phase_settings([i for i in range(5, 10)], True))
