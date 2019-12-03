import numpy as np


def computer(program):
    """
    TODO sehr unschön

    >>> computer([1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50])
    [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50]
    """
    opcode_positions = np.arange(0, len(program), 4)
    for int_pointer in opcode_positions:
        opcode = program[int_pointer]
        first_parameter_address = program[int_pointer + 1]
        second_parameter_address = program[int_pointer + 2]
        result_address = program[int_pointer + 3]
        if opcode == 1:
            program[result_address] = program[first_parameter_address] + program[second_parameter_address]
        elif opcode == 2:
            program[result_address] = program[first_parameter_address] * program[second_parameter_address]
        elif opcode == 99:
            return program
        else:
            return repr(opcode) + "program alert!"


def execute(optional_reconstruct, filename="data/input_day_02.txt"):
    with open(filename, 'r') as input_file:
        program = list(map(int, input_file.read().split(",")))
        return optional_reconstruct(program, 19690720) if optional_reconstruct is not None else computer(program)


def reconstruct_program(program, output):
    for a in range(0, 100):
        for b in range(0, 100):
            test_program = program.copy()
            test_program[1] = a
            test_program[2] = b
            computer(test_program)
            if test_program[0] == output:
                return test_program
    return "ERROR!"


print(execute(None))
print(execute(reconstruct_program))
