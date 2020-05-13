"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.sp = 0
        self.pc = 0
        self.MAR = None
        self.MDR = None
        # self.FL = 0

    def load(self, load_file):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010,  # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111,  # PRN R0
        #     0b00000000,
        #     0b00000001,  # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

        # sys.argv is a list of all args
        load_file = load_file
        print("load_file => ", load_file)

        with open(load_file) as f:
            for line in f:
                # add to memory
                i = line.split("#")
                num = i[0].strip()
                if num == "":
                    continue

                self.ram[address] = int(num, 2)
                print("current address => ", address)
                print("value in the RAM => ", self.ram[address])

                address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def ram_read(self, index):
        return self.ram[index]

    def ram_write(self, value, address):
        self.ram[address] = value

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True
        while running == True:
            command = self.ram[self.pc]
            # LDI - load and store in register
            if command == 0b10000010:
                self.reg[self.ram[self.pc + 1]] = self.ram[self.pc + 2]
                self.pc += 3
            # PRINT
            elif command == 0b01000111:
                print(self.reg[self.ram[self.pc + 1]])
                self.pc += 2
            # MULTIPLY
            elif command == 0b10100010:
                reg1 = self.ram[self.pc + 1]
                reg2 = self.ram[self.pc + 2]
                answer = self.reg[reg1] * self.reg[reg2]
                print("PRODUCT => ", answer)
                self.reg[0] = answer
                self.reg[1] = 0
                self.pc += 3
            # HALT
            elif command == 0b00000001:
                running = False

            # IF NOT RECOGNIZED
            else:
                sys.exit(1)
