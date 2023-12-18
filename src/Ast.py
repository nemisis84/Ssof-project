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


    elif isinstance(node, ast.Expr):
        current_trace.add_statement(node)
        traverse_ast(node.value, current_trace, all_traces)

    elif isinstance(node, ast.Assign):
        current_trace.add_statement(node)
        for target in node.targets:
            traverse_ast(target, current_trace, all_traces)
        traverse_ast(node.value, current_trace, all_traces)

    elif isinstance(node, (ast.If)):
        else_trace = current_trace.deep_copy()

        # trace for if
        current_trace.add_statement(node)
        for body_child_node in node.body:
            traverse_ast(body_child_node, current_trace, all_traces)
        
        # trace for else
        current_trace.add_child_trace(else_trace)
        all_traces.append(else_trace)
        if len(node.orelse) > 0:
            else_trace.add_statement(node)

            for orelse_child_node in node.orelse:
                traverse_ast(orelse_child_node, else_trace, all_traces)

    elif isinstance(node, (ast.While)):
        for i in range(1, WHILE_LOOP_LIMIT+1):
            while_trace = current_trace.deep_copy()
            current_trace.add_child_trace(while_trace)
            all_traces.append(while_trace)

            for _ in range(i):
                while_trace.add_statement(node)
                for child_node in node.body:
                    traverse_ast(child_node, while_trace, all_traces)
    
    # Expressions
    elif isinstance(node, ast.Constant):
        current_trace.add_statement(node)

    elif isinstance(node, ast.Name):
        current_trace.add_statement(node)

    elif isinstance(node, ast.BinOp):
        current_trace.add_statement(node)
        traverse_ast(node.left, current_trace, all_traces)
        traverse_ast(node.op, current_trace, all_traces)
        traverse_ast(node.right, current_trace, all_traces)

    elif isinstance(node, ast.UnaryOp):
        current_trace.add_statement(node)
        traverse_ast(node.op, current_trace, all_traces)
        traverse_ast(node.operand, current_trace, all_traces)

    elif isinstance(node, ast.BoolOp):
        current_trace.add_statement(node)
        for value in node.values:
            traverse_ast(value, current_trace, all_traces)

    elif isinstance(node, ast.Compare):
        current_trace.add_statement(node)
        traverse_ast(node.left, current_trace, all_traces)
        for op in node.ops:
            traverse_ast(op, current_trace, all_traces)
        for comparator in node.comparators:
            traverse_ast(comparator, current_trace, all_traces)

    elif isinstance(node, ast.Call):
        current_trace.add_statement(node)
        traverse_ast(node.func, current_trace, all_traces)
        for arg in node.args:
            traverse_ast(arg, current_trace, all_traces)

    elif isinstance(node, ast.Attribute):
        current_trace.add_statement(node)
        traverse_ast(node.value, current_trace, all_traces)

def get_traces(node):
    all_traces = []
    initial_trace = ExecutionTrace()
    all_traces.append(initial_trace)

    traverse_ast(node, initial_trace, all_traces)
    return all_traces



if __name__ == "__main__":
    # get source code
    # filename = '../slices/1a-basic-flow.py'
    # filename = "../slices/3c-expr-attributes.py"
    # filename = "../slices/9-regions-guards.py"
    filename = "../slices/4a-conds-branching.py"
    # filename = "../slices/5a-loops-unfolding.py"
    # filename = "../slices/7-conds-implicit.py"
    # filename = "../slices/3a-expr-func-calls.py"
    with open(filename, 'r') as file:
        source = file.read()

    # create ast and json objects
    tree = ast.parse(source, filename)
    json_dict = export_dict(tree)
    # print(json_dict)
    
    # lab 3 exercise 2
    # PrintNodeInfoVisitor().visit(tree)

    # lab 3 exercise 3

    for trace in get_traces(tree):
        for i, statement in enumerate(trace.statements):
            is_last_statement = (i == len(trace.statements) - 1)
            end = "" if is_last_statement else " -> "
            if isinstance(statement, ast.Constant):
                print(f"{statement.__class__.__name__}: {statement.value}", end=end)
            elif isinstance(statement, ast.Name):
                print(f"{statement.__class__.__name__}: {statement.id}", end=end)
            elif isinstance(statement, ast.Attribute):
                print(f"{statement.__class__.__name__}: {statement.attr}", end=end)
            else:
                print(statement.__class__.__name__, end=end)
        print()
    