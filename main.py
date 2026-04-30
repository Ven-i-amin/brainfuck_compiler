import argparse
import os
import traceback

from antlr4 import CommonTokenStream, InputStream

from brainfuck.brainfuck import BrainfuckInterpreter
from brainfuck.compiler.x86_compiler import X86Compiler
from errors.brainfuck_errors import SyntaxChecker
from errors.error_listener import CustomErrorListener
from gen.brainfuckLexer import brainfuckLexer
from gen.brainfuckParser import brainfuckParser
from middleend.ast_optimizer import ASTOptimizer
from middleend.brainfuck_ast import build_ast, format_ast
from middleend.semantic_analyzer import SemanticAnalyzer


def parse_source(input_file: str, show_source: bool = False):
    with open(input_file, "r", encoding="utf-8") as source:
        source_code = source.read()

    if show_source:
        print(f"\nSource program ({input_file}):")
        print("-" * 50)
        print(source_code)
        print("-" * 50)

    syntax_checker = SyntaxChecker()
    if not syntax_checker.check_all(source_code):
        syntax_checker.print_errors(verbose=True)
        raise ValueError("Compilation aborted due to syntax errors")
    syntax_checker.print_errors(verbose=False)

    input_stream = InputStream(source_code)
    lexer = brainfuckLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = brainfuckParser(stream)

    error_listener = CustomErrorListener()
    parser.removeErrorListeners()
    parser.addErrorListener(error_listener)
    tree = parser.prog()

    if error_listener.errors:
        raise ValueError(f"Parsing errors: {len(error_listener.errors)}")

    return build_ast(tree)


def validate_ast(ast):
    semantic_analyzer = SemanticAnalyzer()
    if not semantic_analyzer.analyze(ast, verbose=False):
        raise ValueError("Semantic analysis found critical errors")


def optimize_ast(ast, show_optimization: bool = False):
    optimizer = ASTOptimizer()
    optimizer.optimization_level = 1
    optimized_ast = optimizer.optimize(ast, verbose=show_optimization)

    if show_optimization:
        print("\nOptimized AST:")
        print("-" * 50)
        print(format_ast(optimized_ast))

    return optimized_ast


def prepare_ast(
    input_file: str,
    show_source: bool = False,
    show_ast: bool = False,
    show_optimization: bool = False,
):
    ast = parse_source(input_file, show_source=show_source)

    if show_ast:
        print("\nAST:")
        print("-" * 50)
        print(format_ast(ast))

    validate_ast(ast)
    return optimize_ast(ast, show_optimization=show_optimization)


def compile_to_asm(
    input_file: str,
    output_file: str,
    show_source: bool = False,
    show_ast: bool = False,
    show_optimization: bool = False,
) -> str:
    ast = prepare_ast(
        input_file,
        show_source=show_source,
        show_ast=show_ast,
        show_optimization=show_optimization,
    )
    compiler = X86Compiler()
    return compiler.execute(ast, output_file=output_file, verbose=show_optimization)


def run_on_python(
    input_file: str,
    show_source: bool = False,
    show_ast: bool = False,
    show_optimization: bool = False,
):
    ast = prepare_ast(
        input_file,
        show_source=show_source,
        show_ast=show_ast,
        show_optimization=show_optimization,
    )
    interpreter = BrainfuckInterpreter()
    return interpreter.execute(ast, verbose=False)


def add_output_flags(command_parser: argparse.ArgumentParser):
    command_parser.add_argument(
        "-a",
        "--all",
        action="store_true",
        help="Show all available details",
    )
    command_parser.add_argument(
        "-s",
        "--source",
        action="store_true",
        help="Show the source Brainfuck file",
    )
    command_parser.add_argument(
        "-t",
        "--ast",
        action="store_true",
        help="Show the AST",
    )
    command_parser.add_argument(
        "-p",
        "--optimization",
        action="store_true",
        help="Show AST optimization details",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Brainfuck compiler and interpreter")
    subparsers = parser.add_subparsers(dest="command")

    compile_parser = subparsers.add_parser(
        "compile-asm",
        help="Compile a Brainfuck source file into an x86 assembly file",
    )
    compile_parser.add_argument("input_file", help="Path to the Brainfuck source file")
    compile_parser.add_argument(
        "-o",
        "--output",
        dest="output_file",
        help="Path to the output assembly file",
    )
    add_output_flags(compile_parser)

    run_parser = subparsers.add_parser(
        "run",
        help="Interpret a Brainfuck source file on Python",
    )
    run_parser.add_argument("input_file", help="Path to the Brainfuck source file")
    add_output_flags(run_parser)

    return parser


def resolve_output_flags(args):
    return (
        args.all or args.source,
        args.all or args.ast,
        args.all or args.optimization,
    )


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    try:
        if args.command == "compile-asm":
            input_file = args.input_file
            output_file = args.output_file or os.path.splitext(input_file)[0] + ".asm"
            show_source, show_ast, show_optimization = resolve_output_flags(args)
            compile_to_asm(
                input_file,
                output_file,
                show_source=show_source,
                show_ast=show_ast,
                show_optimization=show_optimization,
            )
        elif args.command == "run":
            input_file = args.input_file
            show_source, show_ast, show_optimization = resolve_output_flags(args)
            run_on_python(
                input_file,
                show_source=show_source,
                show_ast=show_ast,
                show_optimization=show_optimization,
            )
        else:
            parser.print_help()
            raise SystemExit(1)
    except FileNotFoundError:
        print(f"Error: file '{input_file}' not found")
        raise SystemExit(1)
    except Exception as error:
        print(f"Critical error: {error}")
        traceback.print_exc()
        raise SystemExit(1)


if __name__ == "__main__":
    main()
