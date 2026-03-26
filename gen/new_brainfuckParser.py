from dataclasses import dataclass
from typing import List, Optional
from antlr4 import Token, CommonTokenStream
from gen.brainfuckLexer import brainfuckLexer

@dataclass
class CommandToken:
    """Имитация ANTLR токена"""
    text: str
    
    def getText(self):
        return self.text

class ProgContext:
    def __init__(self, exprs: List['ExprContext']):
        self._exprs = exprs
    
    def expr(self):
        return self._exprs
    
    def COMMAND(self):
        return None

class ExprContext:
    def __init__(self, command: Optional[str] = None, exprs: Optional[List['ExprContext']] = None):
        self._command = command
        self._exprs = exprs or []
    
    def expr(self):
        return self._exprs
    
    def COMMAND(self):
        if self._command:
            return CommandToken(self._command)
        return None

class TokenParser:
    
    def __init__(self, token_stream: CommonTokenStream):
        self.token_stream = token_stream
        self.tokens = []
        self.pos = 0
        
        token_stream.fill()
        for token in token_stream.tokens:
            if token.type != brainfuckLexer.WS and token.type != Token.EOF:
                self.tokens.append(token)
        
        self.length = len(self.tokens)
        self._errors = []
    
    def prog(self) -> ProgContext:
        try:
            # Проверяем баланс скобок на уровне токенов
            self._check_brackets()
            
            exprs = []
            while self.pos < self.length:
                expr = self._parse_expr()
                if expr:
                    exprs.append(expr)
            
            return ProgContext(exprs)
        except SyntaxError as e:
            self._errors.append(str(e))
            return ProgContext([])
    
    def _check_brackets(self):
        stack = []
        for i, token in enumerate(self.tokens):
            if token.type == brainfuckLexer.T__0:  # '['
                stack.append((i, token.line, token.column))
            elif token.type == brainfuckLexer.T__1:  # ']'
                if not stack:
                    raise SyntaxError(f"Unmatched ']' at line {token.line}, column {token.column}")
                stack.pop()
        
        if stack:
            pos, line, col = stack[-1]
            raise SyntaxError(f"Unclosed '[' at line {line}, column {col}")
    
    def _parse_expr(self) -> Optional[ExprContext]:
        if self.pos >= self.length:
            return None
        
        token = self.tokens[self.pos]
        
        if token.type == brainfuckLexer.T__0:  # '['
            return self._parse_loop()
        elif token.type == brainfuckLexer.T__1:  # ']'
            raise SyntaxError(f"Unmatched ']' at line {token.line}, column {token.column}")
        elif token.type == brainfuckLexer.COMMAND:
            self.pos += 1
            return ExprContext(command=token.text)
        else:
            raise SyntaxError(f"Unexpected token type {token.type} at line {token.line}, column {token.column}")
    
    def _parse_loop(self) -> ExprContext:
        #Парсим цикл [ ... ]
        start_token = self.tokens[self.pos]
        self.pos += 1  # Пропускаем '['
        
        inner_exprs = []
        
        # содержимое цикла до закрывающей скобки
        while self.pos < self.length and self.tokens[self.pos].type != brainfuckLexer.T__1:
            expr = self._parse_expr()
            if expr:
                inner_exprs.append(expr)
        
        # Проверка,что нашли закрывающую скобку
        if self.pos >= self.length:
            raise SyntaxError(f"Unclosed '[' at line {start_token.line}, column {start_token.column}")
        
        self.pos += 1  # Пропускаем ']'
        
        return ExprContext(exprs=inner_exprs)
    
    def removeErrorListeners(self):
        pass
    
    def addErrorListener(self, listener):
        self.error_listener = listener
    
    @property
    def errors(self):
        return self._errors


class BrainfuckParser:
    
    def __init__(self, token_stream: CommonTokenStream):
        self.token_stream = token_stream
        self._parser = TokenParser(token_stream)
        self._errors = []
    
    def prog(self):
        return self._parser.prog()
    
    def removeErrorListeners(self):
        pass
    
    def addErrorListener(self, listener):
        self.error_listener = listener
    
    @property
    def errors(self):
        return self._parser.errors
