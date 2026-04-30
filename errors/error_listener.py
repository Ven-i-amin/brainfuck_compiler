from antlr4.error.ErrorListener import ErrorListener


class CustomErrorListener(ErrorListener):
    def __init__(self):
        self.errors = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.errors.append(
            {
                "line": line,
                "column": column,
                "message": msg,
            }
        )
        print(f"[PARSER ERROR] Line {line}:{column} - {msg}")
