from typing import List
from brainfuck.compiler.vm_compiler import OpCode


class VirtualMachine:
    """Виртуальная машина для выполнения байт-кода Brainfuck"""

    def __init__(self, memory_size: int = 30000):
        self.memory_size = memory_size
        self.memory: List[int] = [0] * memory_size
        self.pointer: int = 0
        self.ip: int = 0  # Instruction pointer

    def load_bytecode(self, bytecode: bytes):
        """Загружает байт-код в VM"""
        self.bytecode = list(bytecode)
        self.ip = 0

    def run(self, verbose: bool = False) -> None:
        """Выполняет байт-код"""
        max_iterations = 1_000_000
        iterations = 0

        while self.ip < len(self.bytecode):
            op = self.bytecode[self.ip]

            if op == OpCode.INC:
                self.memory[self.pointer] = (self.memory[self.pointer] + 1) % 256
                self.ip += 1

            elif op == OpCode.DEC:
                self.memory[self.pointer] = (self.memory[self.pointer] - 1) % 256
                self.ip += 1

            elif op == OpCode.RIGHT:
                self.pointer = (self.pointer + 1) % self.memory_size
                self.ip += 1

            elif op == OpCode.LEFT:
                self.pointer = (self.pointer - 1) % self.memory_size
                self.ip += 1

            elif op == OpCode.OUT:
                value = self.memory[self.pointer]
                if 32 <= value < 127:
                    print(chr(value), end='', flush=True)
                elif value == 10:
                    print('\n', end='', flush=True)
                self.ip += 1

            elif op == OpCode.INP:
                try:
                    char = input()
                    self.memory[self.pointer] = ord(char[0]) if char else 0
                except EOFError:
                    self.memory[self.pointer] = 0
                self.ip += 1

            elif op == OpCode.JMP_FWD:
                # Если ячейка = 0, прыгаем вперёд
                addr = self.bytecode[self.ip + 1] | (self.bytecode[self.ip + 2] << 8)
                if self.memory[self.pointer] == 0:
                    self.ip = addr
                else:
                    self.ip += 3

            elif op == OpCode.JMP_BCK:
                # Прыгаем назад (начало цикла)
                addr = self.bytecode[self.ip + 1] | (self.bytecode[self.ip + 2] << 8)
                self.ip = addr

            elif op == OpCode.HALT:
                if verbose:
                    print("\n[VM HALTED]")
                return

            else:
                raise RuntimeError(f"Unknown opcode: {op}")

            iterations += 1
            if iterations > max_iterations:
                raise RuntimeError(f"VM iteration limit exceeded: {max_iterations}")

    def reset(self):
        """Сброс состояния VM"""
        self.memory = [0] * self.memory_size
        self.pointer = 0
        self.ip = 0


__all__ = ["VirtualMachine"]