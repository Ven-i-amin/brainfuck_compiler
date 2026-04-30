import sys

from brainfuck.base import BrainfuckBackend
from middleend.brainfuck_ast import CommandNode, LoopNode, ProgramNode


class BrainfuckInterpreter(BrainfuckBackend):
    def __init__(self, memory_size: int = 30000):
        self.memory_size = memory_size
        self.reset()

    def execute(self, ast: ProgramNode, output_file: str | None = None, verbose: bool = True):
        del output_file
        self.execute_ast(ast)
        return None

    def move_pointer(self, direction: str, steps: int = 1) -> None:
        if direction == ">":
            self.pointer += steps
        elif direction == "<":
            self.pointer -= steps

        if self.pointer < 0 or self.pointer >= len(self.memory):
            raise RuntimeError(f"Memory pointer out of bounds: {self.pointer}")

    def change_value(self, delta: int) -> None:
        self.memory[self.pointer] = (self.memory[self.pointer] + delta) % 256

    def output(self) -> None:
        sys.stdout.write(chr(self.memory[self.pointer]))
        sys.stdout.flush()

    def input_char(self) -> None:
        try:
            value = input()
        except EOFError:
            value = ""
        self.memory[self.pointer] = ord(value[0]) if value else 0

    def cycle_working(self) -> bool:
        return self.memory[self.pointer] != 0

    def execute_ast(self, ast, max_iterations: int = 1_000_000) -> None:
        if isinstance(ast, ProgramNode):
            for child in ast.body:
                self.execute_ast(child, max_iterations)
            return

        if isinstance(ast, LoopNode):
            iteration = 0
            while self.cycle_working():
                for child in ast.body:
                    self.execute_ast(child, max_iterations)
                iteration += 1
                if iteration > max_iterations:
                    raise RuntimeError(f"Iteration limit exceeded: {max_iterations}")
            return

        if isinstance(ast, CommandNode):
            self._execute_command(ast.command)

    def _execute_command(self, cmd: str) -> None:
        if cmd == ".":
            self.output()
        elif cmd == ",":
            self.input_char()
        elif cmd == "+":
            self.change_value(1)
        elif cmd == "-":
            self.change_value(-1)
        elif cmd == ">":
            self.move_pointer(">")
        elif cmd == "<":
            self.move_pointer("<")
        elif cmd.startswith("optimized:add:"):
            self.change_value(int(cmd.split(":")[2]))
        elif cmd.startswith("optimized:sub:"):
            self.change_value(-int(cmd.split(":")[2]))
        elif cmd.startswith("optimized:right:"):
            self.move_pointer(">", int(cmd.split(":")[2]))
        elif cmd.startswith("optimized:left:"):
            self.move_pointer("<", int(cmd.split(":")[2]))
        elif cmd == "optimized:clear":
            self.memory[self.pointer] = 0
        else:
            raise ValueError(f"Unknown command: {cmd}")

    def reset(self) -> None:
        self.memory = [0] * self.memory_size
        self.pointer = 0


brainfuck = BrainfuckInterpreter

__all__ = ["BrainfuckInterpreter", "brainfuck"]
