from dataclasses import dataclass
from typing import List
from enum import Enum


class ErrorSeverity(Enum):
    ERROR = "ERROR"
    WARNING = "WARNING"


@dataclass
class SyntaxError:
    message: str
    line: int
    column: int
    severity: ErrorSeverity = ErrorSeverity.ERROR


class SyntaxChecker:
    def __init__(self):
        self.errors: List[SyntaxError] = []

    #Лишние скобки
    def check_brackets(self, code: str) -> bool:
        stack = []
        lines = code.split('\n')

        for line_num, line in enumerate(lines, 1):
            for col_num, char in enumerate(line, 1):
                if char == '[':
                    stack.append((line_num, col_num))
                elif char == ']':
                    if not stack:
                        self.errors.append(SyntaxError(
                            message="Незакрытая скобка ']'",
                            line=line_num,
                            column=col_num
                        ))
                        return False
                    stack.pop()

        if stack:
            line, col = stack[0]
            self.errors.append(SyntaxError(
                message="Неоткрытая скобка '[' (нет закрывающей ']')",
                line=line,
                column=col
            ))
            return False

        return True

    #Для пустых циклов
    def check_empty_loops(self, code: str) -> bool:
        lines = code.split('\n')
        has_error = False

        for line_num, line in enumerate(lines, 1):
            i = 0
            while i < len(line) - 1:
                if line[i] == '[' and line[i + 1] == ']':
                    self.errors.append(SyntaxError(
                        message="Пустой цикл '[]'",
                        line=line_num,
                        column=i + 1,
                        severity=ErrorSeverity.WARNING
                    ))
                    has_error = True
                i += 1

        return not has_error
    #На недопустимые символы
    def check_invalid_chars(self, code: str) -> bool:
        valid_chars = set('><+-.,[]')
        lines = code.split('\n')
        has_error = False

        for line_num, line in enumerate(lines, 1):
            for col_num, char in enumerate(line, 1):
                if char not in valid_chars and not char.isspace():
                    self.errors.append(SyntaxError(
                        message=f"Недопустимый символ '{char}'",
                        line=line_num,
                        column=col_num,
                        severity=ErrorSeverity.WARNING
                    ))
                    has_error = True

        return not has_error

    def check_all(self, code: str) -> bool:
        self.errors = []
        self.check_brackets(code)
        self.check_empty_loops(code)
        self.check_invalid_chars(code)
        return len([e for e in self.errors if e.severity == ErrorSeverity.ERROR]) == 0

    def print_errors(self):
        if not self.errors:
            print("Синтаксических ошибок не найдено")
            return

        print(f"\n Найдено ошибок: {len(self.errors)}")
        for error in self.errors:
            prefix = "[ERROR]" if error.severity == ErrorSeverity.ERROR else "[WARNING]"
            print(f"{prefix} Строка {error.line}:{error.column} - {error.message}")