from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Set


class Severity(Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


@dataclass
class SemanticDiagnostic:
    severity: Severity
    message: str
    line: Optional[int] = None
    column: Optional[int] = None

    def __str__(self):
        loc = f" at line {self.line}" if self.line else ""
        return f"{self.severity.value}{loc}: {self.message}"


class SemanticAnalyzer:
    def __init__(self):
        self.diagnostics: List[SemanticDiagnostic] = []
        self.max_loop_depth = 100
        self.current_loop_depth = 0
        self.all_commands: Set[str] = {">", "<", "+", "-", ".", ","}

    def analyze(self, ast, verbose: bool = True) -> bool:
        self.diagnostics.clear()
        self.current_loop_depth = 0

        self._analyze_program(ast)
        self._check_infinite_loops(ast)
        self._check_dead_code(ast)
        self._print_report(verbose)

        return not any(d.severity == Severity.ERROR for d in self.diagnostics)

    def _analyze_program(self, node):
        if hasattr(node, "body"):
            for stmt in node.body:
                self._analyze_statement(stmt)

    def _analyze_statement(self, stmt):
        from middleend.brainfuck_ast import CommandNode, LoopNode

        if isinstance(stmt, CommandNode):
            self._analyze_command(stmt)
        elif isinstance(stmt, LoopNode):
            self._analyze_loop(stmt)

    def _analyze_command(self, cmd_node):
        cmd = cmd_node.command

        if cmd not in self.all_commands:
            self.diagnostics.append(
                SemanticDiagnostic(
                    Severity.ERROR,
                    f"Unknown command: '{cmd}' - allowed commands: {', '.join(sorted(self.all_commands))}",
                )
            )

    def _analyze_loop(self, loop_node):
        self.current_loop_depth += 1

        if self.current_loop_depth > self.max_loop_depth:
            self.diagnostics.append(
                SemanticDiagnostic(
                    Severity.WARNING,
                    f"Loop nesting is too deep ({self.current_loop_depth}) > {self.max_loop_depth}",
                )
            )

        if not loop_node.body:
            self.diagnostics.append(
                SemanticDiagnostic(
                    Severity.WARNING,
                    "Empty loop detected (may lead to an infinite loop)",
                )
            )

        for stmt in loop_node.body:
            self._analyze_statement(stmt)

        self.current_loop_depth -= 1

    def _check_infinite_loops(self, ast):
        from middleend.brainfuck_ast import CommandNode, LoopNode

        def find_infinite_loops(node):
            if isinstance(node, LoopNode):
                has_cell_modification = any(
                    isinstance(cmd, CommandNode) and cmd.command in ["+", "-"]
                    for cmd in node.body
                )
                has_pointer_move = any(
                    isinstance(cmd, CommandNode) and cmd.command in [">", "<"]
                    for cmd in node.body
                )

                if not has_cell_modification and not has_pointer_move:
                    self.diagnostics.append(
                        SemanticDiagnostic(
                            Severity.WARNING,
                            "Loop does not change program state (possible infinite loop)",
                        )
                    )

                for stmt in node.body:
                    find_infinite_loops(stmt)
            elif hasattr(node, "body"):
                for stmt in node.body:
                    find_infinite_loops(stmt)

        find_infinite_loops(ast)

    def _check_dead_code(self, ast):
        from middleend.brainfuck_ast import LoopNode

        def check_dead(node):
            if isinstance(node, LoopNode):
                if not node.body:
                    pass

        check_dead(ast)

    def _print_report(self, verbose: bool):
        if not self.diagnostics:
            if verbose:
                print("\nSemantic analysis: no issues found")
            return

        errors = [diagnostic for diagnostic in self.diagnostics if diagnostic.severity == Severity.ERROR]
        warnings = [diagnostic for diagnostic in self.diagnostics if diagnostic.severity == Severity.WARNING]

        if verbose or errors:
            print("\nSemantic analysis report:")
            print("_" * 50)

            for diagnostic in self.diagnostics:
                print(f"  {diagnostic}")

            print("_" * 50)
            if errors:
                print(f"  Errors: {len(errors)}")
            if warnings:
                print(f"  Warnings: {len(warnings)}")
            print("_" * 50)
