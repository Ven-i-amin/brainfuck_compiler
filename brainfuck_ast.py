from __future__ import annotations

from dataclasses import dataclass

from brainfuckParser import brainfuckParser


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


def build_ast(ctx: brainfuckParser.ProgContext | brainfuckParser.ExprContext) -> ProgramNode | AstNode:
    if isinstance(ctx, brainfuckParser.ProgContext):
        return ProgramNode([build_ast(expr_ctx) for expr_ctx in ctx.expr()])

    command = ctx.COMMAND()
    if command is not None:
        return CommandNode(command.getText())

    return LoopNode([build_ast(expr_ctx) for expr_ctx in ctx.expr()])


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
