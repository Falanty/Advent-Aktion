from util.Iterator import SimpleIterator as Iterator


class Computer:
    def __init__(self, program, feedback_mode=False, print_output=False):
        self.pc = iter(Iterator(0))
        self.program = program
        self.input_counter = iter(Iterator(0))
        self.relative_pointer = 0
        self.feedback_mode = feedback_mode
        self.print_output = print_output
        self.inputs = ()
        self.output = None
        self.op_codes = {
            1: lambda x: self._add_values(x),
            2: lambda x: self._multiply_values(x),
            3: lambda x: self._handle_input(x),
            4: lambda x: self._handle_output(x),
            5: lambda x: self._jump_uneven(x),
            6: lambda x: self._jump_even(x),
            7: lambda x: self._store_less_than(x),
            8: lambda x: self._store_even(x),
            9: lambda x: self._increase_relative_pointer(x)
        }

    def run(self, *inputs):
        self.inputs = inputs
        while True:
            inst = parse_instruction(self.program[next(self.pc)])
            if inst[0] == 99:
                return True, self.output
            if inst[0] not in self.op_codes.keys():
                print("ERROR opCode: " + str(inst[0]))
                return True, None

            self.op_codes.get(inst[0])(inst)
            if inst[0] == 4 and self.feedback_mode:
                self.input_counter = iter(Iterator(0))
                return False, self.output

    def _get_parameter_ad(self, mode):
        pointer = next(self.pc)
        if mode == 0:
            self._increase_memory(self.program[pointer] + 1 - len(self.program))
            return self.program[pointer]
        elif mode == 1:
            return pointer
        elif mode == 2:
            self._increase_memory((self.relative_pointer + pointer + 1 - len(self.program)))
            return self.relative_pointer + self.program[pointer]

    def _increase_memory(self, increase):
        if increase > 0:
            self.program += ([0] * increase)

    def _do_jump(self, is_jump, mode):
        if is_jump:
            return iter(Iterator(self.program[self._get_parameter_ad(mode)]))
        return iter(Iterator(next(self.pc) + 1))

    def _add_values(self, inst):
        result = self.program[self._get_parameter_ad(inst[1])] + self.program[self._get_parameter_ad(inst[2])]
        self.program[self._get_parameter_ad(inst[3])] = result

    def _multiply_values(self, inst):
        result = self.program[self._get_parameter_ad(inst[1])] * self.program[self._get_parameter_ad(inst[2])]
        self.program[self._get_parameter_ad(inst[3])] = result

    def _handle_input(self, inst):
        next_input = next(self.input_counter)
        if next_input >= len(self.inputs):
            number = int(input("input> "))
        else:
            number = self.inputs[next_input]
        self.program[self._get_parameter_ad(inst[1])] = number

    def _handle_output(self, inst):
        out = self.program[self._get_parameter_ad(inst[1])]
        print(out) if self.print_output else None
        self.output = out

    def _jump_uneven(self, inst):
        self.pc = self._do_jump(self.program[self._get_parameter_ad(inst[1])] != 0, inst[2])

    def _jump_even(self, inst):
        self.pc = self._do_jump(self.program[self._get_parameter_ad(inst[1])] == 0, inst[2])

    def _store_less_than(self, inst):
        is_less_than = self.program[self._get_parameter_ad(inst[1])] < self.program[self._get_parameter_ad(inst[2])]
        self.program[self._get_parameter_ad(inst[3])] = 1 if is_less_than else 0

    def _store_even(self, inst):
        is_even = self.program[self._get_parameter_ad(inst[1])] == self.program[self._get_parameter_ad(inst[2])]
        self.program[self._get_parameter_ad(inst[3])] = 1 if is_even else 0

    def _increase_relative_pointer(self, inst):
        self.relative_pointer += self.program[self._get_parameter_ad(inst[1])]


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
