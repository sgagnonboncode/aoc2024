from src.common.file_utils import read_lines


class Computer():

    def __init__(self,eax:int,ebx:int,ecx:int,program:list[int]):
        self.program: list[int] = program
        self.eax:int = eax
        self.ebx:int = ebx
        self.ecx:int = ecx
        self.ptr:int = 0
        self.output: list[int] = []
        self._initial_state = (self.eax, self.ebx, self.ecx, self.ptr)


    @staticmethod
    def parse_input(input_lines:list[str]) -> 'Computer':
        computer = Computer(
            eax=int(input_lines[0].split(": ")[1].strip()),
            ebx=int(input_lines[1].split(": ")[1].strip()),
            ecx=int(input_lines[2].split(": ")[1].strip()),
            program=[int(x) for x in input_lines[4].split(": ")[1].split(",")]
        )
        return computer
    
    def reset(self):
        self.eax, self.ebx, self.ecx, self.ptr = self._initial_state
        self.output = []

    
    def combo_value(self, operand:int) -> int:
        if operand in(0,1,2,3):
            return operand
        elif operand == 4:
            return self.eax
        elif operand == 5:
            return self.ebx
        elif operand == 6:
            return self.ecx
        else:
            raise ValueError(f"Invalid program.")

    def out(self, operand:int)->bool:
        new_value = self.combo_value(operand) % 8
        self.output.append(new_value)
        return True


    def run(self, eax:int|None=None)-> list[int]:
        self.reset()
        if eax is not None:
            self.eax = eax
        
        p_len = len(self.program)
        while self.ptr < p_len:
            opcode = self.program[self.ptr]
            operand = self.program[self.ptr + 1]

            if opcode == 0:
                # division, combo
                # eax = eax // 2 ^ value , which is a very convoluted
                #  way of saying 'shift right' by value positions, up to 7 bits
                value = self.combo_value(operand)
                self.eax = self.eax // (2 ** value)
                # self.eax = self.eax >> value
            elif opcode == 1:
                # bitwise XOR, literal
                # ebx = ebx XOR operand
                self.ebx = self.ebx ^ operand 
            elif opcode == 2:
                # modulo 8, combo
                value = self.combo_value(operand)
                self.ebx = value % 8
            elif opcode == 3:
                # nop if eax = 0
                # jump otherwise, literal
                if self.eax != 0:
                    self.ptr = operand
                    continue  # skip the ptr increment at the end
      
            elif opcode ==4:
                # bitwize XOR ebx and ecx
                # operand ignored for 'legacy' reasons
                self.ebx = self.ebx ^ self.ecx
            elif opcode ==5:
                # output
                self.out(operand)
            elif opcode ==6:
                value = self.combo_value(operand)
                # convoluted way of doing : self.ebx = self.eax >> value
                self.ebx = self.eax // (2 ** value)
            elif opcode ==7:
                value = self.combo_value(operand)
                # convoluted way of doing : self.ecx = self.eax >> value
                self.ecx = self.eax // (2 ** value)
            self.ptr +=2
        return self.output
    

    # NOTE: A compiled program of my input which turned out to not be needed after all.
    #       I changed my program to use the 'run' method instead to be able to support
    #       all puzzle inputs.
    #
    # def simplified(self, eax_init:int)->list[int]:
    #     # 2,4 : ebx = eax % 8
    #     # 1,1 : ebx = ebx ^ 1
    #     # 7,5 : ecx = eax >> (ebx %8) 
    #     # 1,5 : ebx = ebx ^ 5
    #     # 4,1 : ebx = self.ebx ^ self.ecx
    #     # 5,5 : output ebx%8
    #     # 0,3 : eax >>= 3
    #     # 3,0 : JNZ 0 / NOP
    #     # since we always jump back to 0 , we can never be out of bounds
    #     #  unless we are done (eax == 0)
    #
    #     # since the numbers are positive, we can use &7 instead of %8 , which is faster
    #
    #     output: list[int] = []
    #     eax = eax_init
    #     while True:
    #         ebx = (eax & 7) ^ 1
    #         ebx = ((ebx ^ 5) ^ (eax >> (ebx & 7))) &7
    #         output.append(ebx)
    #         eax = eax >> 3  # shift right 3 bits
    #         if eax == 0:
    #             break
    #     return output

    def debug(self)->int:
        
        # for the puzzle input:
        # - the loop produces an output per octal segment of eax
        # - eax must then be in [8**(n-1) ... 8**(n)-1)  to produce n outputs
        #   since the last jump will end the program with eax ==0
        # (may not be true for programs which do not end with 0330)
        #
        # test assumption
        # for n in range(2,17):
        #     upper_bound = 8**n -1
        #     lower_bound = 8**(n-1)
        #     upper_output_len = len(self.run(upper_bound))
        #     lower_output_len = len(self.run(lower_bound))
        #     assert upper_output_len == n
        #     assert lower_output_len == n
        #     assert len(self.run(upper_bound+1)) == n+1
        #     assert len(self.run(lower_bound-1)) == n-1

        # backward induction: try to generate the program backwards
        solutions = {0}
        step =0
        for p in reversed(self.program):
            step+=1
            # print(f"Step {step}")#, current solutions: {solutions}")
            # only the 3 last instructions are significant to generate an output when going backwards
            # (found by analysis of the program)

            # new_sols = set()
            # for s in solutions:
            #     for x in range(8):
            #         eax = s << 3 | x
            #         # output = self.simplified(eax)
            #         output = self.run(eax)
            #         if len(output) >= step and output[-step] == p:
            #             new_sols.add(eax)

            solutions = {
                eax for s in solutions for x in range(8)
                if len(output:= self.run(eax:= s<<3 |x)) >= step and output[-step] == p
            }

        min_eax = min(solutions)

        # test program one last time
        assert self.run(min_eax) == self.program
 
        return min_eax
        
            
def solve_part1() -> str:
    # lines = read_lines("input/day17/example2.txt")
    lines = read_lines("input/day17/part1.txt")
    computer = Computer.parse_input(lines)
    computer.run()
    return ",".join(str(x) for x in computer.output)

def solve_part2() -> int:
    # lines = read_lines("input/day17/example2.txt")
    lines = read_lines("input/day17/part1.txt")
    computer = Computer.parse_input(lines)
    return computer.debug()