from typing import List, Optional

from middleend.brainfuck_ast import CommandNode, LoopNode, ProgramNode


class ASTOptimizer:
    def __init__(self):
        self.optimization_stats = {
            "fused_inc": 0,
            "fused_move": 0,
            "removed_empty_loops": 0,
            "simplified_clear": 0,
        }
        self.optimization_level = 2

    def optimize(self, ast: ProgramNode, verbose: bool = True) -> ProgramNode:
        optimized = self._optimize_node(ast)
        self._print_stats(verbose)
        return optimized

    def _optimize_node(self, node):
        if isinstance(node, ProgramNode):
            return self._optimize_program(node)
        if isinstance(node, LoopNode):
            return self._optimize_loop(node)
        return node

    def _optimize_program(self, node: ProgramNode) -> ProgramNode:
        optimized_body = self._optimize_block(node.body)
        return ProgramNode(optimized_body)

    def _optimize_loop(self, node: LoopNode) -> Optional[LoopNode]:
        optimized_body = self._optimize_block(node.body)

        if not optimized_body:
            self.optimization_stats["removed_empty_loops"] += 1
            return None

        if len(optimized_body) == 1:
            cmd = optimized_body[0]
            if isinstance(cmd, CommandNode) and cmd.command == "-":
                self.optimization_stats["simplified_clear"] += 1
                return CommandNode("optimized:clear")

        return LoopNode(optimized_body)

    def _optimize_block(self, block: List) -> List:
        if self.optimization_level == 0:
            return block

        optimized = []
        for node in block:
            opt_node = self._optimize_node(node)
            if opt_node is not None:
                optimized.append(opt_node)

        if self.optimization_level >= 1:
            optimized = self._fuse_commands(optimized)

        return optimized

    def _fuse_commands(self, block: List) -> List:
        if not block:
            return []

        fused = []
        i = 0

        while i < len(block):
            node = block[i]

            if not isinstance(node, CommandNode):
                fused.append(node)
                i += 1
                continue

            cmd = node.command

            if cmd in [".", ","] or cmd.startswith("optimized:clear"):
                fused.append(node)
                i += 1
                continue

            if cmd in ["+", "-"]:
                delta = 1 if cmd == "+" else -1
                j = i + 1

                while j < len(block):
                    if isinstance(block[j], CommandNode):
                        next_cmd = block[j].command
                        if next_cmd == "+":
                            delta += 1
                            j += 1
                        elif next_cmd == "-":
                            delta -= 1
                            j += 1
                        else:
                            break
                    else:
                        break

                if delta != 0:
                    if delta == 1:
                        fused.append(CommandNode("+"))
                    elif delta == -1:
                        fused.append(CommandNode("-"))
                    elif delta > 0:
                        fused.append(CommandNode(f"optimized:add:{delta}"))
                        self.optimization_stats["fused_inc"] += j - i - 1
                    else:
                        fused.append(CommandNode(f"optimized:sub:{-delta}"))
                        self.optimization_stats["fused_inc"] += j - i - 1

                i = j
                continue

            if cmd in [">", "<"]:
                delta = 1 if cmd == ">" else -1
                j = i + 1

                while j < len(block):
                    if isinstance(block[j], CommandNode):
                        next_cmd = block[j].command
                        if next_cmd == ">":
                            delta += 1
                            j += 1
                        elif next_cmd == "<":
                            delta -= 1
                            j += 1
                        else:
                            break
                    else:
                        break

                if delta != 0:
                    if delta == 1:
                        fused.append(CommandNode(">"))
                    elif delta == -1:
                        fused.append(CommandNode("<"))
                    elif delta > 0:
                        fused.append(CommandNode(f"optimized:right:{delta}"))
                        self.optimization_stats["fused_move"] += j - i - 1
                    else:
                        fused.append(CommandNode(f"optimized:left:{-delta}"))
                        self.optimization_stats["fused_move"] += j - i - 1

                i = j
                continue

            fused.append(node)
            i += 1

        return fused

    def _print_stats(self, verbose: bool):
        if not verbose:
            return

        total_optimizations = sum(self.optimization_stats.values())

        if total_optimizations > 0:
            print("\nOptimization stats:")
            if self.optimization_stats["fused_inc"] > 0:
                print(f"  Fused '+/-' commands: {self.optimization_stats['fused_inc']}")
            if self.optimization_stats["fused_move"] > 0:
                print(f"  Fused '>/< commands: {self.optimization_stats['fused_move']}")
            if self.optimization_stats["simplified_clear"] > 0:
                print(f"  Simplified '[-]' clear loops: {self.optimization_stats['simplified_clear']}")
            if self.optimization_stats["removed_empty_loops"] > 0:
                print(f"  Removed empty loops: {self.optimization_stats['removed_empty_loops']}")
            print(f"  Total optimizations: {total_optimizations}")
        else:
            print("\nNo optimizations applied")
