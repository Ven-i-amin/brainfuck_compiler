from __future__ import annotations

from dataclasses import dataclass

from gen.brainfuckParser import brainfuckParser

try:
    from gen.brainfuckParser import brainfuckParser
    ANTLR_ProgContext = brainfuckParser.ProgContext
    ANTLR_ExprContext = brainfuckParser.ExprContext
except ImportError:
    ANTLR_ProgContext = None
    ANTLR_ExprContext = None

try:
    from gen.new_brainfuckParser import ProgContext as Custom_ProgContext
    from gen.new_brainfuckParser import ExprContext as Custom_ExprContext
except ImportError:
    Custom_ProgContext = None
    Custom_ExprContext = None



@dataclass
class CommandNode:
    command: str


@dataclass
class LoopNode:
    body: list["AstNode"]


@dataclass
class ProgramNode:
    body: list["AstNode"]


AstNode = CommandNode | LoopNode


def _is_prog_context(ctx) -> bool:
    if ANTLR_ProgContext and isinstance(ctx, ANTLR_ProgContext):
        return True
    if Custom_ProgContext and isinstance(ctx, Custom_ProgContext):
        return True
    return type(ctx).__name__ == 'ProgContext'


def _is_expr_context(ctx) -> bool:
    if ANTLR_ExprContext and isinstance(ctx, ANTLR_ExprContext):
        return True
    if Custom_ExprContext and isinstance(ctx, Custom_ExprContext):
        return True
    return type(ctx).__name__ == 'ExprContext'


def build_ast(ctx) -> Union[ProgramNode, AstNode]:
    
    if _is_prog_context(ctx):
        exprs = ctx.expr()
        if exprs is None:
            exprs = []
        return ProgramNode([build_ast(expr_ctx) for expr_ctx in exprs])

    command = ctx.COMMAND()
    if command is not None:
        return CommandNode(command.getText())

    exprs = ctx.expr()
    if exprs is None:
        exprs = []
    return LoopNode([build_ast(expr_ctx) for expr_ctx in exprs])




def format_ast(node: ProgramNode | AstNode) -> str:
    lines = [_node_label(node)]
    children = _node_children(node)

    for index, child in enumerate(children):
        is_last = index == len(children) - 1
        lines.extend(_format_child(child, "", is_last))

    return "\n".join(lines)


def print_ast(node: ProgramNode | AstNode) -> None:
    print(format_ast(node))


def _format_child(node: AstNode, prefix: str, is_last: bool) -> list[str]:
    branch = "\\-- " if is_last else "+-- "
    lines = [prefix + branch + _node_label(node)]
    next_prefix = prefix + ("    " if is_last else "|   ")
    children = _node_children(node)

    for index, child in enumerate(children):
        child_is_last = index == len(children) - 1
        lines.extend(_format_child(child, next_prefix, child_is_last))

    return lines


def _node_label(node: ProgramNode | AstNode) -> str:
    if isinstance(node, ProgramNode):
        return "Program"
    if isinstance(node, LoopNode):
        return "Loop [ ]"
    return f"Command {node.command}"


def _node_children(node: ProgramNode | AstNode) -> list[AstNode]:
    if isinstance(node, ProgramNode):
        return node.body
    if isinstance(node, LoopNode):
        return node.body
    return []
