from typing import List, Tuple
from brainfuck_ast import ProgramNode, LoopNode, CommandNode


class OpCode:
    """Коды операций виртуальной машины"""
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
    """Компилятор AST в байт-код виртуальной машины"""

    def __init__(self):
        self.bytecode: List[Tuple[int, int]] = []

    def compile(self, ast: ProgramNode) -> List[Tuple[int, int]]:
        """Компиляция AST в байт-код"""
        self.bytecode = []

        print("\nГенерация байт-кода для виртуальной машины...")

        self._compile_block(ast.body)
        self.bytecode.append((OpCode.HALT, 0))

        print(f"  Сгенерировано инструкций: {len(self.bytecode)}")

        return self.bytecode

    def _compile_block(self, block: List):
        """Компиляция блока инструкций"""
        for node in block:
            if isinstance(node, CommandNode):
                self._compile_command(node)
            elif isinstance(node, LoopNode):
                self._compile_loop(node)

    def _compile_command(self, cmd_node: CommandNode):
        """Компиляция отдельной команды"""
        cmd = cmd_node.command

        if cmd == '+':
            self.bytecode.append((OpCode.INC, 0))
        elif cmd == '-':
            self.bytecode.append((OpCode.DEC, 0))
        elif cmd == '>':
            self.bytecode.append((OpCode.RIGHT, 0))
        elif cmd == '<':
            self.bytecode.append((OpCode.LEFT, 0))
        elif cmd.startswith('optimized:add:'):
            value = int(cmd.split(':')[2])
            if value == 1:
                self.bytecode.append((OpCode.INC, 0))
            else:
                self.bytecode.append((OpCode.ADD, value))
        elif cmd.startswith('optimized:sub:'):
            value = int(cmd.split(':')[2])
            if value == 1:
                self.bytecode.append((OpCode.DEC, 0))
            else:
                self.bytecode.append((OpCode.SUB, value))
        elif cmd.startswith('optimized:right:'):
            value = int(cmd.split(':')[2])
            if value == 1:
                self.bytecode.append((OpCode.RIGHT, 0))
            else:
                self.bytecode.append((OpCode.MOV, value))
        elif cmd.startswith('optimized:left:'):
            value = int(cmd.split(':')[2])
            if value == 1:
                self.bytecode.append((OpCode.LEFT, 0))
            else:
                self.bytecode.append((OpCode.MOV, -value))
        elif cmd == 'optimized:clear':
            self.bytecode.append((OpCode.CLEAR, 0))
        elif cmd == '.':
            self.bytecode.append((OpCode.OUT, 0))
        elif cmd == ',':
            self.bytecode.append((OpCode.IN, 0))

    def _compile_loop(self, loop_node: LoopNode):
        """Компиляция цикла Brainfuck"""
        # Проверка условия входа в цикл
        check_pos = len(self.bytecode)
        self.bytecode.append((OpCode.JZ, 0))

        # Начало тела цикла
        loop_start = len(self.bytecode)

        # Тело цикла
        self._compile_block(loop_node.body)

        # Возврат к проверке условия
        self.bytecode.append((OpCode.JNZ, check_pos))

        # Заполняем адрес для JZ (выход из цикла)
        after_loop = len(self.bytecode)
        self.bytecode[check_pos] = (OpCode.JZ, after_loop)

    def print_bytecode(self):
        """Вывод байт-кода для отладки"""
        print("\nБайт-код виртуальной машины:")
        print("=" * 60)
        print(f"{'Адрес':<6} {'Инструкция':<12} {'Аргумент':<10} {'Описание'}")
        print("-" * 60)

        op_names = {
            OpCode.NOP: 'NOP', OpCode.INC: 'INC', OpCode.DEC: 'DEC',
            OpCode.ADD: 'ADD', OpCode.SUB: 'SUB', OpCode.RIGHT: 'RIGHT',
            OpCode.LEFT: 'LEFT', OpCode.MOV: 'MOV', OpCode.OUT: 'OUT',
            OpCode.IN: 'IN', OpCode.JZ: 'JZ', OpCode.JNZ: 'JNZ',
            OpCode.CLEAR: 'CLEAR', OpCode.SET: 'SET', OpCode.HALT: 'HALT'
        }

        descriptions = {
            OpCode.INC: 'Увеличить ячейку на 1',
            OpCode.DEC: 'Уменьшить ячейку на 1',
            OpCode.ADD: 'Добавить значение',
            OpCode.SUB: 'Вычесть значение',
            OpCode.RIGHT: 'Сдвиг вправо',
            OpCode.LEFT: 'Сдвиг влево',
            OpCode.MOV: 'Сдвиг на N',
            OpCode.OUT: 'Вывод символа',
            OpCode.IN: 'Ввод символа',
            OpCode.JZ: 'Прыжок если 0',
            OpCode.JNZ: 'Прыжок если не 0',
            OpCode.CLEAR: 'Очистка ячейки',
            OpCode.SET: 'Установка значения',
            OpCode.HALT: 'Остановка'
        }

        for i, (op, arg) in enumerate(self.bytecode):
            name = op_names.get(op, 'UNKNOWN')
            desc = descriptions.get(op, '')
            if arg != 0:
                print(f"{i:<6} {name:<12} {arg:<10} {desc}")
            else:
                print(f"{i:<6} {name:<12} {'-':<10} {desc}")

        print("=" * 60)