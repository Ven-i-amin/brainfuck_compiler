from antlr4 import FileStream, CommonTokenStream
from brainfuckLexer import brainfuckLexer
from brainfuckParser import brainfuckParser
from brainfuckListener import brainfuckListener
from brainfuck_ast import build_ast, print_ast

if (__name__ == "__main__"):
    input_stream = FileStream("input.bf")
    lexer = brainfuckLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = brainfuckParser(stream)
    tree = parser.prog()

    listener = brainfuckListener()
    
    ast_tree = build_ast(tree)
    print_ast(ast_tree)
    
    print("")

    listener.enterProg(tree)
    