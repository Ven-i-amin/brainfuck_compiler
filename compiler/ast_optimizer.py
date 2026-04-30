# compiler/ast_optimizer.py
from typing import List, Optional
from brainfuck_ast import ProgramNode, LoopNode, CommandNode


class ASTOptimizer:
    def __init__(self):
        self.optimization_stats = {
            'fused_inc': 0,
            'fused_move': 0,
            'removed_empty_loops': 0,
            'simplified_clear': 0,
        }
        self.optimization_level = 2

    def optimize(self, ast: ProgramNode) -> ProgramNode:
        print("\n⚡ Типозависимый анализ и оптимизация AST...")
        optimized = self._optimize_node(ast)
        self._print_stats()
        return optimized

    def _optimize_node(self, node):
        from brainfuck_ast import ProgramNode, LoopNode, CommandNode

        if isinstance(node, ProgramNode):
            return self._optimize_program(node)
        elif isinstance(node, LoopNode):
            return self._optimize_loop(node)
        else:
            return node

    def _optimize_program(self, node: ProgramNode) -> ProgramNode:
        optimized_body = self._optimize_block(node.body)
        return ProgramNode(optimized_body)

    def _optimize_loop(self, node: LoopNode) -> Optional[LoopNode]:
        """Оптимизация циклов"""
        # Рекурсивно оптимизируем тело цикла
        optimized_body = self._optimize_block(node.body)

        # Удаляем пустые циклы
        if not optimized_body:
            self.optimization_stats['removed_empty_loops'] += 1
            return None

        # Оптимизация: Цикл-очистка [-]
        if len(optimized_body) == 1:
            cmd = optimized_body[0]
            if isinstance(cmd, CommandNode):
                if cmd.command == '-':
                    self.optimization_stats['simplified_clear'] += 1
                    return CommandNode('optimized:clear')

        return LoopNode(optimized_body)

    def _optimize_block(self, block: List) -> List:
        """Оптимизация блока команд"""
        if self.optimization_level == 0:
            return block

        # Рекурсивно оптимизируем каждый узел
        optimized = []
        for node in block:
            opt_node = self._optimize_node(node)
            if opt_node is not None:
                optimized.append(opt_node)

        # Свёртка последовательных команд (уровень 1+)
        if self.optimization_level >= 1:
            optimized = self._fuse_commands(optimized)

        return optimized

    def _fuse_commands(self, block: List) -> List:
        """
        Сворачивает ТОЛЬКО последовательные команды одного типа
        БЕЗ компенсации противоположных команд внутри циклов
        """
        if not block:
            return []

        fused = []
        i = 0

        while i < len(block):
            node = block[i]

            # Если это не команда - добавляем как есть
            if not isinstance(node, CommandNode):
                fused.append(node)
                i += 1
                continue

            cmd = node.command

            # Команды, которые НЕ свёртываются
            if cmd in ['.', ','] or cmd.startswith('optimized:clear'):
                fused.append(node)
                i += 1
                continue

            # Свёртка + и -
            if cmd in ['+', '-']:
                delta = 1 if cmd == '+' else -1
                j = i + 1

                # Собираем последовательные + и -
                while j < len(block):
                    if isinstance(block[j], CommandNode):
                        next_cmd = block[j].command
                        if next_cmd == '+':
                            delta += 1
                            j += 1
                        elif next_cmd == '-':
                            delta -= 1
                            j += 1
                        else:
                            break
                    else:
                        break

                # Добавляем результат
                if delta != 0:
                    if delta == 1:
                        fused.append(CommandNode('+'))
                    elif delta == -1:
                        fused.append(CommandNode('-'))
                    elif delta > 0:
                        fused.append(CommandNode(f'optimized:add:{delta}'))
                        self.optimization_stats['fused_inc'] += (j - i - 1)
                    else:
                        fused.append(CommandNode(f'optimized:sub:{-delta}'))
                        self.optimization_stats['fused_inc'] += (j - i - 1)

                i = j
                continue

            # Свёртка > и <
            if cmd in ['>', '<']:
                delta = 1 if cmd == '>' else -1
                j = i + 1

                # Собираем последовательные > и <
                while j < len(block):
                    if isinstance(block[j], CommandNode):
                        next_cmd = block[j].command
                        if next_cmd == '>':
                            delta += 1
                            j += 1
                        elif next_cmd == '<':
                            delta -= 1
                            j += 1
                        else:
                            break
                    else:
                        break

                # Добавляем результат
                if delta != 0:
                    if delta == 1:
                        fused.append(CommandNode('>'))
                    elif delta == -1:
                        fused.append(CommandNode('<'))
                    elif delta > 0:
                        fused.append(CommandNode(f'optimized:right:{delta}'))
                        self.optimization_stats['fused_move'] += (j - i - 1)
                    else:
                        fused.append(CommandNode(f'optimized:left:{-delta}'))
                        self.optimization_stats['fused_move'] += (j - i - 1)

                i = j
                continue

            # Другие команды - добавляем как есть
            fused.append(node)
            i += 1

        return fused

    def _print_stats(self):
        """Вывод статистики оптимизаций"""
        total_optimizations = sum(self.optimization_stats.values())

        if total_optimizations > 0:
            print(f"\nСтатистика оптимизаций:")
            if self.optimization_stats['fused_inc'] > 0:
                print(f"  Свёрнуто команд '+/-': {self.optimization_stats['fused_inc']}")
            if self.optimization_stats['fused_move'] > 0:
                print(f"  Свёрнуто команд '>/<': {self.optimization_stats['fused_move']}")
            if self.optimization_stats['simplified_clear'] > 0:
                print(f"  Упрощено циклов-очистки '[-]': {self.optimization_stats['simplified_clear']}")
            if self.optimization_stats['removed_empty_loops'] > 0:
                print(f"  Удалено пустых циклов: {self.optimization_stats['removed_empty_loops']}")
            print(f"  Всего оптимизаций: {total_optimizations}")
        else:
            print("\n Оптимизаций не выполнено")