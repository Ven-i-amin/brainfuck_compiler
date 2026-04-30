from dataclasses import dataclass, field
from typing import List, Optional, Set
from enum import Enum


class Severity(Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


@dataclass
class SemanticDiagnostic:
    """Диагностическое сообщение семантического анализатора"""
    severity: Severity
    message: str
    line: Optional[int] = None
    column: Optional[int] = None

    def __str__(self):
        loc = f" at line {self.line}" if self.line else ""
        return f"{self.severity.value}{loc}: {self.message}"


class SemanticAnalyzer:
    """Семантический анализатор AST"""

    def __init__(self):
        self.diagnostics: List[SemanticDiagnostic] = []
        self.max_loop_depth = 100
        self.current_loop_depth = 0
        self.all_commands: Set[str] = {'>', '<', '+', '-', '.', ','}

    def analyze(self, ast) -> bool:
        """
        Запуск семантического анализа
        Возвращает True если нет критических ошибок
        """
        self.diagnostics.clear()
        self.current_loop_depth = 0

        # Анализ программы
        self._analyze_program(ast)

        # Дополнительные проверки
        self._check_infinite_loops(ast)
        self._check_dead_code(ast)

        # Вывод отчёта
        self._print_report()

        return not any(d.severity == Severity.ERROR for d in self.diagnostics)

    def _analyze_program(self, node):
        """Анализ корневого узла программы"""
        if hasattr(node, 'body'):
            for stmt in node.body:
                self._analyze_statement(stmt)

    def _analyze_statement(self, stmt):
        """Анализ отдельной инструкции"""
        from brainfuck_ast import CommandNode, LoopNode

        if isinstance(stmt, CommandNode):
            self._analyze_command(stmt)
        elif isinstance(stmt, LoopNode):
            self._analyze_loop(stmt)

    def _analyze_command(self, cmd_node):
        """Семантическая проверка команды"""
        cmd = cmd_node.command

        # Проверка на неизвестную команду
        if cmd not in self.all_commands:
            self.diagnostics.append(SemanticDiagnostic(
                Severity.ERROR,
                f"Unknown command: '{cmd}' - допустимы только: {', '.join(self.all_commands)}"
            ))

    def _analyze_loop(self, loop_node):
        """Анализ цикла"""
        self.current_loop_depth += 1

        # Проверка глубины вложенности
        if self.current_loop_depth > self.max_loop_depth:
            self.diagnostics.append(SemanticDiagnostic(
                Severity.WARNING,
                f"Слишком глубокая вложенность циклов ({self.current_loop_depth}) > {self.max_loop_depth}"
            ))

        # Проверка пустого цикла
        if not loop_node.body:
            self.diagnostics.append(SemanticDiagnostic(
                Severity.WARNING,
                "Пустой цикл (может привести к бесконечному выполнению)"
            ))

        # Рекурсивный анализ тела цикла
        for stmt in loop_node.body:
            self._analyze_statement(stmt)

        self.current_loop_depth -= 1

    def _check_infinite_loops(self, ast):
        """Поиск потенциально бесконечных циклов"""
        from brainfuck_ast import LoopNode, CommandNode

        def find_infinite_loops(node):
            if isinstance(node, LoopNode):
                # Простая проверка: цикл без изменения текущей ячейки
                has_cell_modification = any(
                    isinstance(cmd, CommandNode) and cmd.command in ['+', '-']
                    for cmd in node.body
                )
                has_pointer_move = any(
                    isinstance(cmd, CommandNode) and cmd.command in ['>', '<']
                    for cmd in node.body
                )

                if not has_cell_modification and not has_pointer_move:
                    self.diagnostics.append(SemanticDiagnostic(
                        Severity.WARNING,
                        "Цикл не изменяет состояние (возможен бесконечный цикл)"
                    ))

                # Рекурсивная проверка вложенных циклов
                for stmt in node.body:
                    find_infinite_loops(stmt)
            elif hasattr(node, 'body'):
                for stmt in node.body:
                    find_infinite_loops(stmt)

        find_infinite_loops(ast)

    def _check_dead_code(self, ast):
        """Поиск недостижимого кода"""
        from brainfuck_ast import LoopNode, CommandNode

        # Простая проверка: код после бесконечного цикла
        def check_dead(node):
            if isinstance(node, LoopNode):
                if not node.body:
                    # Пустой цикл может быть бесконечным
                    pass
        # Более сложный анализ можно добавить позже

    def _print_report(self):
        """Вывод отчёта о семантическом анализе"""
        if not self.diagnostics:
            print("\nСемантический анализ: ошибок не обнаружено")
            return

        errors = [d for d in self.diagnostics if d.severity == Severity.ERROR]
        warnings = [d for d in self.diagnostics if d.severity == Severity.WARNING]

        print(f"\nОтчёт семантического анализа:")
        print("_" * 50)

        for diag in self.diagnostics:
            print(f"  {diag}")

        print("_" * 50)
        if errors:
            print(f"  Ошибок: {len(errors)}")
        if warnings:
            print(f"  Предупреждений: {len(warnings)}")
        print("_" * 50)