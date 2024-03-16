class Error:
    def __init__(self, line, column, description, scope, kind):
        self.line = line
        self.column = column
        self.description = description
        self.scope = scope
        self.kind = kind

    def __str__(self):
        return f"{self.description} | {self.scope} | {self.line} | {self.column} | {self.kind}"
