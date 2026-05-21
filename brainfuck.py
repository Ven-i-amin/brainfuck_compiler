import sys
import io
from brainfuck_ast import ProgramNode, LoopNode, CommandNode


class brainfuck:
    def __init__(self):
        self.memory = [0] * 30000
        self.pointer = 0

    def move_pointer(self, direction):
        if direction == '>':
            self.pointer += 1
        elif direction == '<':
            self.pointer -= 1

    def change_value(self, command):
        if command == '+':
            self.memory[self.pointer] = (self.memory[self.pointer] + 1) % 256
        elif command == '-':
            self.memory[self.pointer] = (self.memory[self.pointer] - 1) % 256

    def output(self):
        value = self.memory[self.pointer]
        if 32 <= value < 127:
            print(chr(value), end='', flush=True)
        elif value == 10:
            print('\n', end='', flush=True)
        elif value == 13:
            print('\r', end='', flush=True)
        elif value == 9:
            print('\t', end='', flush=True)

    def input_char(self):
        try:
            char = input()
            if char:
                self.memory[self.pointer] = ord(char[0])
            else:
                self.memory[self.pointer] = 0
        except EOFError:
            self.memory[self.pointer] = 0

    def cycle_working(self) -> bool:
        return self.memory[self.pointer] != 0
    
    def execute_ast(self, ast, max_iterations=1000000):
        if isinstance(ast, ProgramNode):
            for child in ast.body:
                self.execute_ast(child, max_iterations)
        
        elif isinstance(ast, LoopNode):
            iteration = 0
            while self.cycle_working():
                for child in ast.body:
                    self.execute_ast(child, max_iterations)
                iteration += 1
                if iteration > max_iterations:
                    print(f"\n[ERROR: Лимит итераций ({max_iterations})]", file=sys.stderr)
                    break
        
        elif isinstance(ast, CommandNode):
            cmd = ast.command
            if cmd in ['<', '>']:
                self.move_pointer(cmd)
            elif cmd in ['+', '-']:
                self.change_value(cmd)
            elif cmd == '.':
                self.output()
            elif cmd == ',':
                self.input_char()
    
    def reset(self):
        self.memory = [0] * 30000
        self.pointer = 0