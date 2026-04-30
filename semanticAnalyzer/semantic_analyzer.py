from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple
from brainfuck_ast import ProgramNode, LoopNode, CommandNode, AstNode


@dataclass
class SemanticWarning:
    """Предупреждение семантического анализатора"""
    message: str
    node_type: str
    path: str
    severity: str = "WARNING"


@dataclass
class SemanticError:
    """Ошибка семантического анализатора"""
    message: str
    node_type: str
    path: str
    severity: str = "ERROR"


class SemanticAnalyzer:
    """Семантический анализатор для Brainfuck"""
    
    def __init__(self, max_memory: int = 30000):
        self.max_memory = max_memory
        self.warnings: List[SemanticWarning] = []
        self.errors: List[SemanticError] = []
    
    def analyze(self, ast: ProgramNode) -> bool:
        """
        Запускает семантический анализ.
        Возвращает True, если нет критических ошибок.
        """
        self.warnings = []
        self.errors = []
        
        self._check_node(ast, "")
        
        self._print_results()
        
        return len(self.errors) == 0
    
    def _check_node(self, node: AstNode, path: str):
        """Рекурсивно проверяет узел AST"""
        
        if isinstance(node, ProgramNode):
            for i, child in enumerate(node.body):
                self._check_node(child, f"{path}prog[{i}]")
        
        elif isinstance(node, LoopNode):
            # Пустой цикл
            if not node.body:
                self.errors.append(SemanticError(
                    message="Пустой цикл [] не выполняет никаких действий",
                    node_type="LoopNode",
                    path=path
                ))
            else:
                #цикл без изменения текущей ячейки
                if not self._loop_modifies_current_cell(node.body):
                    self.warnings.append(SemanticWarning(
                        message="Цикл может быть бесконечным (не изменяет текущую ячейку)",
                        node_type="LoopNode",
                        path=path
                    ))
                
                # Рекурсивная проверка вложенных узлов
                for i, child in enumerate(node.body):
                    self._check_node(child, f"{path}loop[{i}]")
        
        elif isinstance(node, CommandNode):
            cmd = node.command
            
            #Подозрительные последовательности
            if cmd in ['<', '>']:
                # Можно добавить проверку на выход за границы,
                # но для этого нужно отслеживать позицию указателя
                pass
    
    def _loop_modifies_current_cell(self, body: List[AstNode], depth: int = 0) -> bool:
        """
        Проверяет, изменяет ли цикл текущую ячейку памяти.
        Если нет — цикл потенциально бесконечный.
        """
        pointer_offset = 0
        
        for node in body:
            if isinstance(node, CommandNode):
                cmd = node.command
                
                if cmd == '>' :
                    pointer_offset += 1
                elif cmd == '<':
                    pointer_offset -= 1
                elif cmd in ['+', '-'] and pointer_offset == 0:
                    # Изменение текущей ячейки
                    return True
            elif isinstance(node, LoopNode):
                # Рекурсивная проверка вложенного цикла
                if self._loop_modifies_current_cell(node.body, depth + 1):
                    return True
        
        return False
    
    def _print_results(self):
        """Выводит результаты анализа в консоль"""
        
        if not self.errors and not self.warnings:
            print("\nСемантический анализ пройден успешно!")
            return
        
        print("\n" + "=" * 60)
        print("РЕЗУЛЬТАТЫ СЕМАНТИЧЕСКОГО АНАЛИЗА")
        print("=" * 60)
        
        if self.errors:
            print(f"\n!!! ОШИБКИ !!! ({len(self.errors)}):")
            for err in self.errors:
                print(f"  [{err.severity}] {err.message}")
                print(f"    Путь: {err.path}")
                print(f"    Узел: {err.node_type}")
        
        if self.warnings:
            print(f"\n! ПРЕДУПРЕЖДЕНИЯ ! ({len(self.warnings)}):")
            for warn in self.warnings:
                print(f"  [{warn.severity}] {warn.message}")
                print(f"    Путь: {warn.path}")
                print(f"    Узел: {warn.node_type}")
        
        print("=" * 60)