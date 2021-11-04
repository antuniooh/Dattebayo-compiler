from Tokens.TokenEnum import TokenEnum as te
from Tokens.Token import Token
from Interpreters.Errors import NotMatch
from Interpreters.Expression import Expression
from Interpreters.OperationInterpreter import OperationInterpreter
from Interpreters.Common.Values import Values

"""
Class for variables declaration without initialization

                        GLC
VariableInitialization : (VariableType)* IDENTIFIER HAKU Values
VariableType : RASENGAN | RAIKIRI | ZETSU | KUCHIYOSE
Values : Num | STRING | BOOLEAN | IDENTIFIER | NumOperation | StrOperation
Num : INT | FLOAT
NumOperation : (Num | IDENTIFIER) , Operation , (Num | IDENTIFIER) , [{Operation , (Num | IDENTIFIER)}] ;
StrOperation : STRING , FUUMASHURIKEN , STRING , [{FUUMASHURIKEN , STRING}] ;
Operation ⇐ FUUMASHURIKEN | KUNAI | SHURIKEN | KATANA ;
"""


class VariableInitialization(Expression):
    def __init__(self, token_index: int, token_array=None):
        super().__init__(token_index, token_array)
        self.values_interpreter = Values(token_index, token_array)

    def run_glc(self):
        try:
            result = self.var_ini_glc()
            return [True, self.token_index, f'Variable initialized with {result[2]}']
        except:
            return [False, self.token_index, None]

    def var_ini_glc(self):
        try:
            self.variable_type()
        except:
            pass

        self.eat(te.IDENTIFIER)
        self.eat(te.HAKU)

        type_value = self.check_type_value()

        self.end_point()

        return type_value

    def variable_type(self):
        """VariableType : RASENGAN | RAIKIRI | ZETSU | KUCHIYOSE"""

        token = self.current_token

        if token.type == te.RASENGAN:
            self.eat(te.RASENGAN)
        elif token.type == te.RAIKIRI:
            self.eat(te.RAIKIRI)
        elif token.type == te.ZETSU:
            self.eat(te.ZETSU)
        elif token.type == te.KUCHIYOSE:
            self.eat(te.KUCHIYOSE)
        else:
            self.error()

    def check_type_value(self):
        self.values_interpreter = Values(self.token_index, self.tokens)
        type_value = self.values_interpreter.run_glc()

        if type_value[0]:
            self.marker_index = type_value[1]
            self.update_interpreter_params()

        return type_value