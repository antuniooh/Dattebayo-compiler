from Tokens.TokenEnum import TokenEnum as te
from Tokens.Token import Token
from Interpreters.Errors import NotMatch
from Interpreters.Expression import Expression

"""
Expressions for math operations

expr : term ((PLUS | MINUS) term)*
term : factor ((MUL | DIV) factor)*
factor : INTEGER
"""


class OperationInterpreter(Expression):
    def __init__(self, token_index: int, token_array=None):
        super().__init__(token_index, token_array)

    def run_glc(self):
        try:
            result = self.expr()
            return [True, self.token_index, "number"]
        except Exception as e:
            return [False, self.token_index, None]

    def factor(self):
        """factor : INTEGER"""
        token = self.current_token
        self.eat(te.INTEGER)
        return token.value

    def term(self):
        """term : factor ((MUL | DIV) factor)*"""
        result = self.factor()

        while self.current_token.type in (te.SHURIKEN, te.KATANA):
            token = self.current_token
            if token.type == te.SHURIKEN:
                self.eat(te.SHURIKEN)
                result = result * self.factor()
            elif token.type == te.KATANA:
                self.eat(te.KATANA)
                result = result / self.factor()

        return result

    def expr(self):
        """expr : term ((PLUS | MINUS) term)*"""
        result = self.term()

        while self.current_token.type in (te.FUUMASHURIKEN, te.KUNAI):
            token = self.current_token
            if token.type == te.FUUMASHURIKEN:
                self.eat(te.FUUMASHURIKEN)
                result = result + self.term()
            elif token.type == te.KUNAI:
                self.eat(te.KUNAI)
                result = result - self.term()
        return result