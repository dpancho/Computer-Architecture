"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.reg = [0] * 256   
        self.ram = [0] * 64   
        self.stack_pointer = 0xF3

    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self,mar,mdr):
        self.ram[mar] = mdr

    def load(self, file_name):
        """Load a program into memory."""

        address = 0

        with open(file_name) as f: 
            lines = f.readlines()
            lines = [line for line in lines if line.startswith('0') or line.startswith('1')]
            program = [int(line[:8], 2) for line in lines]

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1
        
        print(self.ram)


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB": 
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        HLT = 0b00000001  ##Hault = 1
        LDI = 0b10000010  ##Load  = 130
        PRN = 0b01000111  ##Print = 71
        MUL = 0b10100010
        PUSH = 0b01000101
        POP = 0b01000110

        running = True
        IR = self.pc

        while running:
            instruction = self.ram_read(IR)
            opr_a = self.ram_read(IR + 1)
            opr_b = self.ram_read(IR + 2)

            ##if instruc is Hault
            if instruction == HLT:
                # running = False
                # self.pc +=1
                sys.exit(0)

            ##if instruc is Load
            elif instruction == LDI:
                self.reg[opr_a] = opr_b
                IR += 3 

            ##if instruc is Print
            elif instruction == PRN:
                print(self.reg[opr_a])
                IR += 2

            #if inctruc is MULTIPLY
            elif instruction == MUL:
                self.alu("MUL", opr_a, opr_b)
                IR += 3 
                print('you are MULTIPLYING')
            
            # PUSH
            elif instruction == PUSH:
                # register = self.ram[opr_a]
                self.stack_pointer -= 1
                self.reg[self.stack_pointer] = self.reg[self.ram[opr_a]]
                IR += 2
            
            # POP
            elif instruction == POP:
                # register = self.ram[opr_a]
                self.reg[self.ram[opr_a]] = self.reg[self.stack_pointer]
                self.stack_pointer += 1
                IR += 2

            else:
                print(f"bad input: {bin(instruction)}")
                # running = False
                sys.exit(1)
