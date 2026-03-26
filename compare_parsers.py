from antlr4 import InputStream, CommonTokenStream
from gen.brainfuckLexer import brainfuckLexer
from gen.brainfuckParser import brainfuckParser as ANTLRBrainfuckParser
from gen.new_brainfuckParser import BrainfuckParser as CustomBrainfuckParser
from brainfuck_ast import build_ast, print_ast
from brainfuck_ast import ProgramNode, CommandNode, LoopNode

def compare_parsers_on_tokens(source_code: str):
    input_stream = InputStream(source_code)
    lexer = brainfuckLexer(input_stream)
    stream = CommonTokenStream(lexer)
    
    stream.fill()
    print(f"\nВсего токенов: {len(stream.tokens)}")
    
    # ANTLR парсер
    stream.seek(0)  
    antlr_parser = ANTLRBrainfuckParser(stream)
    antlr_tree = antlr_parser.prog()
    
    # Кастомный
    stream.seek(0) 
    custom_parser = CustomBrainfuckParser(stream)
    custom_tree = custom_parser.prog()
    
    #AST
    antlr_ast = build_ast(antlr_tree)
    custom_ast = build_ast(custom_tree)
    
    return antlr_ast, custom_ast

def compare_asts(ast1: ProgramNode, ast2: ProgramNode, verbose: bool = True):
    
    def ast_to_list(node):
        if isinstance(node, ProgramNode):
            result = ['Program']
            for child in node.body:
                result.append(ast_to_list(child))
            return result
        elif isinstance(node, LoopNode):
            result = ['Loop']
            for child in node.body:
                result.append(ast_to_list(child))
            return result
        elif isinstance(node, CommandNode):
            return ['Command', node.command]
        return ['Unknown']
    
    def find_differences(list1, list2, path=""):
        differences = []
        
        if type(list1) != type(list2):
            differences.append(f"{path}: Type mismatch - {type(list1)} vs {type(list2)}")
            return differences
        
        if isinstance(list1, list):
            if len(list1) != len(list2):
                differences.append(f"{path}: Length mismatch - {len(list1)} vs {len(list2)}")
            
            for i, (item1, item2) in enumerate(zip(list1, list2)):
                differences.extend(find_differences(item1, item2, f"{path}[{i}]"))
        else:
            if list1 != list2:
                differences.append(f"{path}: Value mismatch - '{list1}' vs '{list2}'")
        
        return differences
    
    list1 = ast_to_list(ast1)
    list2 = ast_to_list(ast2)
    
    if verbose:
        print("\nСравнение AST:")
        print("ANTLR AST:", list1)
        print("Custom AST:", list2)
    
    differences = find_differences(list1, list2)
    
    if differences:
        print("\n НАЙДЕНЫ РАЗЛИЧИЯ:")
        for diff in differences:
            print(f"  {diff}")
        return False
    else:
        print("\n AST полностью совпадают!")
        return True

def test_with_file(filename: str):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            source_code = f.read()
        
        print("=" * 60)
        print(f"Тестирование файла: {filename}")
        print(f"Размер кода: {len(source_code)} символов")
        print(f"Первые 100 символов: {source_code[:100]}")
        
        antlr_ast, custom_ast = compare_parsers_on_tokens(source_code)
        are_equal = compare_asts(antlr_ast, custom_ast)
        
        return are_equal
        
    except FileNotFoundError:
        print(f"Файл {filename} не найден")
        return False
    except Exception as e:
        print(f"Ошибка: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_with_file("input.bf")