from util.Iterator import SimpleIterator as Iterator


class Computer:
    def __init__(self, program, feedback_mode):
        self.pc = iter(Iterator(0))
        self.program = program
        self.input_counter = iter(Iterator(0))
        self.relative_counter = 0
        self.feedback_mode = feedback_mode
        self.output = None

    def get_parameter_ad(self, mode):
        pointer = next(self.pc)
        if mode == 0 or mode is None:
            self.increase_memory_addresses(self.program[pointer] + 1 - len(self.program))
            return self.program[pointer]
        elif mode == 1:
            return pointer
        elif mode == 2:
            self.increase_memory_addresses((self.relative_counter + pointer + 1 - len(self.program)))
            return self.relative_counter + self.program[pointer]

    def increase_memory_addresses(self, increase):
        if increase > 0:
            self.program += ([0] * increase)

    def do_jump(self, is_jump, mode):
        if is_jump:
            return iter(Iterator(self.program[self.get_parameter_ad(mode)]))
        return iter(Iterator(next(self.pc) + 1))

    def run(self, *inputs):
        while True:
            inst = parse_instruction(self.program[next(self.pc)])
            if inst[0] == 1:
                result = self.program[self.get_parameter_ad(inst[1])] + self.program[self.get_parameter_ad(inst[2])]
                result_address = self.get_parameter_ad(inst[3])
                self.program[result_address] = result
            elif inst[0] == 2:
                result = self.program[self.get_parameter_ad(inst[1])] * self.program[self.get_parameter_ad(inst[2])]
                result_address = self.get_parameter_ad(inst[3])
                self.program[result_address] = result
            elif inst[0] == 3:
                next_input = next(self.input_counter)
                if next_input >= len(inputs):
                    number = int(input("input> "))
                else:
                    number = inputs[next_input]
                result_address = self.get_parameter_ad(inst[1])
                self.program[result_address] = number
            elif inst[0] == 4:
                out = self.program[self.get_parameter_ad(inst[1])]
                print(out)
                self.output = out
                if self.feedback_mode:
                    self.input_counter = iter(Iterator(0))
                    return False, self.output
            elif inst[0] == 5:
                self.pc = self.do_jump(self.program[self.get_parameter_ad(inst[1])] != 0, inst[2])
            elif inst[0] == 6:
                self.pc = self.do_jump(self.program[self.get_parameter_ad(inst[1])] == 0, inst[2])
            elif inst[0] == 7:
                result = self.program[self.get_parameter_ad(inst[1])] < self.program[self.get_parameter_ad(inst[2])]
                result_address = self.get_parameter_ad(inst[3])
                self.program[result_address] = 1 if result else 0
            elif inst[0] == 8:
                result = self.program[self.get_parameter_ad(inst[1])] == self.program[self.get_parameter_ad(inst[2])]
                result_address = self.get_parameter_ad(inst[3])
                self.program[result_address] = 1 if result else 0
            elif inst[0] == 9:
                self.relative_counter += self.program[self.get_parameter_ad(inst[1])]
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
