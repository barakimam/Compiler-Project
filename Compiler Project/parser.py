from structures import ASTNode

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_index = 0
        self.current_token = self.tokens[self.token_index]

    def advance(self):
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]

    def expect(self, token_type):
        if self.current_token.type == token_type:
            token_value = self.current_token.value
            self.advance()
            return token_value
        else:
            raise Exception(f"Syntax Error: Expected {token_type}, got {self.current_token.type} at index {self.token_index}")


    def factor(self):
        token = self.current_token
        if token.type == 'NUMBER':
            self.advance()
            return ASTNode('number', value=token.value)
        elif token.type == 'IDENTIFIER':
            if self.token_index + 1 < len(self.tokens) and self.tokens[self.token_index + 1].type == 'LPAREN':
                return self.function_call()
            self.advance()
            return ASTNode('identifier', value=token.value)
        elif token.type == 'LPAREN':
            self.advance()
            node = self.expression()
            self.expect('RPAREN')
            return node
        raise Exception(f"Invalid factor: {token.type}")

    def term(self):
        node = self.factor()
        while self.current_token.type in ('TIMES', 'DIVIDE'):
            op = self.current_token.value
            self.advance()
            node = ASTNode('binop', children=[node, self.factor()], value=op)
        return node
    
    def additive_expression(self):
        node = self.term()
        while self.current_token.type in ('PLUS', 'MINUS'):
            op = self.current_token.value
            self.advance()
            node = ASTNode('binop', children=[node, self.term()], value=op)
        return node
        
    def expression(self):
        node = self.additive_expression()
        if self.current_token.type == 'REL_OP':
             op = self.current_token.value
             self.advance()
             node = ASTNode('relop', children=[node, self.additive_expression()], value=op)
        return node

    def statement(self):
        if self.current_token.type == 'IF':
            return self.if_statement()
        if self.current_token.type == 'WHILE':
            return self.while_statement()
        
        node = None
        if self.current_token.type == 'IDENTIFIER':
            if self.token_index + 1 < len(self.tokens) and self.tokens[self.token_index + 1].type == 'LPAREN':
                node = self.function_call()
            else:
                node = self.assignment_statement()
        elif self.current_token.type == 'PRINT':
            node = self.print_statement()
        elif self.current_token.type == 'RETURN':
            node = self.return_statement()
        else:
            raise Exception(f"Invalid statement starting with {self.current_token.type}")
        
        self.expect('SEMICOLON')
        return node

    def statement_block(self):
        self.expect('LBRACE')
        statements = []
        while self.current_token.type != 'RBRACE':
            statements.append(self.statement())
        self.expect('RBRACE')
        return ASTNode('statements', children=statements)

    def assignment_statement(self):
        identifier = self.expect('IDENTIFIER')
        self.expect('ASSIGN')
        expr = self.expression()
        return ASTNode('assign', children=[ASTNode('identifier', value=identifier), expr], value='=')

    def print_statement(self):
        self.expect('PRINT')
        expr = self.expression()
        return ASTNode('print', children=[expr])

    def if_statement(self):
        self.expect('IF')
        self.expect('LPAREN')
        condition = self.expression()
        self.expect('RPAREN')
        if_block = self.statement_block()
        else_block = None
        if self.current_token.type == 'ELSE':
            self.advance()
            else_block = self.statement_block()
        return ASTNode('if', children=[condition, if_block, else_block] if else_block else [condition, if_block])

    def while_statement(self):
        self.expect('WHILE')
        self.expect('LPAREN')
        condition = self.expression()
        self.expect('RPAREN')
        body = self.statement_block()
        return ASTNode('while', children=[condition, body])

    def function_definition(self):
        self.expect('DEF')
        name = self.expect('IDENTIFIER')
        self.expect('LPAREN')
        params = []
        if self.current_token.type == 'IDENTIFIER':
            params.append(ASTNode('param', value=self.expect('IDENTIFIER')))
            while self.current_token.type == 'COMMA':
                self.advance()
                params.append(ASTNode('param', value=self.expect('IDENTIFIER')))
        self.expect('RPAREN')
        body = self.statement_block()
        return ASTNode('func_def', children=[ASTNode('identifier', value=name)] + params + [body])

    def function_call(self):
        name = self.expect('IDENTIFIER')
        self.expect('LPAREN')
        args = []
        if self.current_token.type != 'RPAREN':
            args.append(self.expression())
            while self.current_token.type == 'COMMA':
                self.advance()
                args.append(self.expression())
        self.expect('RPAREN')
        return ASTNode('func_call', children=[ASTNode('identifier', value=name)] + args)

    def return_statement(self):
        self.expect('RETURN')
        value = self.expression()
        return ASTNode('return', children=[value])

    def parse(self):
        declarations = []
        while self.current_token.type != 'EOF':
            if self.current_token.type == 'DEF':
                declarations.append(self.function_definition())
            else:
                declarations.append(self.statement())
        return ASTNode('program', children=declarations)

