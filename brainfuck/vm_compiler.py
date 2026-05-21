from typing import List, Tuple

from middleend.brainfuck_ast import CommandNode, LoopNode, ProgramNode


class OpCode:
    NOP = 0x00
    INC = 0x01
    DEC = 0x02
    ADD = 0x03
    SUB = 0x04
    RIGHT = 0x05
    LEFT = 0x06
    MOV = 0x07
    OUT = 0x08
    IN = 0x09
    JZ = 0x0A
    JNZ = 0x0B
    CLEAR = 0x0C
    SET = 0x0D
    HALT = 0xFF


class VMCompiler:
    def __init__(self):
        self.bytecode: List[Tuple[int, int]] = []

    def compile(self, ast: ProgramNode, verbose: bool = True) -> List[Tuple[int, int]]:
        self.bytecode = []

        if verbose:
            print("\nGenerating virtual machine bytecode...")

        self._compile_block(ast.body)
        self.bytecode.append((OpCode.HALT, 0))

        if verbose:
            print(f"  Instructions generated: {len(self.bytecode)}")

        return self.bytecode

    def _compile_block(self, block: List) -> None:
        for node in block:
            if isinstance(node, CommandNode):
                self._compile_command(node)
            elif isinstance(node, LoopNode):
                self._compile_loop(node)

    def _compile_command(self, cmd_node: CommandNode) -> None:
        cmd = cmd_node.command

        if cmd == "+":
            self.bytecode.append((OpCode.INC, 0))
        elif cmd == "-":
            self.bytecode.append((OpCode.DEC, 0))
        elif cmd == ">":
            self.bytecode.append((OpCode.RIGHT, 0))
        elif cmd == "<":
            self.bytecode.append((OpCode.LEFT, 0))
        elif cmd.startswith("optimized:add:"):
            value = int(cmd.split(":")[2])
            self.bytecode.append((OpCode.INC, 0) if value == 1 else (OpCode.ADD, value))
        elif cmd.startswith("optimized:sub:"):
            value = int(cmd.split(":")[2])
            self.bytecode.append((OpCode.DEC, 0) if value == 1 else (OpCode.SUB, value))
        elif cmd.startswith("optimized:right:"):
            value = int(cmd.split(":")[2])
            self.bytecode.append((OpCode.RIGHT, 0) if value == 1 else (OpCode.MOV, value))
        elif cmd.startswith("optimized:left:"):
            value = int(cmd.split(":")[2])
            self.bytecode.append((OpCode.LEFT, 0) if value == 1 else (OpCode.MOV, -value))
        elif cmd == "optimized:clear":
            self.bytecode.append((OpCode.CLEAR, 0))
        elif cmd == ".":
            self.bytecode.append((OpCode.OUT, 0))
        elif cmd == ",":
            self.bytecode.append((OpCode.IN, 0))

    def _compile_loop(self, loop_node: LoopNode) -> None:
        check_pos = len(self.bytecode)
        self.bytecode.append((OpCode.JZ, 0))
        self._compile_block(loop_node.body)
        self.bytecode.append((OpCode.JNZ, check_pos))
        after_loop = len(self.bytecode)
        self.bytecode[check_pos] = (OpCode.JZ, after_loop)

    def print_bytecode(self) -> None:
        print("\nVirtual machine bytecode:")
        print("=" * 60)
        print(f"{'Addr':<6} {'Instr':<12} {'Arg':<10} {'Description'}")
        print("-" * 60)

        op_names = {
            OpCode.NOP: "NOP",
            OpCode.INC: "INC",
            OpCode.DEC: "DEC",
            OpCode.ADD: "ADD",
            OpCode.SUB: "SUB",
            OpCode.RIGHT: "RIGHT",
            OpCode.LEFT: "LEFT",
            OpCode.MOV: "MOV",
            OpCode.OUT: "OUT",
            OpCode.IN: "IN",
            OpCode.JZ: "JZ",
            OpCode.JNZ: "JNZ",
            OpCode.CLEAR: "CLEAR",
            OpCode.SET: "SET",
            OpCode.HALT: "HALT",
        }

        descriptions = {
            OpCode.INC: "Increment cell by 1",
            OpCode.DEC: "Decrement cell by 1",
            OpCode.ADD: "Add value",
            OpCode.SUB: "Subtract value",
            OpCode.RIGHT: "Move right",
            OpCode.LEFT: "Move left",
            OpCode.MOV: "Move by N",
            OpCode.OUT: "Output byte",
            OpCode.IN: "Input byte",
            OpCode.JZ: "Jump if zero",
            OpCode.JNZ: "Jump if not zero",
            OpCode.CLEAR: "Clear cell",
            OpCode.SET: "Set value",
            OpCode.HALT: "Stop",
        }

        for index, (op, arg) in enumerate(self.bytecode):
            name = op_names.get(op, "UNKNOWN")
            description = descriptions.get(op, "")
            display_arg = arg if arg != 0 else "-"
            print(f"{index:<6} {name:<12} {display_arg!s:<10} {description}")

        print("=" * 60)


__all__ = ["OpCode", "VMCompiler"]
