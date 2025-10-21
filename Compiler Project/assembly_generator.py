class AssemblyGenerator:
    def __init__(self, tac_code):
        self.tac_code = tac_code
        self.assembly_code = []

    def is_number(self, s):
        try:
            if s is None: return False
            int(s)
            return True
        except (ValueError, TypeError):
            return False

    def get_operand(self, operand):
        if self.is_number(operand):
            return f"#{operand}"
        return operand

    def generate(self):
        for instr in self.tac_code:
            parts = instr.split()
            if len(parts) == 0: continue
            
            if instr.strip().endswith(':'):
                self.assembly_code.append(f"\n{instr.strip()}")
                continue

            op = parts[0]
            

            if 'call' in parts:
                dest = parts[0]
                func_name = parts[3]
                self.assembly_code.append(f"  CALL {func_name.replace(',', '')}")
                self.assembly_code.append(f"  STORE AX, {dest}")
                continue

            if op == 'if_false':
                condition, _, label = parts[1], parts[2], parts[3]
                self.assembly_code.append(f"  LOAD {self.get_operand(condition)}, R1")
                self.assembly_code.append(f"  CMP R1, #0")
                self.assembly_code.append(f"  JE {label}")
            elif op == 'goto':
                self.assembly_code.append(f"  JMP {parts[1]}")

            elif op == 'func_begin':
                self.assembly_code.append(f"\n{parts[1]}:")
                self.assembly_code.append("  PUSH BP")
                self.assembly_code.append("  MOV SP, BP")
            elif op == 'func_end':
                self.assembly_code.append("  POP BP")
                self.assembly_code.append("  RET")
            elif op == 'return':
                self.assembly_code.append(f"  LOAD {self.get_operand(parts[1])}, AX")
            elif op == 'param':
                self.assembly_code.append(f"  PUSH {self.get_operand(parts[1])}")
            elif op == 'get_param':
                self.assembly_code.append(f"  POP {parts[1]}")
            
            elif op == 'print':
                self.assembly_code.append(f"  PRINT {self.get_operand(parts[1])}")

            elif '=' in parts:
                dest = parts[0]
                if len(parts) == 3:
                    src = parts[2]
                    self.assembly_code.append(f"  LOAD {self.get_operand(src)}, R1")
                    self.assembly_code.append(f"  STORE R1, {dest}")
                elif len(parts) == 5:
                    src1, op_sym, src2 = parts[2], parts[3], parts[4]
                    op_code = {'+': 'ADD', '-': 'SUB', '*': 'MUL', '/': 'DIV', 
                               '>': 'CMPGT', '<': 'CMPLT', '==': 'CMPEQ', '!=': 'CMPNE'}.get(op_sym, "OP_ERR")
                    self.assembly_code.append(f"  LOAD {self.get_operand(src1)}, R1")
                    self.assembly_code.append(f"  LOAD {self.get_operand(src2)}, R2")
                    self.assembly_code.append(f"  {op_code} R1, R2")
                    self.assembly_code.append(f"  STORE R1, {dest}")
        
        return "\n".join(self.assembly_code)