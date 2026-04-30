import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from brainfuck_ast import build_ast
from semantic_analyzer import SemanticAnalyzer
from gen.brainfuckParser import brainfuckParser
from antlr4 import InputStream, CommonTokenStream
from gen.brainfuckLexer import brainfuckLexer


def test_semantic_analysis(source_code: str, test_name: str):
    
    print(f"\n{'='*60}")
    print(f"ТЕСТ: {test_name}")
    print(f"{'='*60}")
    print(f"Код: {source_code}")
    print("-" * 60)
    
    #лексический анализ
    input_stream = InputStream(source_code)
    lexer = brainfuckLexer(input_stream)
    stream = CommonTokenStream(lexer)
    stream.fill()
    
    parser = brainfuckParser(stream)
    tree = parser.prog()
    
    # AST
    ast = build_ast(tree)
    
    #семантический анализ
    analyzer = SemanticAnalyzer()
    is_valid = analyzer.analyze(ast)
    
    # нет ошибок, выполнение программы
    if is_valid:
        print("\nЗапуск интерпретатора")
        from brainfuck import brainfuck
        bf = brainfuck()
        bf.execute_ast(ast)
    
    return is_valid

if __name__ == "__main__":
    
    # Корректная программа
    test_semantic_analysis(
        "++++++++[>++++[>++>+++>+++>+<<<<-]>+>+>->>+[<]<-]>>.",
        "Hello World (упрощённый)"
    )
    
    #Пустой цикл
    test_semantic_analysis(
        "+++[]---",
        "Пустой цикл []"
    )
    
    #Потенциально бесконечный цикл
    test_semantic_analysis(
        "+[>]<",
        "Цикл без изменения текущей ячейки"
    )
    
    # Простая программа
    test_semantic_analysis(
        "++++++++++[>+++++++>++++++++++>+++>+<<<<-]>++.>+.+++++++..+++.>++.<<+++++++++++++++.>.+++.------.--------.>+.>.",
        "Hello World"
    )
    
    # Вложенные пустые циклы
    test_semantic_analysis(
        "+[[]]",
        "Вложенный пустой цикл"
    )