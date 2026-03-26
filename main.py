from antlr4 import InputStream, CommonTokenStream  # ← Добавили InputStream
from gen.brainfuckLexer import brainfuckLexer
from gen.brainfuckParser import brainfuckParser
from gen.brainfuckListener import brainfuckListener
from brainfuck_ast import build_ast, print_ast
from errors.brainfuck_errors import SyntaxChecker
from errors.error_listener import CustomErrorListener
from gen.new_brainfuckParser import BrainfuckParser as CustomBrainfuckParser

USE_ANTLR = False

if __name__ == "__main__":
    try:
        input_file = "input.bf"
        
        with open(input_file, "r", encoding="utf-8") as f:
            source_code = f.read()
        
        # Проверка синтаксиса
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
        
        if USE_ANTLR:
            input_stream = InputStream(source_code)
            lexer = brainfuckLexer(input_stream)
            stream = CommonTokenStream(lexer)
            parser = brainfuckParser(stream)
            
            error_listener = CustomErrorListener()
            parser.removeErrorListeners()
            parser.addErrorListener(error_listener)
            tree = parser.prog()
            
            if error_listener.errors:
                print(f"\n Ошибки парсинга (ANTLR): {len(error_listener.errors)}")
                for err in error_listener.errors:
                    print(f"  {err}")
                exit(1)
        else:
            parser = CustomBrainfuckParser(stream)
            tree = parser.prog()
            
            if parser.errors:
                print(f"\n Ошибки парсинга (Custom): {len(parser.errors)}")
                for error in parser.errors:
                    print(f"  {error}")
                exit(1)
        
        print(" Парсинг успешен")
        
        ast_tree = build_ast(tree)
        print_ast(ast_tree)
        
        print("_" * 50)
        print("Результат выполнения:")
        
        # Выполнение через listener
        from gen.brainfuckListener import brainfuckListener
        listener = brainfuckListener()
        listener.enterProg(tree)
        
    except FileNotFoundError:
        print(f" Ошибка: Файл {input_file} не найден")
        exit(1)
    except SyntaxError as e:
        print(f" Ошибка синтаксиса: {e}")
        exit(1)
    except Exception as e:
        print(f" Критическая ошибка: {e}")
        import traceback
        traceback.print_exc()
        exit(1)