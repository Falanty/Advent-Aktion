from util.Iterator import SimpleIterator as Iterator


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


def do_jump(is_jump, mode, program, pc):
    if is_jump:
        return iter(Iterator(get_parameter(mode, program, pc)))
    return iter(Iterator(next(pc)+1))


def computer(program):
    pc = iter(Iterator(0))
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
            print(get_parameter(inst[1], program, pc))
        elif inst[0] == 5:
            pc = do_jump(get_parameter(inst[1], program, pc) != 0, inst[2], program, pc)
        elif inst[0] == 6:
            pc = do_jump(get_parameter(inst[1], program, pc) == 0, inst[2], program, pc)
        elif inst[0] == 7:
            result = get_parameter(inst[1], program, pc) < get_parameter(inst[2], program, pc)
            program[program[next(pc)]] = 1 if result else 0
        elif inst[0] == 8:
            result = get_parameter(inst[1], program, pc) == get_parameter(inst[2], program, pc)
            program[program[next(pc)]] = 1 if result else 0
        elif inst[0] == 99:
            return program
        else:
            print("error, opcode: " + str(inst))


def execute(filename="data/input_day_05.txt"):
    with open(filename, 'r') as input_file:
        program = list(map(int, input_file.read().split(",")))
        return computer(program)


execute()
