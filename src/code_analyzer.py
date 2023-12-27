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
    def __init__(self, patterns_file, code_file):
        self.WHILE_LOOP_LIMIT = 3
        self.policy = self.import_policy(patterns_file)
        self.tree = self.import_tree(code_file)
        self.multi_labelling = MultiLabelling()
        self.vulnerability = Vulnerabilities()

    def import_tree(self, filename):
        with open(filename, 'r') as file:
            source = file.read()
        tree = ast.parse(source, filename)
        return tree
    
    def import_policy(self, input_file):
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

    def report(self, variable_name, multi_label, sink_lineno = None):
        if self.is_sink(variable_name):
            illegal_flow = self.policy.corresponding_illegal_flow(variable_name, multi_label)
            self.vulnerability.report_vulnerability(variable_name, illegal_flow, sink_lineno)
        else:
            print("No illegal flow found")
 

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

        #============================#
        # ROOT NODE
        #============================#

        if isinstance(node, ast.Module):
            for child_node in node.body:
                self.traverse_ast(child_node, current_trace, all_traces)

        #============================#
        # STATEMENTS
        #============================#

        elif isinstance(node, ast.Expr):
            current_trace.add_statement(node)
            self.traverse_ast(node.value, current_trace, all_traces)

        elif isinstance(node, ast.Assign):
            
            # assume only one left hand variable in assignments
            left_variable_name = node.targets[0].id 

            # if right hand part of assignment is a variable
            if isinstance(node.value, ast.Name):
                right_variable_name = node.value.id

                input_source_patterns = self.policy.get_relevant_patterns(right_variable_name, "source")
                
                # if right hand variable is a source in one of the patterns
                if len(input_source_patterns) > 0:
                    pattern_object = input_source_patterns[0]
                    label = Label([(right_variable_name, set(), node.lineno)])
                    multi_label = MultiLabel(node.lineno, {pattern_object.get_name(): (pattern_object, label)})
                    print("Assign name to", left_variable_name, right_variable_name)
                    self.multi_labelling.add_multilabel(left_variable_name, multi_label)
                
                # if right hand variable is assigned before
                if right_variable_name in self.multi_labelling.get_multi_labels():
                    existing_multilabel = self.multi_labelling.get_multi_label(right_variable_name)

                    # todo: this seems like an unnecessary check
                    if left_variable_name in self.multi_labelling.get_multi_labels() and len(input_source_patterns) > 0: # Is the variable_name assigned assigned to the current value_variable_name (edge case handling)?
                        new_multi_label = self.multi_labelling.get_multi_label(left_variable_name).combine(existing_multilabel) # Combine
                        self.multi_labelling.multi_labels[left_variable_name] = new_multi_label
                    else: # Overwrite variable_name entry
                        self.multi_labelling.mutator(right_variable_name, left_variable_name)

                
                if self.is_sink(left_variable_name): # Report
                    print(f"Reporting assignment: {left_variable_name}")
                    multi_label = self.multi_labelling.get_multi_label(left_variable_name)
                    self.report(left_variable_name, multi_label, node.lineno)

            elif isinstance(node.value, ast.Constant):
                print("Assign constant to:", left_variable_name)
                self.multi_labelling.add_multilabel(left_variable_name, MultiLabel())

            current_trace.add_statement(node)
            for target in node.targets: 
                self.traverse_ast(target, current_trace, all_traces)
            self.traverse_ast(node.value, current_trace, all_traces, assignment=left_variable_name) # Continue traversal


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
        
        #============================#
        # EXPRESSIONS
        #============================#
                        
        elif isinstance(node, ast.Constant):
            current_trace.add_statement(node)

        elif isinstance(node, ast.Name):
            current_trace.add_statement(node)
            return node

        elif isinstance(node, ast.BinOp):
            # We need to report names, and ignore constants. It needs to be recursive. 
            current_trace.add_statement(node)
            left_node = self.traverse_ast(node.left, current_trace, all_traces)
            node_op = self.traverse_ast(node.op, current_trace, all_traces)
            rigth_node = self.traverse_ast(node.right, current_trace, all_traces)
            names = []

            for node in [left_node, node_op, rigth_node]:
                if isinstance(node, ast.Name):
                    names.append(node)
                if type(node) == list:
                    names.extend(node)
            
            return names

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

            sink_patterns = self.policy.get_relevant_patterns(call_name, "sink")
            sanitizer_patterns = self.policy.get_relevant_patterns(call_name, "sanitizer")
            input_source_patterns = self.policy.get_relevant_patterns(call_name, "source")
            
            multi_label = MultiLabel()

            # if call has no arguments, call is a source and call is value of assignment
            if not node.args and len(input_source_patterns) > 0 and assignment != False:
                pattern_object = input_source_patterns[0]
                is_sanitized = self.has_matching_object(list(map(lambda x: x.get_name(), sanitizer_patterns)), list(map(lambda x: x.get_name(), input_source_patterns)))
                label = Label([(call_name, set(), node.lineno)])
                multi_label = MultiLabel(node.lineno, {pattern_object.get_name(): (pattern_object, label)})
                print(f"Assign function {call_name} to:", assignment)
                self.multi_labelling.add_multilabel(assignment, multi_label)
                self.report(assignment, multi_label, node.lineno)
                
                return
            
            # if call has arguments, loop over arguments first
            inner_nodes = []
            for arg in node.args:
                inner_node = self.traverse_ast(arg, current_trace, all_traces)
                if type(inner_node) != list and inner_node:
                    inner_node = [inner_node]
                elif not inner_node:
                    inner_node = []
                inner_nodes.extend(inner_node)

            for name in inner_nodes:

                call_input = name.id
                input_source_patterns = self.policy.get_relevant_patterns(call_name, "source")

                # call input is variable that was left hand part of assigment earlier
                if call_input in self.multi_labelling.get_multi_labels():
                    add_multi_label = self.multi_labelling.get_multi_label(call_input)
                    multi_label = multi_label.combine(add_multi_label)

                # call input is source
                if len(input_source_patterns) > 0:
                    pattern_object = input_source_patterns[0]

                    # check if call name is sanitizer of call input
                    is_sanitized = self.has_matching_object(list(map(lambda x: x.get_name(), sanitizer_patterns)), list(map(lambda x: x.get_name(), input_source_patterns)))
                    label = Label([(call_input, {call_name}, node.lineno)]) if is_sanitized else Label([(call_input, set(), node.lineno)])
                    
                    add_multi_label = MultiLabel(node.lineno, {pattern_object.get_name(): (pattern_object, label)})
                    multi_label = multi_label.combine(add_multi_label)

                # call name is sanitizer
                if len(sanitizer_patterns) > 0:
                    sanitizer_pattern = sanitizer_patterns[0]

                    if call_input in self.multi_labelling.get_multi_labels():
                        call_input_multi_label = self.multi_labelling.get_multi_label(call_input)
                        pattern_to_label_mappings = call_input_multi_label.get_pattern_to_label_mapping()
                        for (pattern, label) in pattern_to_label_mappings.values():
                            if pattern.get_name() == sanitizer_pattern.get_name():
                                for label_info in label.get_sources():
                                    source = label_info[0]
                                    label.add_sanitizer(source, call_name)

            if len(sink_patterns) > 0:
                print(f"Reporting function: {call_name}")

                self.report(call_name, multi_label, node.lineno)

            if assignment:
                print("Assign function to:", assignment)
                self.multi_labelling.add_multilabel(assignment, multi_label)
            
        elif isinstance(node, ast.Attribute):
            # TODO: what if a sink calls on an attribute which is a source. 
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
    # code_file = "1b-basic-flow"
    code_file = "1b-basic-flow"
    patterns = f"../slices/{code_file}.patterns.json"
    code = f"../slices/{code_file}.py"
    analyzer = Code_analyzer(patterns, code)
    traces = analyzer.walk_tree()
    for vulnerabilities in analyzer.vulnerability.get_all_vulnerabilities():
        print(vulnerabilities)
    analyzer.pretty_print_traces(traces)