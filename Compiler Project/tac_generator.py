class TACGenerator:
    def __init__(self):
        self.temp_count = 0
        self.label_count = 0
        self.tac_code = []

    def new_temp(self):
        self.temp_count += 1
        return f"t{self.temp_count}"

    def new_label(self):
        self.label_count += 1
        return f"L{self.label_count}"

    def visit(self, node):
        method_name = 'visit_' + node.type
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        for child in node.children:
            self.visit(child)

    def visit_program(self, node): self.generic_visit(node)
    def visit_statements(self, node): self.generic_visit(node)
    
    def visit_number(self, node): return node.value
    def visit_identifier(self, node): return node.value
    def visit_param(self, node): return node.value
    
    def visit_assign(self, node):
        var_name = node.children[0].value
        expr_result = self.visit(node.children[1])
        self.tac_code.append(f"{var_name} = {expr_result}")

    def visit_binop(self, node):
        left = self.visit(node.children[0])
        right = self.visit(node.children[1])
        temp = self.new_temp()
        self.tac_code.append(f"{temp} = {left} {node.value} {right}")
        return temp
    
    def visit_relop(self, node):
        left = self.visit(node.children[0])
        right = self.visit(node.children[1])
        temp = self.new_temp()
        self.tac_code.append(f"{temp} = {left} {node.value} {right}")
        return temp

    def visit_if(self, node):
        condition_var = self.visit(node.children[0])
        label_after_if = self.new_label()
        self.tac_code.append(f"if_false {condition_var} goto {label_after_if}")
        self.visit(node.children[1])
        
        if len(node.children) > 2 and node.children[2]:
            label_after_else = self.new_label()
            self.tac_code.append(f"goto {label_after_else}")
            self.tac_code.append(f"{label_after_if}:")
            self.visit(node.children[2])
            self.tac_code.append(f"{label_after_else}:")
        else:
            self.tac_code.append(f"{label_after_if}:")

    def visit_while(self, node):
        label_start = self.new_label()
        label_end = self.new_label()
        self.tac_code.append(f"{label_start}:")
        condition_var = self.visit(node.children[0])
        self.tac_code.append(f"if_false {condition_var} goto {label_end}")
        self.visit(node.children[1])
        self.tac_code.append(f"goto {label_start}")
        self.tac_code.append(f"{label_end}:")
        
    def visit_func_def(self, node):
        func_name = node.children[0].value
        self.tac_code.append(f"func_begin {func_name}")
        for param in node.children[1:-1]:
            self.tac_code.append(f"get_param {param.value}")
        self.visit(node.children[-1])
        self.tac_code.append(f"func_end")
        
    def visit_func_call(self, node):
        func_name = node.children[0].value
        args = [self.visit(arg) for arg in node.children[1:]]
        for arg in reversed(args):
            self.tac_code.append(f"param {arg}")
        temp = self.new_temp()
        self.tac_code.append(f"{temp} = call {func_name}, {len(args)}")
        return temp

    def visit_return(self, node):
        return_val = self.visit(node.children[0])
        self.tac_code.append(f"return {return_val}")

    def visit_print(self, node):
        expr_to_print = self.visit(node.children[0])
        self.tac_code.append(f"print {expr_to_print}")