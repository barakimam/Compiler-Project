from structures import Token

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None
        self.keywords = {'print', 'if', 'else', 'while', 'def', 'return'}

    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def get_number(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_identifier(self):
        result = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        
        token_type = result.upper() if result in self.keywords else 'IDENTIFIER'
        return Token(token_type, result)
    
    def get_relational_op(self):
        op = self.current_char
        self.advance()
        if self.current_char == '=':
            op += self.current_char
            self.advance()
        return Token('REL_OP', op)

    def tokenize(self):
        tokens = []
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            
            if self.current_char.isdigit():
                tokens.append(Token('NUMBER', self.get_number()))
                continue

            if self.current_char.isalnum() or self.current_char == '_':
                tokens.append(self.get_identifier())
                continue

            if self.current_char in ('>', '<', '!'):
                if self.current_char == '!' and self.text[self.pos+1] == '=':
                    self.advance()
                    self.advance()
                    tokens.append(Token('REL_OP', '!='))
                    continue
                tokens.append(self.get_relational_op())
                continue
            
            token_map = {
                '+': 'PLUS', '-': 'MINUS', '*': 'TIMES', '/': 'DIVIDE',
                '=': 'ASSIGN', '(': 'LPAREN', ')': 'RPAREN', ';': 'SEMICOLON',
                '{': 'LBRACE', '}': 'RBRACE', ',': 'COMMA'
            }
            if self.current_char in token_map:
                if self.current_char == '=' and self.text[self.pos+1] == '=':
                    self.advance()
                    self.advance()
                    tokens.append(Token('REL_OP', '=='))
                else:
                    tokens.append(Token(token_map[self.current_char], self.current_char))
                    self.advance()
                continue

            raise Exception(f"Invalid character: {self.current_char}")
        
        tokens.append(Token('EOF', None))
        return tokens