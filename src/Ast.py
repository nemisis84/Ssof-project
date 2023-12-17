import ast
from astexport.export import export_dict

WHILE_LOOP_LIMIT = 3

# lab 3 exercise 2
class PrintNodeInfoVisitor(ast.NodeVisitor):
    def generic_visit(self, node):
        print(f"ast_type: {node.__class__.__name__}")
        if hasattr(node, 'lineno'):
            print(f"lineno: {node.lineno}")
        ast.NodeVisitor.generic_visit(self, node)

# lab 3 exercise 3
class ExecutionTrace:
    def __init__(self):
        self.statements = []
        self.child_traces = set()
    
    def add_child_trace(self, trace):
        self.child_traces.add(trace)

    def add_statement(self, statement):
        self.statements.append(statement)
        for child in self.child_traces:
            child.add_statement(statement)

    def deep_copy(self):
        result = ExecutionTrace()
        for statement in self.statements:
            result.add_statement(statement)
        return result

    def __str__(self):
        return ' -> '.join(map(str, self.statements))

def traverse_ast(node, current_trace, all_traces):

    if isinstance(node, ast.Module):
        for child_node in node.body:
            traverse_ast(child_node, current_trace, all_traces)
    
    elif isinstance(node, (ast.Expr, ast.Assign)):
        current_trace.add_statement(node.__class__.__name__)

    elif isinstance(node, (ast.If)):
        else_trace = current_trace.deep_copy()

        # trace for if
        current_trace.add_statement(node.__class__.__name__)
        for body_child_node in node.body:
            traverse_ast(body_child_node, current_trace, all_traces)
        
        # trace for else
        current_trace.add_child_trace(else_trace)
        all_traces.append(else_trace)
        if len(node.orelse) > 0:
            else_trace.add_statement("Else")

            for orelse_child_node in node.orelse:
                traverse_ast(orelse_child_node, else_trace, all_traces)

    elif isinstance(node, (ast.While)):
        for i in range(1, WHILE_LOOP_LIMIT+1):
            while_trace = current_trace.deep_copy()
            current_trace.add_child_trace(while_trace)
            all_traces.append(while_trace)

            for _ in range(i):
                while_trace.add_statement("While")
                for child_node in node.body:
                    traverse_ast(child_node, while_trace, all_traces)
                

def get_traces(node):
    all_traces = []
    initial_trace = ExecutionTrace()
    all_traces.append(initial_trace)

    traverse_ast(node, initial_trace, all_traces)
    return all_traces


def build_ats_tree(file_path):
    
    with open(file_path, 'r') as file:
        source = file.read()

    # create ast and json objects
    tree = ast.parse(source, file_path)
    json_dict = export_dict(tree)
    
    return tree, json_dict


if __name__ == "__main__":
    # get source code
    #filename = '../slices/5b-loops-unfolding.py'
    filename = 'slices/5b-loops-unfolding.py'
    
    tree, json_dict = build_ats_tree(filename)
    # print(json_dict)

    # lab 3 exercise 2
    # PrintNodeInfoVisitor().visit(tree)

    # lab 3 exercise 3
    for trace in get_traces(tree):
        print(trace)
        
