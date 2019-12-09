from util.IntComputer import Computer


def execute(filename="data/input_day_09.txt"):
    with open(filename, 'r') as input_file:
        program = list(map(int, input_file.read().split(",")))
    computer = Computer(program, print_output=True)
    return computer.run()


execute(filename="data/test_day_09.txt")
execute()
