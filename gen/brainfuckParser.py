# Generated from brainfuck.g4 by ANTLR 4.13.1
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,4,24,2,0,7,0,2,1,7,1,1,0,5,0,6,8,0,10,0,12,0,9,9,0,1,0,1,0,1,
        1,1,1,4,1,15,8,1,11,1,12,1,16,1,1,1,1,1,1,3,1,22,8,1,1,1,0,0,2,0,
        2,0,0,24,0,7,1,0,0,0,2,21,1,0,0,0,4,6,3,2,1,0,5,4,1,0,0,0,6,9,1,
        0,0,0,7,5,1,0,0,0,7,8,1,0,0,0,8,10,1,0,0,0,9,7,1,0,0,0,10,11,5,0,
        0,1,11,1,1,0,0,0,12,14,5,1,0,0,13,15,3,2,1,0,14,13,1,0,0,0,15,16,
        1,0,0,0,16,14,1,0,0,0,16,17,1,0,0,0,17,18,1,0,0,0,18,19,5,2,0,0,
        19,22,1,0,0,0,20,22,5,3,0,0,21,12,1,0,0,0,21,20,1,0,0,0,22,3,1,0,
        0,0,3,7,16,21
    ]

class brainfuckParser ( Parser ):

    grammarFileName = "brainfuck.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'['", "']'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "COMMAND", 
                      "WS" ]

    RULE_prog = 0
    RULE_expr = 1

    ruleNames =  [ "prog", "expr" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    COMMAND=3
    WS=4

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.1")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ProgContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(brainfuckParser.EOF, 0)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(brainfuckParser.ExprContext)
            else:
                return self.getTypedRuleContext(brainfuckParser.ExprContext,i)


        def getRuleIndex(self):
            return brainfuckParser.RULE_prog

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterProg" ):
                listener.enterProg(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitProg" ):
                listener.exitProg(self)




    def prog(self):

        localctx = brainfuckParser.ProgContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_prog)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 7
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==1 or _la==3:
                self.state = 4
                self.expr()
                self.state = 9
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 10
            self.match(brainfuckParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(brainfuckParser.ExprContext)
            else:
                return self.getTypedRuleContext(brainfuckParser.ExprContext,i)


        def COMMAND(self):
            return self.getToken(brainfuckParser.COMMAND, 0)

        def getRuleIndex(self):
            return brainfuckParser.RULE_expr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpr" ):
                listener.enterExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpr" ):
                listener.exitExpr(self)




    def expr(self):

        localctx = brainfuckParser.ExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_expr)
        self._la = 0 # Token type
        try:
            self.state = 21
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [1]:
                self.enterOuterAlt(localctx, 1)
                self.state = 12
                self.match(brainfuckParser.T__0)
                self.state = 14 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 13
                    self.expr()
                    self.state = 16 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not (_la==1 or _la==3):
                        break

                self.state = 18
                self.match(brainfuckParser.T__1)
                pass
            elif token in [3]:
                self.enterOuterAlt(localctx, 2)
                self.state = 20
                self.match(brainfuckParser.COMMAND)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





