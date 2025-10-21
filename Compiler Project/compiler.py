from lexer import Lexer
from parser import Parser
from semantic import SemanticAnalyzer
from tac_generator import TACGenerator
from assembly_generator import AssemblyGenerator
from structures import ASTNode

def print_ast(node, level=0):
    indent = "  " * level
    info = f"{node.type}"
    if node.value is not None: info += f" -> {node.value}"
    print(indent + info)
    for child in node.children:
        print_ast(child, level + 1)

def compile_source(source_code):
    
    print("--- 1. Lexical Analysis (Tokens) ---")
    lexer = Lexer(source_code)
    tokens = lexer.tokenize()
    for token in tokens: print(token)

    print("\n--- 2. Parsing (Abstract Syntax Tree) ---")
    parser = Parser(tokens)
    ast = parser.parse()
    print_ast(ast)

    print("\n--- 3. Semantic Analysis ---")
    semantic_analyzer = SemanticAnalyzer()
    try:
        semantic_analyzer.visit(ast)
        print("Semantic analysis successful.")
    except NameError as e:
        print(e)
        return

    print("\n--- 4. Three-Address Code (TAC) ---")
    tac_generator = TACGenerator()
    tac_generator.visit(ast)
    for tac_line in tac_generator.tac_code: print(tac_line)
    
    print("\n--- 5. Assembly Code Generation ---")
    assembly_generator = AssemblyGenerator(tac_generator.tac_code)
    assembly_code = assembly_generator.generate()
    print(assembly_code)

if __name__ == '__main__':
    code = """
    def get_max(a, b) {
        if (a > b) {
            return a;
        } else {
            return b;
        }
    }
    
    x = 15;
    y = 25;
    max_val = get_max(x, y);
    print max_val;

    i = 0;
    while (i < 3) {
        i = i + 1;
    }
    print i;
    """
    
    compile_source(code)