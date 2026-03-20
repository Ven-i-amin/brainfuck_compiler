# error_listener.py
from antlr4.error.ErrorListener import ErrorListener


class CustomErrorListener(ErrorListener):
    #Обработчик ошибок парсера ANTLR

    def __init__(self):
        self.errors = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.errors.append({
            'line': line,
            'column': column,
            'message': msg
        })
        print(f"[PARSER ERROR] Строка {line}:{column} - {msg}")