# compiler/x86_compiler.py
from typing import List
from brainfuck_ast import ProgramNode, LoopNode, CommandNode


class X86Compiler:
    def __init__(self):
        self.asm_lines: List[str] = []
        self.labels_count = 0
        self.memory_size = 30000

    def compile(self, ast: ProgramNode, output_file: str = "brainfuck.asm"):
        self.asm_lines = []
        self.labels_count = 0

        self._generate_header()
        self._generate_program(ast)
        self._generate_footer()

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(self.asm_lines))

        print(f"  Сгенерирован файл: {output_file}")
        return output_file

    def _generate_header(self):
        self.asm_lines.extend([
            "section .data",
            "    memory: times 30000 db 0",
            "",
            "section .text",
            "    global _start",
            "",
            "_start:",
            "    mov r15, memory      ; r15 = указатель на текущую ячейку памяти",
            ""
        ])

    def _generate_program(self, node: ProgramNode):
        self._generate_block(node.body)

    def _generate_block(self, block: List):
        for node in block:
            if isinstance(node, CommandNode):
                self._generate_command(node)
            elif isinstance(node, LoopNode):
                self._generate_loop(node)

    def _generate_command(self, cmd_node: CommandNode):
        cmd = cmd_node.command

        if cmd == '+':
            self.asm_lines.append("    inc byte [r15]")
        elif cmd == '-':
            self.asm_lines.append("    dec byte [r15]")
        elif cmd == '>':
            self.asm_lines.append("    inc r15")
        elif cmd == '<':
            self.asm_lines.append("    dec r15")
        elif cmd == '.':
            # Вывод символа
            self.asm_lines.extend([
                "    mov rax, 1       ; sys_write",
                "    mov rdi, 1       ; stdout",
                "    mov rsi, r15     ; адрес текущей ячейки",
                "    mov rdx, 1       ; длина 1 байт",
                "    syscall"
            ])
        elif cmd == ',':
            # Ввод символа
            self.asm_lines.extend([
                "    mov rax, 0       ; sys_read",
                "    mov rdi, 0       ; stdin",
                "    mov rsi, r15     ; адрес текущей ячейки",
                "    mov rdx, 1       ; длина 1 байт",
                "    syscall"
            ])
        elif cmd.startswith('optimized:add:'):
            value = int(cmd.split(':')[2])
            self.asm_lines.append(f"    add byte [r15], {value}")
        elif cmd.startswith('optimized:sub:'):
            value = int(cmd.split(':')[2])
            self.asm_lines.append(f"    sub byte [r15], {value}")
        elif cmd.startswith('optimized:right:'):
            value = int(cmd.split(':')[2])
            self.asm_lines.append(f"    add r15, {value}")
        elif cmd.startswith('optimized:left:'):
            value = int(cmd.split(':')[2])
            self.asm_lines.append(f"    sub r15, {value}")
        elif cmd == 'optimized:clear':
            self.asm_lines.append("    mov byte [r15], 0")

        self.asm_lines.append("")

    def _generate_loop(self, loop_node: LoopNode):
        label_start = f"loop_{self.labels_count}_start"
        label_end = f"loop_{self.labels_count}_end"
        self.labels_count += 1

        self.asm_lines.extend([
            f"{label_start}:",
            f"    cmp byte [r15], 0",
            f"    je {label_end}",
            ""
        ])

        self._generate_block(loop_node.body)

        self.asm_lines.extend([
            f"    jmp {label_start}",
            f"{label_end}:",
            ""
        ])

    def _generate_footer(self):
        self.asm_lines.extend([
            "    mov rax, 60      ; sys_exit",
            "    mov rdi, 0       ; код возврата 0",
            "    syscall"
        ])

    def print_assembly(self):
        print("\n" + "=" * 60)
        print("АССЕМБЛЕРНЫЙ КОД:")
        print("=" * 60)
        for line in self.asm_lines:
            print(line)