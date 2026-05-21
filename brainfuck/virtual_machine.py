from typing import List, Tuple

from brainfuck.vm_compiler import OpCode


class VirtualMachine:
    def __init__(self, memory_size: int = 30000):
        self.memory = [0] * memory_size
        self.pointer = 0
        self.pc = 0
        self.running = True
        self.instructions_executed = 0
        self.max_instructions = 1_000_000
        self.bytecode: List[Tuple[int, int]] = []
        self.stats = {
            "inc": 0,
            "dec": 0,
            "add": 0,
            "sub": 0,
            "mov": 0,
            "jumps": 0,
            "outputs": 0,
            "inputs": 0,
        }

    def load_program(self, bytecode: List[Tuple[int, int]], verbose: bool = True) -> None:
        self.bytecode = bytecode
        self.pc = 0
        self.running = True
        self.instructions_executed = 0
        if verbose:
            print(f"\nLoaded {len(bytecode)} VM instructions")

    def run(self, debug: bool = False, verbose: bool = True) -> bool:
        if verbose:
            print("\nRunning virtual machine...")
            print("=" * 50)

        try:
            while self.running and self.pc < len(self.bytecode):
                self.instructions_executed += 1
                if self.instructions_executed > self.max_instructions:
                    print(f"\nInstruction limit exceeded ({self.max_instructions})")
                    return False

                op, arg = self.bytecode[self.pc]
                self._execute_instruction(op, arg, debug)
                self.pc += 1

            if verbose:
                print("\nVirtual machine finished")
                self._print_stats()
            return True
        except Exception as error:
            print(f"\nVM error: {error}")
            print(f"  PC: {self.pc}, Pointer: {self.pointer}")
            return False

    def _execute_instruction(self, op: int, arg: int, debug: bool = False) -> None:
        if op == OpCode.INC:
            self.memory[self.pointer] = (self.memory[self.pointer] + 1) & 0xFF
            self.stats["inc"] += 1
        elif op == OpCode.DEC:
            self.memory[self.pointer] = (self.memory[self.pointer] - 1) & 0xFF
            self.stats["dec"] += 1
        elif op == OpCode.ADD:
            self.memory[self.pointer] = (self.memory[self.pointer] + arg) & 0xFF
            self.stats["add"] += 1
        elif op == OpCode.SUB:
            self.memory[self.pointer] = (self.memory[self.pointer] - arg) & 0xFF
            self.stats["sub"] += 1
        elif op == OpCode.RIGHT:
            self.pointer += 1
            self._check_bounds()
            self.stats["mov"] += 1
        elif op == OpCode.LEFT:
            self.pointer -= 1
            self._check_bounds()
            self.stats["mov"] += 1
        elif op == OpCode.MOV:
            self.pointer += arg
            self._check_bounds()
            self.stats["mov"] += abs(arg)
        elif op == OpCode.OUT:
            print(chr(self.memory[self.pointer]), end="", flush=True)
            self.stats["outputs"] += 1
        elif op == OpCode.IN:
            try:
                user_input = input()
            except EOFError:
                user_input = ""
            self.memory[self.pointer] = ord(user_input[0]) & 0xFF if user_input else 0
            self.stats["inputs"] += 1
        elif op == OpCode.JZ:
            if self.memory[self.pointer] == 0:
                self.pc = arg
                self.stats["jumps"] += 1
        elif op == OpCode.JNZ:
            if self.memory[self.pointer] != 0:
                self.pc = arg
                self.stats["jumps"] += 1
        elif op == OpCode.CLEAR:
            self.memory[self.pointer] = 0
        elif op == OpCode.SET:
            self.memory[self.pointer] = arg & 0xFF
        elif op == OpCode.HALT:
            self.running = False
        else:
            raise RuntimeError(f"Unknown instruction: {op}")

        if debug and self.instructions_executed % 1000 == 0:
            self._debug_print()

    def _check_bounds(self) -> None:
        if self.pointer < 0 or self.pointer >= len(self.memory):
            raise RuntimeError(f"Memory pointer out of bounds: {self.pointer}")

    def _debug_print(self) -> None:
        print(
            f"\n[DEBUG] PC: {self.pc}, PTR: {self.pointer}, "
            f"CELL: {self.memory[self.pointer]}, INS: {self.instructions_executed}"
        )

    def _print_stats(self) -> None:
        print("\nExecution stats:")
        print("_" * 50)
        print(f"  Instructions executed: {self.instructions_executed}")
        print(f"  Increments: {self.stats['inc']}")
        print(f"  Decrements: {self.stats['dec']}")
        print(f"  Adds: {self.stats['add']}")
        print(f"  Subs: {self.stats['sub']}")
        print(f"  Pointer moves: {self.stats['mov']}")
        print(f"  Conditional jumps: {self.stats['jumps']}")
        print(f"  Outputs: {self.stats['outputs']}")
        print(f"  Inputs: {self.stats['inputs']}")


__all__ = ["VirtualMachine"]
