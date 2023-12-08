import ast
from astexport.export import export_dict

STATEMENTS = {ast.Expr, ast.Assign, ast.If, ast.While}

class PrintNodeInfoVisitor(ast.NodeVisitor):
    def generic_visit(self, node):
        print(f"ast_type: {node.__class__.__name__}")
        if hasattr(node, 'lineno'):
            print(f"lineno: {node.lineno}")
        ast.NodeVisitor.generic_visit(self, node)

def get_complete_traces(tree):
    traces = {}
    
    for node in tree.body:
        if node.__class__ == ast.Expr:
            print("yes")
        print(f"ast_type: {node.__class__.__name__}")
   
# get source code
filename = './slices/4a-conds-branching.py'
with open(filename, 'r') as file:
    source = file.read()

# create ast and json objects
tree = ast.parse(source, filename)
json_dict = export_dict(tree)
print(json_dict)

# traverse tree and print info for each node
# PrintNodeInfoVisitor().visit(tree)

get_complete_traces(tree)

