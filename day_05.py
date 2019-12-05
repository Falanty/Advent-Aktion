class Iterator:
    def __iter__(self):
        self.i = 0
        return self

    def __next__(self):
        x = self.i
        self.i += 1
        return x


def parse_instruction(instruction):
    """
    >>> parse_instruction(3456)
    [56, 4, 3, 0]
    """
    parsed_instruction = list()
    parsed_digit = instruction % 100
    instruction //= 100
    for _ in range(4):
        parsed_instruction.append(parsed_digit)
        parsed_digit = instruction % 10
        instruction //= 10
    return parsed_instruction


def get_parameter(mode, program, pc):
    return program[program[next(pc)]] if mode == 0 else program[next(pc)]


def computer(program):
    """
    >>> computer([1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50])
    [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50]
    """
    pc = iter(Iterator())
    for _ in range(len(program)):
        inst = parse_instruction(program[next(pc)])
        if inst[0] == 1:
            result = get_parameter(inst[1], program, pc) + get_parameter(inst[2], program, pc)
            program[program[next(pc)]] = result
        elif inst[0] == 2:
            result = get_parameter(inst[1], program, pc) * get_parameter(inst[2], program, pc)
            program[program[next(pc)]] = result
        elif inst[0] == 3:
            number = int(input("input> "))
            program[program[next(pc)]] = number
        elif inst[0] == 4:
            print(program[program[next(pc)]])
        elif inst[0] == 99:
            return program
        else:
            return repr(inst) + " program alert!"


def execute(optional_reconstruct, filename="data/input_day_05.txt"):
    with open(filename, 'r') as input_file:
        program = list(map(int, input_file.read().split(",")))
        return optional_reconstruct(program, 19690720) if optional_reconstruct is not None else computer(program)


execute(None)
