from util.Iterator import SimpleIterator as Iterator


class Computer:
    def __init__(self, program, feedback_mode):
        self.pc = iter(Iterator(0))
        self.program = program
        self.input_counter = iter(Iterator(0))
        self.feedback_mode = feedback_mode
        self.output = None

    def get_parameter(self, mode):
        return self.program[self.program[next(self.pc)]] if mode == 0 else self.program[next(self.pc)]

    def do_jump(self, is_jump, mode):
        if is_jump:
            return iter(Iterator(self.get_parameter(mode)))
        return iter(Iterator(next(self.pc) + 1))

    def run(self, *inputs):
        while True:
            inst = parse_instruction(self.program[next(self.pc)])
            if inst[0] == 1:
                result = self.get_parameter(inst[1]) + self.get_parameter(inst[2])
                self.program[self.program[next(self.pc)]] = result
            elif inst[0] == 2:
                result = self.get_parameter(inst[1]) * self.get_parameter(inst[2])
                self.program[self.program[next(self.pc)]] = result
            elif inst[0] == 3:
                next_input = next(self.input_counter)
                if next_input >= len(inputs):
                    number = int(input("input> "))
                else:
                    number = inputs[next_input]
                self.program[self.program[next(self.pc)]] = number
            elif inst[0] == 4:
                out = self.get_parameter(inst[1])
                self.output = out
                if self.feedback_mode:
                    self.input_counter = iter(Iterator(0))
                    return False, self.output
            elif inst[0] == 5:
                self.pc = self.do_jump(self.get_parameter(inst[1]) != 0, inst[2])
            elif inst[0] == 6:
                self.pc = self.do_jump(self.get_parameter(inst[1]) == 0, inst[2])
            elif inst[0] == 7:
                result = self.get_parameter(inst[1]) < self.get_parameter(inst[2])
                self.program[self.program[next(self.pc)]] = 1 if result else 0
            elif inst[0] == 8:
                result = self.get_parameter(inst[1]) == self.get_parameter(inst[2])
                self.program[self.program[next(self.pc)]] = 1 if result else 0
            elif inst[0] == 99:
                return True, self.output
            else:
                print("ERROR opcode: " + str(inst[0]))
                return True, None


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
