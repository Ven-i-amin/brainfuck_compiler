# main.py
from antlr4 import InputStream, CommonTokenStream
from gen.brainfuckLexer import brainfuckLexer
from gen.brainfuckParser import brainfuckParser
from brainfuck_ast import build_ast, print_ast
from errors.brainfuck_errors import SyntaxChecker
from errors.error_listener import CustomErrorListener
from compiler.semantic_analyzer import SemanticAnalyzer
from compiler.ast_optimizer import ASTOptimizer
from compiler.x86_compiler import X86Compiler


def main():
    print("\n" + "=" * 60)
    print("BRAINFUCK КОМПИЛЯТОР В X86")
    print("=" * 60)

    try:
        input_file = "input.bf"
        
        with open(input_file, "r", encoding="utf-8") as f:
            source_code = f.read()

        print(f"\nИсходная программа ({input_file}):")
        print("-" * 50)
        print(source_code)
        print("-" * 50)

        # ЭТАП 1: СИНТАКСИЧЕСКИЙ АНАЛИЗ
        print("\nЭТАП 1: СИНТАКСИЧЕСКИЙ АНАЛИЗ")
        print("-" * 50)

        syntax_checker = SyntaxChecker()
        if not syntax_checker.check_all(source_code):
            syntax_checker.print_errors()
            print("\nВыполнение прервано из-за синтаксических ошибок")
            exit(1)
        else:
            syntax_checker.print_errors()

        input_stream = InputStream(source_code)
        lexer = brainfuckLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = brainfuckParser(stream)

        error_listener = CustomErrorListener()
        parser.removeErrorListeners()
        parser.addErrorListener(error_listener)
        tree = parser.prog()

        if error_listener.errors:
            print(f"\nОшибки парсинга: {len(error_listener.errors)}")
            exit(1)
        print("Парсинг успешен")

        # ЭТАП 2: ПОСТРОЕНИЕ AST
        print("\nЭТАП 2: ПОСТРОЕНИЕ AST")
        print("-" * 50)
        ast = build_ast(tree)
        print_ast(ast)

        # ЭТАП 3: СЕМАНТИЧЕСКИЙ АНАЛИЗ
        print("\nЭТАП 3: СЕМАНТИЧЕСКИЙ АНАЛИЗ")
        print("-" * 50)
        semantic_analyzer = SemanticAnalyzer()
        if not semantic_analyzer.analyze(ast):
            print("Семантический анализ обнаружил критические ошибки")
            exit(1)

        # ЭТАП 4: ТИПОЗАВИСИМЫЙ АНАЛИЗ И ОПТИМИЗАЦИЯ AST
        print("\nЭТАП 4: ТИПОЗАВИСИМЫЙ АНАЛИЗ И ОПТИМИЗАЦИЯ AST")
        print("-" * 50)
        optimizer = ASTOptimizer()
        optimizer.optimization_level = 1
        optimized_ast = optimizer.optimize(ast)

        print("\nОптимизированное AST:")
        print_ast(optimized_ast)

        # ЭТАП 5: ГЕНЕРАЦИЯ X86 АССЕМБЛЕРА
        print("\nЭТАП 5: ГЕНЕРАЦИЯ X86 АССЕМБЛЕРА")
        print("-" * 50)

        x86_compiler = X86Compiler()
        asm_file = x86_compiler.compile(optimized_ast, "brainfuck.asm")
        #x86_compiler.print_assembly()

        print("\n" + "_" * 60)
        print("КОМПИЛЯЦИЯ ЗАВЕРШЕНА")

    except FileNotFoundError:
        print(f"Ошибка: Файл '{input_file}' не найден")
        exit(1)
    except Exception as e:
        print(f"Критическая ошибка: {e}")
        import traceback
        traceback.print_exc()
        exit(1)


if __name__ == "__main__":
    main()