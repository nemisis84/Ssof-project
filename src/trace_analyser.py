import json
from Pattern import Pattern
from MultiLabelling import MultiLabelling
from Vulnerabilities import Vulnerabilities
from Policy import Policy
from MultiLabel import MultiLabel
from Label import Label
from Ast import export_dict, get_traces
import ast



def create_policy(input_file):
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


def analyse_trace(trace, multilabelling=None, policy = None, vulnerability=None):
    multi_label = MultiLabel()
    for statement in trace.statements:
        id = statement.id
        value = statement.id

        source = policy.get_names_with_source(value)
        sink = policy.get_names_with_sink(value)
        sanitizer = policy.get_names_with_sanitizer(value)

        if source:
            if source not in multi_label.get_pattern_names():
                pattern = policy.get_pattern(source)
                label = Label()
                label.add_source((value, {}))
                multi_label.add_label(pattern, label)
            else:
                pattern = policy.get_pattern(source)
                label = Label()
                label.add_source((value, {}))
                



if __name__ == "__main__":
    filename = "../slices/4a-conds-branching.patterns.json"
    policy = create_policy(filename)
    print(policy)
    
    filename = "../slices/4a-conds-branching.py"
    with open(filename, 'r') as file:
        source = file.read()

    # create ast and json objects
    tree = ast.parse(source, filename)
    traces = get_traces(tree)
    analyse_trace(traces[0])