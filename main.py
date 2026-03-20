from antlr4 import InputStream, CommonTokenStream  # ← Добавили InputStream
from gen.brainfuckLexer import brainfuckLexer
from gen.brainfuckParser import brainfuckParser
from gen.brainfuckListener import brainfuckListener
from brainfuck_ast import build_ast, print_ast
from errors.brainfuck_errors import SyntaxChecker
from errors.error_listener import CustomErrorListener

if (__name__ == "__main__"):
    try:

        input_file = "input.bf"

        with open(input_file, "r", encoding="utf-8") as f:
            source_code = f.read()

        syntax_checker = SyntaxChecker()
        if not syntax_checker.check_all(source_code):
            syntax_checker.print_errors()
            print("\n Выполнение прервано из-за синтаксических ошибок")
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
            print(f"\n Ошибки парсинга: {len(error_listener.errors)}")
            exit(1)
        print(" Парсинг успешен")

        ast_tree = build_ast(tree)
        print_ast(ast_tree)

        print("_" * 50)
        print("Результат выполнения:")
        listener = brainfuckListener()
        listener.enterProg(tree)

    except FileNotFoundError:
        print(" Ошибка: Файл "+ input_file +" не найден")
        exit(1)
    except SyntaxError as e:
        print(f" Ошибка синтаксиса: {e}")
        exit(1)
    except Exception as e:
        print(f" Критическая ошибка: {e}")
        exit(1)