class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}

    def visit(self, node):
        method_name = 'visit_' + node.type
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        for child in node.children:
            self.visit(child)

    def visit_program(self, node): self.generic_visit(node)
    def visit_statements(self, node): self.generic_visit(node)
    def visit_number(self, node): pass
    def visit_binop(self, node): self.generic_visit(node)
    def visit_relop(self, node): self.generic_visit(node)
    def visit_return(self, node): self.generic_visit(node)
    def visit_param(self, node): pass

    def visit_assign(self, node):
        var_name = node.children[0].value
        self.symbol_table[var_name] = 'variable'
        self.visit(node.children[1])

    def visit_identifier(self, node):
        if node.value not in self.symbol_table:
            raise NameError(f"Error: Variable or function '{node.value}' is not defined.")

    def visit_print(self, node):
        self.visit(node.children[0])

    def visit_if(self, node):
        self.visit(node.children[0])
        self.visit(node.children[1])
        if len(node.children) > 2 and node.children[2]:
            self.visit(node.children[2])
    
    def visit_while(self, node):
        self.visit(node.children[0])
        self.visit(node.children[1])

    def visit_func_def(self, node):
        func_name = node.children[0].value
        self.symbol_table[func_name] = 'function'
        for param_node in node.children[1:-1]:
             self.symbol_table[param_node.value] = 'variable'
        self.visit(node.children[-1])
    
    def visit_func_call(self, node):
        func_name = node.children[0].value
        if func_name not in self.symbol_table or self.symbol_table[func_name] != 'function':
            raise NameError(f"Error: Function '{func_name}' is not defined.")
        for arg_node in node.children[1:]:
            self.visit(arg_node)