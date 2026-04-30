from typing import List, Tuple
from compiler.vm_compiler import OpCode


class VirtualMachine:
    """Виртуальная машина для исполнения байт-кода"""

    def __init__(self, memory_size: int = 30000):
        self.memory = [0] * memory_size
        self.pointer = 0
        self.pc = 0
        self.running = True
        self.instructions_executed = 0
        self.max_instructions = 1_000_000

        # Статистика
        self.stats = {
            'inc': 0, 'dec': 0, 'add': 0, 'sub': 0,
            'mov': 0, 'jumps': 0, 'outputs': 0, 'inputs': 0
        }

    def load_program(self, bytecode: List[Tuple[int, int]]):
        """Загрузка программы в VM"""
        self.bytecode = bytecode
        self.pc = 0
        self.running = True
        self.instructions_executed = 0
        print(f"\nЗагружено {len(bytecode)} инструкций в виртуальную машину")

    def run(self, debug: bool = False) -> bool:
        """Запуск VM"""
        print("\nЗапуск виртуальной машины...")
        print("=" * 50)

        try:
            while self.running and self.pc < len(self.bytecode):
                # Защита от бесконечных циклов
                self.instructions_executed += 1
                if self.instructions_executed > self.max_instructions:
                    print(f"\nПревышен лимит инструкций ({self.max_instructions})")
                    return False

                # Выполнение инструкции
                op, arg = self.bytecode[self.pc]
                self._execute_instruction(op, arg, debug)

                # Переход к следующей инструкции
                self.pc += 1

            print("\nВиртуальная машина завершила работу")
            self._print_stats()
            return True

        except Exception as e:
            print(f"\nОшибка VM: {e}")
            print(f"   PC: {self.pc}, Указатель: {self.pointer}")
            return False

    def _execute_instruction(self, op: int, arg: int, debug: bool = False):
        """Выполнение одной инструкции"""

        if op == OpCode.INC:
            self.memory[self.pointer] = (self.memory[self.pointer] + 1) & 0xFF
            self.stats['inc'] += 1

        elif op == OpCode.DEC:
            self.memory[self.pointer] = (self.memory[self.pointer] - 1) & 0xFF
            self.stats['dec'] += 1

        elif op == OpCode.ADD:
            self.memory[self.pointer] = (self.memory[self.pointer] + arg) & 0xFF
            self.stats['add'] += 1

        elif op == OpCode.SUB:
            self.memory[self.pointer] = (self.memory[self.pointer] - arg) & 0xFF
            self.stats['sub'] += 1

        elif op == OpCode.RIGHT:
            self.pointer += 1
            if self.pointer >= len(self.memory):
                raise RuntimeError(f"Выход за границы памяти (адрес {self.pointer})")

        elif op == OpCode.LEFT:
            self.pointer -= 1
            if self.pointer < 0:
                raise RuntimeError(f"Выход за границы памяти (адрес {self.pointer})")

        elif op == OpCode.MOV:
            self.pointer += arg
            if self.pointer < 0 or self.pointer >= len(self.memory):
                raise RuntimeError(f"Выход за границы памяти (адрес {self.pointer})")
            self.stats['mov'] += abs(arg)

        elif op == OpCode.OUT:
            char = chr(self.memory[self.pointer])
            print(char, end='', flush=True)
            self.stats['outputs'] += 1

        elif op == OpCode.IN:
            try:
                user_input = input()
                if user_input:
                    self.memory[self.pointer] = ord(user_input[0]) & 0xFF
                else:
                    self.memory[self.pointer] = 0
                self.stats['inputs'] += 1
            except EOFError:
                self.memory[self.pointer] = 0

        elif op == OpCode.JZ:
            if self.memory[self.pointer] == 0:
                self.pc = arg
                self.stats['jumps'] += 1

        elif op == OpCode.JNZ:
            if self.memory[self.pointer] != 0:
                self.pc = arg
                self.stats['jumps'] += 1

        elif op == OpCode.CLEAR:
            self.memory[self.pointer] = 0

        elif op == OpCode.SET:
            self.memory[self.pointer] = arg & 0xFF

        elif op == OpCode.HALT:
            self.running = False

        else:
            raise RuntimeError(f"Неизвестная инструкция: {op}")

        # Отладка
        if debug and self.instructions_executed % 1000 == 0:
            self._debug_print()

    def _debug_print(self):
        """Отладочная печать состояния"""
        print(f"\n[DEBUG] PC: {self.pc}, PTR: {self.pointer}, "
              f"CELL: {self.memory[self.pointer]}, "
              f"INS: {self.instructions_executed}")

        start = max(0, self.pointer - 3)
        end = min(len(self.memory), self.pointer + 4)
        cells = [self.memory[i] for i in range(start, end)]
        ptr_rel = self.pointer - start

        visual = "[" + "][".join(f"{c:3}" for c in cells) + "]"
        pointer_line = " " * (ptr_rel * 5 + 2) + "▲"
        print(f"  Память: {visual}")
        print(f"           {pointer_line}")

    def _print_stats(self):
        """Вывод статистики выполнения"""
        print(f"\nСтатистика выполнения:")
        print("_" * 50)
        print(f"  Инструкций выполнено: {self.instructions_executed}")
        print(f"  Инкрементов: {self.stats['inc']}")
        print(f"  Декрементов: {self.stats['dec']}")
        print(f"  Сложений: {self.stats['add']}")
        print(f"  Вычитаний: {self.stats['sub']}")
        print(f"  Перемещений указателя: {self.stats['mov']}")
        print(f"  Условных прыжков: {self.stats['jumps']}")
        print(f"  Выводов символов: {self.stats['outputs']}")
        print(f"  Вводов символов: {self.stats['inputs']}")

        used_cells = sum(1 for v in self.memory if v != 0)
        print(f"  Использовано ячеек памяти: {used_cells}/{len(self.memory)}")
        print(f"  Текущая позиция указателя: {self.pointer}")