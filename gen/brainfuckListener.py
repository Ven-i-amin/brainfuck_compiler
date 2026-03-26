# Generated from brainfuck.g4 by ANTLR 4.13.1
from antlr4 import *

from brainfuck import brainfuck as BrainfuckMachine
from brainfuck_ast import ProgramNode, build_ast
if "." in __name__:
    from gen.brainfuckParser import brainfuckParser
else:
    from brainfuckParser import brainfuckParser

# This class defines a complete listener for a parse tree produced by brainfuckParser.
class brainfuckListener:
    """Listener совместимый с новым парсером"""
    
    def __init__(self):
        self.machine = BrainfuckMachine()
        self.ast = None
    
    def _execute_expr(self, ctx):
        """Выполняет выражение"""
        command = ctx.COMMAND()
        if command is not None:
            self._execute_command(command.getText())
            return
        
        # Это цикл
        while self.machine.cycle_working():
            for nested_expr in ctx.expr():
                self._execute_expr(nested_expr)
    
    def _execute_command(self, command: str):
        if command in [">", "<"]:
            self.machine.move_pointer(command)
        elif command in ["+", "-"]:
            self.machine.change_value(command)
        elif command == ".":
            self.machine.output()
        elif command == ",":
            self.machine.input()
        else:
            raise ValueError(f"Unsupported command: {command}")
    
    def enterProg(self, ctx):
        """Вход в программу"""
        from brainfuck_ast import build_ast
        self.ast = build_ast(ctx)
        
        for expr_ctx in ctx.expr():
            self._execute_expr(expr_ctx)
    
    def exitProg(self, ctx):
        pass
    
    def enterExpr(self, ctx):
        pass
    
    def exitExpr(self, ctx):
        pass


del brainfuckParser
