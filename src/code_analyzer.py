import copy
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

    def get_relevant_source_patterns(self, trace, name):
        relevant_patterns = []
        
        # any non-instantiated variable is to be considered as an entry point to all vulnerabilities
        if name in trace.get_unassigned_variables():
            return self.policy.get_patterns()
        
        # patterns in policy that have `name` as source
        relevant_patterns += self.policy.get_relevant_patterns(name, "source")
        return relevant_patterns
    
    def get_relevant_sink_patterns(self, name):
        return self.policy.get_relevant_patterns(name, "sink")
    
    def get_relevant_sanitizer_patterns(self, name):
        return self.policy.get_relevant_patterns(name, "sanitizer")

    def is_sink(self, name):
        return len(self.get_relevant_sink_patterns(name)) > 0

    def report(self, variable_name, multi_label, sink_lineno = None):
        if self.is_sink(variable_name):
            print(f"Report variable {variable_name}")
            illegal_flow = self.policy.corresponding_illegal_flow(variable_name, multi_label)
            self.vulnerability.report_vulnerability(variable_name, illegal_flow, sink_lineno)
        else:
            print("No illegal flow found")

    def is_unassigned_variable(self, trace, node):
        parent_node = trace.get_nodes()[-1]

        # function call or attribute is not an unassigned variable
        if isinstance(parent_node, ast.Call) or isinstance(parent_node, ast.Attribute):
            return False
        
        # variable is assigned if target of ast.Assign node
        unassigned = True
        for trace_node in trace.get_nodes():
            if isinstance(trace_node, ast.Assign):
                for target in trace_node.targets:
                    if target.id == node.id:
                        unassigned = False
        
        return unassigned

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

    def traverse_ast(self, node, current_trace, all_traces, assignment = False, parent_calls = []):

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
            current_trace.add_node(node)
            self.traverse_ast(node.value, current_trace, all_traces)

        elif isinstance(node, ast.Assign):
            
            # assume only one left hand variable in assignments
            left_variable_name = node.targets[0].id

            if left_variable_name in current_trace.get_unassigned_variables():
                current_trace.remove_unassigned_variable(left_variable_name)

            # if right hand part of assignment is a variable
            if isinstance(node.value, ast.Name):
                right_variable_name = node.value.id

                source_patterns = self.get_relevant_source_patterns(current_trace, right_variable_name)
                
                # for all patterns where right hand variable is a source (could be 0)
                for source_pattern_object in source_patterns:
                    label = Label([(right_variable_name, node.lineno, [[]])])
                    multi_label = MultiLabel({source_pattern_object.get_name(): (source_pattern_object, label)})
                    # print("Assign name to", left_variable_name, right_variable_name)
                    self.multi_labelling.add_multilabel(left_variable_name, multi_label)
                
                # if right hand variable is assigned before
                if right_variable_name in self.multi_labelling.get_multi_labels():
                    existing_multilabel = self.multi_labelling.get_multi_label(right_variable_name)

                    # todo: this seems like an unnecessary check
                    if left_variable_name in self.multi_labelling.get_multi_labels() and len(source_patterns) > 0: # Is the variable_name assigned assigned to the current value_variable_name (edge case handling)?
                        new_multi_label = self.multi_labelling.get_multi_label(left_variable_name).combine(existing_multilabel) # Combine
                        self.multi_labelling.multi_labels[left_variable_name] = new_multi_label
                    else: # Overwrite variable_name entry
                        self.multi_labelling.mutator(right_variable_name, left_variable_name)

                
                if self.is_sink(left_variable_name): # Report
                    # print(f"Reporting assignment: {left_variable_name}")
                    multi_label = self.multi_labelling.get_multi_label(left_variable_name)
                    self.report(left_variable_name, multi_label, node.lineno)

            elif isinstance(node.value, ast.Constant):
                # print("Assign constant to:", left_variable_name)
                self.multi_labelling.add_multilabel(left_variable_name, MultiLabel())

            current_trace.add_node(node)
            for target in node.targets:
                self.traverse_ast(target, current_trace, all_traces)
            self.traverse_ast(node.value, current_trace, all_traces, assignment=left_variable_name) # Continue traversal


        elif isinstance(node, (ast.If)):
            else_trace = current_trace.deep_copy()
    
            # trace for if
            current_trace.add_node(node)
            for body_child_node in node.body:
                self.traverse_ast(body_child_node, current_trace, all_traces)
            
            # trace for else
            current_trace.add_child_trace(else_trace)
            all_traces.append(else_trace)
            if len(node.orelse) > 0:
                else_trace.add_node(node)

                for orelse_child_node in node.orelse:
                    self.traverse_ast(orelse_child_node, else_trace, all_traces)

        elif isinstance(node, (ast.While)):
            for i in range(1, self.WHILE_LOOP_LIMIT+1):
                while_trace = current_trace.deep_copy()
                current_trace.add_child_trace(while_trace)
                all_traces.append(while_trace)

                for _ in range(i):
                    while_trace.add_node(node)
                    for child_node in node.body:
                        self.traverse_ast(child_node, while_trace, all_traces)
        
        #============================#
        # EXPRESSIONS
        #============================#
                        
        elif isinstance(node, ast.Constant):
            current_trace.add_node(node)

        elif isinstance(node, ast.Name):
            if self.is_unassigned_variable(current_trace, node):
                current_trace.add_unassigned_variable(node.id)
            current_trace.add_node(node)
            return node

        elif isinstance(node, ast.BinOp):
            # We need to report names, and ignore constants. It needs to be recursive. 
            current_trace.add_node(node)
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
            current_trace.add_node(node)
            self.traverse_ast(node.op, current_trace, all_traces)
            self.traverse_ast(node.operand, current_trace, all_traces)

        elif isinstance(node, ast.BoolOp):
            current_trace.add_node(node)
            for value in node.values:
                self.traverse_ast(value, current_trace, all_traces)

        elif isinstance(node, ast.Compare):
            current_trace.add_node(node)
            self.traverse_ast(node.left, current_trace, all_traces)
            for op in node.ops:
                self.traverse_ast(op, current_trace, all_traces)
            for comparator in node.comparators:
                self.traverse_ast(comparator, current_trace, all_traces)

        elif isinstance(node, ast.Call):
            current_trace.add_node(node)
            # self.traverse_ast(node.func, current_trace, all_traces)
            
            parent_calls = copy.deepcopy(parent_calls)
            parent_calls.append(node.func.id)

            # if call has arguments, loop over arguments
            inner_nodes = []
            for arg in node.args:
                inner_node = self.traverse_ast(arg, current_trace, all_traces, parent_calls=parent_calls)
                if type(inner_node) != list and inner_node:
                    inner_node = [inner_node]
                elif not inner_node:
                    inner_node = []
                inner_nodes.extend(inner_node)

            # if call has no arguments and is value of assignment
            if len(inner_nodes) == 0 and assignment != False:
                call_name = node.func.id
                source_patterns = self.get_relevant_source_patterns(current_trace, call_name)

                multi_label = MultiLabel()
                for source_pattern in source_patterns:
                    label = Label([(call_name, node.lineno, [[]])])
                    add_multi_label = MultiLabel({source_pattern.get_name(): (source_pattern, label)})
                    multi_label = multi_label.combine(add_multi_label)
                self.multi_labelling.add_multilabel(assignment, multi_label)
                self.report(assignment, multi_label, node.lineno)

            for name in inner_nodes:

                call_input = name.id
                print(f"Call input: {call_input}")
                input_source_patterns = self.get_relevant_source_patterns(current_trace, call_input)

                multi_label = MultiLabel()

                # call input is variable that was left hand part of assigment earlier
                # existing_multi_labels = self.multi_labelling.get_multi_labels()

                if call_input in self.multi_labelling.get_multi_labels():
                    add_multi_label = self.multi_labelling.get_multi_label(call_input)
                    multi_label = multi_label.combine(add_multi_label)

                for input_source_pattern in input_source_patterns:

                    label = Label([(call_input, node.lineno, [])])

                    # existing_label = multi_label.get_label(input_source_pattern)
                    # if existing_label.has_unsanitized_flow():
                    #     label = Label([(call_input, node.lineno, [])])
                    # else:
                    #     label = Label([(call_input, node.lineno, [[]])])

                    print(f"Input source pattern: {input_source_pattern.get_name()}")

                    add_multi_label = MultiLabel({input_source_pattern.get_name(): (input_source_pattern, label)})
                    multi_label = multi_label.combine(add_multi_label)

                sanitizer_flows = dict()
                for call_name in reversed(parent_calls):

                    sanitizer_patterns = self.get_relevant_sanitizer_patterns(call_name)

                    pattern_to_label_mappings = multi_label.get_pattern_to_label_mapping()
                    for (pattern, label) in pattern_to_label_mappings.values():
                        for label_info in label.get_sources():
                            source = label_info[0]

                            key = (label, source)
                            if key not in sanitizer_flows:
                                sanitizer_flows[key] = []
                        for sanitizer_pattern in sanitizer_patterns:
                            if pattern.get_name() == sanitizer_pattern.get_name():
                                sanitizer_flows[key].append((call_name, node.lineno))

                for (label, source), flow_list in sanitizer_flows.items():
                    label.remove_empty_sanitizer_flows()

                for (label, source), flow_list in sanitizer_flows.items():
                    label.add_sanitizer_flow_to_source(source, flow_list)

                for call_name in reversed(parent_calls):
                    if self.is_sink(call_name):
                        self.report(call_name, multi_label, node.lineno)

                if assignment:
                    self.multi_labelling.add_multilabel(assignment, multi_label)
                    self.report(assignment, multi_label, node.lineno)

            return node.func
            
        
        elif isinstance(node, ast.Attribute):
            # TODO: what if a sink calls on an attribute which is a source. 
            current_trace.add_node(node)
            self.traverse_ast(node.value, current_trace, all_traces)
    
    def pretty_print_traces(self, traces):
        for trace in traces:
            for i, node in enumerate(trace.nodes):
                is_last_node = (i == len(trace.nodes) - 1)
                end = "" if is_last_node else " -> "
                if isinstance(node, ast.Constant):
                    print(f"{node.__class__.__name__}: {node.value}", end=end)
                elif isinstance(node, ast.Name):
                    print(f"{node.__class__.__name__}: {node.id}", end=end)
                elif isinstance(node, ast.Attribute):
                    print(f"{node.__class__.__name__}: {node.attr}", end=end)
                else:
                    print(node.__class__.__name__, end=end)

if __name__ == "__main__":
    # code_file = "1b-basic-flow"
    code_file = "3b-expr-func-calls"
    patterns = f"slices/{code_file}.patterns.json"
    code = f"slices/{code_file}.py"
    analyzer = Code_analyzer(patterns, code)
    traces = analyzer.walk_tree()
    for vulnerabilities in analyzer.vulnerability.get_all_vulnerabilities():
        print(vulnerabilities)
    # analyzer.pretty_print_traces(traces)