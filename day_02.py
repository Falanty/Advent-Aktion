class Iterator:
    def __iter__(self):
        self.i = 0
        return self

    def __next__(self):
        x = self.i
        self.i += 1
        return x


def computer(program):
    """
    >>> computer([1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50])
    [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50]
    """
    int_pointer = iter(Iterator())
    for _ in range(len(program)):
        opcode = program[next(int_pointer)]
        if opcode == 1:
            result = program[program[next(int_pointer)]] + program[program[next(int_pointer)]]
            program[program[next(int_pointer)]] = result
        elif opcode == 2:
            result = program[program[next(int_pointer)]] * program[program[next(int_pointer)]]
            program[program[next(int_pointer)]] = result
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
