from util.IntComputer import Computer


def execute(feedback_mode, filename="data/input_day_09.txt"):
    with open(filename, 'r') as input_file:
        program = list(map(int, input_file.read().split(",")))
    computer = Computer(program, feedback_mode)
    return computer.run()


execute(False, filename="data/test_day_09.txt")
execute(False)
