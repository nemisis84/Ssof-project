import json
from Pattern import Pattern
from MultiLabelling import MultiLabelling
from Vulnerabilities import Vulnerabilities
from Policy import Policy
from MultiLabel import MultiLabel
from Label import Label
from Ast import export_dict, get_traces
import ast
from Ast import ExecutionTrace

class Code_analyzer:
    def __init__(self, patterns, code):
        self.WHILE_LOOP_LIMIT = 3
        self.policy = self.create_policy(patterns)
        self.tree = self.import_tree(code)
        self.multi_labelling = MultiLabelling()
        self.vulnerability = Vulnerabilities()


    def import_tree(self, filename):
        with open(filename, 'r') as file:
            source = file.read()
        tree = ast.parse(source, filename)
        return tree
    
    def create_policy(self, input_file):
        with open(input_file, 'r') as file:
            data = json.load(file)
        
        patterns = []
        for pattern in data:
            vulnerability = pattern.get("vulnerability", "")
            sources = pattern.get("sources", [])
            sanitizers = pattern.get("sanitizers", [])
            sinks = pattern.get("sinks", [])
            implicit = pattern.get("implicit", "")
            pattern = Pattern(vulnerability, sources, sanitizers, sinks, implicit)
            patterns.append(pattern)
        
        policy = Policy(patterns)
        return policy

    def is_source(self, input):
        # Assuming `input` is a string representing a variable or function name
        return self.policy.get_names_with_source(input)

    def is_sanitizer(self, input):
        # Assuming `input` is a string representing a variable or function name
        return self.policy.get_names_with_sanitizer(input)

    def is_sink(self, input):
        # Assuming `input` is a string representing a variable or function name
        return self.policy.get_names_with_sink(input)

    def add_source(self, source, pattern_name):
        # Create a multilabel with this source
        multi_label = MultiLabel()
        pattern = self.policy.get_pattern(pattern_name)
        label = Label()
        label.add_source((source, {}))
        multi_label.add_label(pattern, label)

        self.multi_labelling.add_multilabel(source, MultiLabel)

    def add_multilabel(self, variable_name, label):
        multi_label = MultiLabel()
        

    def add_sanitizer(self, sanitizer, pattern_name):
        # Check if pattern excist in a multilabel in Multilabbeling.
        # Add a sanitizer if source is in any of the labels in the multilabel
        pass
    
    def handle_sink(self, sink, pattern):
        # What do we do with sinks?
        pass
    
    def has_matching_object(self, list1, list2):
        for item1 in list1:
            for item2 in list2:
                if item1 == item2:
                    return item1
        return False


    def walk_tree(self):
        all_traces = []
        initial_trace = ExecutionTrace()
        all_traces.append(initial_trace)
        self.traverse_ast(self.tree, initial_trace, all_traces)
        return all_traces

    def traverse_ast(self, node, current_trace, all_traces, assignment = False):

        if isinstance(node, ast.Module):
            for child_node in node.body:
                self.traverse_ast(child_node, current_trace, all_traces)


        elif isinstance(node, ast.Expr):
            current_trace.add_statement(node)
            self.traverse_ast(node.value, current_trace, all_traces)

        elif isinstance(node, ast.Assign):
            
            variable_name = node.targets[0].id #Assumes only one assignment when assigning to variables. 
            self.multi_labelling.add_multilabel(variable_name, MultiLabel())

            current_trace.add_statement(node)
            for target in node.targets:
                self.traverse_ast(target, current_trace, all_traces)
            self.traverse_ast(node.value, current_trace, all_traces, assignment=variable_name)

        elif isinstance(node, (ast.If)):
            else_trace = current_trace.deep_copy()
    
            # trace for if
            current_trace.add_statement(node)
            for body_child_node in node.body:
                self.traverse_ast(body_child_node, current_trace, all_traces)
            
            # trace for else
            current_trace.add_child_trace(else_trace)
            all_traces.append(else_trace)
            if len(node.orelse) > 0:
                else_trace.add_statement(node)

                for orelse_child_node in node.orelse:
                    self.traverse_ast(orelse_child_node, else_trace, all_traces)

        elif isinstance(node, (ast.While)):
            for i in range(1, self.WHILE_LOOP_LIMIT+1):
                while_trace = current_trace.deep_copy()
                current_trace.add_child_trace(while_trace)
                all_traces.append(while_trace)

                for _ in range(i):
                    while_trace.add_statement(node)
                    for child_node in node.body:
                        self.traverse_ast(child_node, while_trace, all_traces)
        
        # Expressions
        elif isinstance(node, ast.Constant):
            current_trace.add_statement(node)

        elif isinstance(node, ast.Name):
            current_trace.add_statement(node)
            return node

        elif isinstance(node, ast.BinOp):
            current_trace.add_statement(node)
            self.traverse_ast(node.left, current_trace, all_traces)
            self.traverse_ast(node.op, current_trace, all_traces)
            self.traverse_ast(node.right, current_trace, all_traces)

        elif isinstance(node, ast.UnaryOp):
            current_trace.add_statement(node)
            self.traverse_ast(node.op, current_trace, all_traces)
            self.traverse_ast(node.operand, current_trace, all_traces)

        elif isinstance(node, ast.BoolOp):
            current_trace.add_statement(node)
            for value in node.values:
                self.traverse_ast(value, current_trace, all_traces)

        elif isinstance(node, ast.Compare):
            current_trace.add_statement(node)
            self.traverse_ast(node.left, current_trace, all_traces)
            for op in node.ops:
                self.traverse_ast(op, current_trace, all_traces)
            for comparator in node.comparators:
                self.traverse_ast(comparator, current_trace, all_traces)

        elif isinstance(node, ast.Call):
            current_trace.add_statement(node)
            self.traverse_ast(node.func, current_trace, all_traces)
            call_name = node.func.id
            pattern_sink = self.is_sink(call_name)
            pattern_sanitizer = self.is_sanitizer(call_name)

            if not node.args and self.is_source(call_name): # No arguments in call. f.ex. f()
                pattern_source = self.is_source(call_name)
                pattern_object = self.policy.get_pattern(pattern_source[0]) # assumes only one matching pattern
                is_sanitized = self.has_matching_object(pattern_sanitizer, pattern_source)
                label = Label([(call_name, {})])
                multi_label = MultiLabel({pattern_object.get_name(): (pattern_object, label)})
            for arg in node.args: # Loop over arguments f(a,b,...)
                inner_node = self.traverse_ast(arg, current_trace, all_traces)
                call_input = inner_node.id
                if call_input in self.multi_labelling.get_multi_labels():
                    multi_label = self.multi_labelling.get_multi_label(call_input)
                else:
                    pattern_source = self.is_source(call_input)
                    pattern_object = self.policy.get_pattern(pattern_source[0]) # assumes only one matching pattern
                    is_sanitized = self.has_matching_object(pattern_sanitizer, pattern_source)
                                            
                    label = Label([(call_input, {})]) if is_sanitized else Label([(call_input, {call_name})])
                    multi_label = MultiLabel({pattern_object.get_name(): (pattern_object, label)})
                    
                if pattern_sink:
                    illegal_flow = self.policy.corresponding_illegal_flow(call_name, multi_label)
                    self.vulnerability.report_vulnerability(call_name, illegal_flow)
            if assignment:
                self.multi_labelling.add_multilabel(assignment, multi_label)
            
            

        elif isinstance(node, ast.Attribute):
            current_trace.add_statement(node)
            self.traverse_ast(node.value, current_trace, all_traces)
    
    def pretty_print_traces(self, traces):
        for trace in traces:
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

if __name__ == "__main__":
    code_file = "1a-basic-flow"
    patterns = f"../slices/{code_file}.patterns.json"
    code = f"../slices/{code_file}.py"
    analyzer = Code_analyzer(patterns, code)
    traces = analyzer.walk_tree()
    print(analyzer.vulnerability.get_all_vulnerabilities())
    analyzer.pretty_print_traces(traces)