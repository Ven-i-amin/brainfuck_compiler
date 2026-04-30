from typing import List

from brainfuck.base import BrainfuckBackend
from middleend.brainfuck_ast import CommandNode, LoopNode, ProgramNode


class X86Compiler(BrainfuckBackend):
    def __init__(self, memory_size: int = 30000):
        self.memory_size = memory_size
        self.asm_lines: List[str] = []
        self.labels_count = 0

    def execute(self, ast: ProgramNode, output_file: str | None = None, verbose: bool = True):
        target = output_file or "brainfuck.asm"
        return self.compile(ast, output_file=target, verbose=verbose)

    def compile(self, ast: ProgramNode, output_file: str = "brainfuck.asm", verbose: bool = True):
        self.asm_lines = []
        self.labels_count = 0

        self._generate_header()
        self._generate_program(ast)
        self._generate_footer()

        with open(output_file, "w", encoding="utf-8") as file:
            file.write("\n".join(self.asm_lines))

        if verbose:
            print(f"Generated assembly file: {output_file}")
        return output_file

    def _generate_header(self) -> None:
        self.asm_lines.extend(
            [
                "section .data",
                f"    memory: times {self.memory_size} db 0",
                "",
                "section .text",
                "    global _start",
                "",
                "_start:",
                "    mov r15, memory",
                "",
            ]
        )

    def _generate_program(self, node: ProgramNode) -> None:
        self._generate_block(node.body)

    def _generate_block(self, block: List) -> None:
        for node in block:
            if isinstance(node, CommandNode):
                self._generate_command(node)
            elif isinstance(node, LoopNode):
                self._generate_loop(node)

    def _generate_command(self, cmd_node: CommandNode) -> None:
        cmd = cmd_node.command

        if cmd == "+":
            self.asm_lines.append("    inc byte [r15]")
        elif cmd == "-":
            self.asm_lines.append("    dec byte [r15]")
        elif cmd == ">":
            self.asm_lines.append("    inc r15")
        elif cmd == "<":
            self.asm_lines.append("    dec r15")
        elif cmd == ".":
            self.asm_lines.extend(
                [
                    "    mov rax, 1",
                    "    mov rdi, 1",
                    "    mov rsi, r15",
                    "    mov rdx, 1",
                    "    syscall",
                ]
            )
        elif cmd == ",":
            self.asm_lines.extend(
                [
                    "    mov rax, 0",
                    "    mov rdi, 0",
                    "    mov rsi, r15",
                    "    mov rdx, 1",
                    "    syscall",
                ]
            )
        elif cmd.startswith("optimized:add:"):
            self.asm_lines.append(f"    add byte [r15], {int(cmd.split(':')[2])}")
        elif cmd.startswith("optimized:sub:"):
            self.asm_lines.append(f"    sub byte [r15], {int(cmd.split(':')[2])}")
        elif cmd.startswith("optimized:right:"):
            self.asm_lines.append(f"    add r15, {int(cmd.split(':')[2])}")
        elif cmd.startswith("optimized:left:"):
            self.asm_lines.append(f"    sub r15, {int(cmd.split(':')[2])}")
        elif cmd == "optimized:clear":
            self.asm_lines.append("    mov byte [r15], 0")

        self.asm_lines.append("")

    def _generate_loop(self, loop_node: LoopNode) -> None:
        label_start = f"loop_{self.labels_count}_start"
        label_end = f"loop_{self.labels_count}_end"
        self.labels_count += 1

        self.asm_lines.extend(
            [
                f"{label_start}:",
                "    cmp byte [r15], 0",
                f"    je {label_end}",
                "",
            ]
        )

        self._generate_block(loop_node.body)

        self.asm_lines.extend(
            [
                f"    jmp {label_start}",
                f"{label_end}:",
                "",
            ]
        )

    def _generate_footer(self) -> None:
        self.asm_lines.extend(
            [
                "    mov rax, 60",
                "    mov rdi, 0",
                "    syscall",
            ]
        )


__all__ = ["X86Compiler"]
