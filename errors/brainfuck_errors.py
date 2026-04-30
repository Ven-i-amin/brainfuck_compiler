from dataclasses import dataclass
from enum import Enum
from typing import List


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

    def check_brackets(self, code: str) -> bool:
        stack = []
        lines = code.split("\n")

        for line_num, line in enumerate(lines, 1):
            for col_num, char in enumerate(line, 1):
                if char == "[":
                    stack.append((line_num, col_num))
                elif char == "]":
                    if not stack:
                        self.errors.append(
                            SyntaxError(
                                message="Unmatched closing bracket ']'",
                                line=line_num,
                                column=col_num,
                            )
                        )
                        return False
                    stack.pop()

        if stack:
            line, col = stack[0]
            self.errors.append(
                SyntaxError(
                    message="Unmatched opening bracket '[' (missing closing ']')",
                    line=line,
                    column=col,
                )
            )
            return False

        return True

    def check_empty_loops(self, code: str) -> bool:
        lines = code.split("\n")
        has_error = False

        for line_num, line in enumerate(lines, 1):
            i = 0
            while i < len(line) - 1:
                if line[i] == "[" and line[i + 1] == "]":
                    self.errors.append(
                        SyntaxError(
                            message="Empty loop '[]'",
                            line=line_num,
                            column=i + 1,
                            severity=ErrorSeverity.WARNING,
                        )
                    )
                    has_error = True
                i += 1

        return not has_error

    def check_invalid_chars(self, code: str) -> bool:
        valid_chars = set("><+-.,[]")
        lines = code.split("\n")
        has_error = False

        for line_num, line in enumerate(lines, 1):
            for col_num, char in enumerate(line, 1):
                if char not in valid_chars and not char.isspace():
                    self.errors.append(
                        SyntaxError(
                            message=f"Invalid character '{char}'",
                            line=line_num,
                            column=col_num,
                            severity=ErrorSeverity.WARNING,
                        )
                    )
                    has_error = True

        return not has_error

    def check_all(self, code: str) -> bool:
        self.errors = []
        self.check_brackets(code)
        self.check_empty_loops(code)
        self.check_invalid_chars(code)
        return len([error for error in self.errors if error.severity == ErrorSeverity.ERROR]) == 0

    def print_errors(self, verbose: bool = True):
        if not self.errors:
            if verbose:
                print("No syntax errors found")
            return

        print(f"\nFound issues: {len(self.errors)}")
        for error in self.errors:
            prefix = "[ERROR]" if error.severity == ErrorSeverity.ERROR else "[WARNING]"
            print(f"{prefix} Line {error.line}:{error.column} - {error.message}")
