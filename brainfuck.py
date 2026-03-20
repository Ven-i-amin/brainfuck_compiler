class brainfuck:
    list = [0] * 30000
    pointer = 0

    def move_pointer(self, direction):
        if direction == '>':
            self.pointer += 1
        elif direction == '<':
            self.pointer -= 1

    def change_value(self, command):
        if command == '+':
            self.list[self.pointer] = (self.list[self.pointer] + 1) % 256
        elif command == '-':
            self.list[self.pointer] = (self.list[self.pointer] - 1) % 256

    def output(self):
        print(chr(self.list[self.pointer]), end='')

    def input(self):
        self.list[self.pointer] = ord(input())

    def cycle_working(self) -> bool:
        return self.list[self.pointer] != 0