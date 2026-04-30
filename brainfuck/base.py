from abc import ABC, abstractmethod

from middleend.brainfuck_ast import ProgramNode


class BrainfuckBackend(ABC):
    @abstractmethod
    def execute(self, ast: ProgramNode, output_file: str | None = None, verbose: bool = True):
        raise NotImplementedError
