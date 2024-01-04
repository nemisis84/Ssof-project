from code_analyzer import Code_analyzer
import sys
import json

code_file = "3a-expr-func-calls"
patterns = f"slices/{code_file}.patterns.json"
code = f"slices/{code_file}.py"


def analyze_py(slice_file, patterns_file):

    analyzer = Code_analyzer(patterns_file, slice_file)
    analyzer.walk_tree()

    vulnerabilities = analyzer.vulnerability.get_all_vulnerabilities()

    return vulnerabilities

def save_to_output_file(output_filename, output_data):

    with open(output_filename, 'w') as f:
        json.dump(output_data, f)

def main():

    if len(sys.argv) != 3:
        print("Usage: py_analyser.py <slice>.py <patterns>.json")
        sys.exit(1)

    slice = sys.argv[1]
    patterns = sys.argv[2]

    vulnerabilities = analyze_py(slice, patterns)

    output_filename = f"./output/{slice.split('.')[1].split('/')[-1]}.output.json"

    save_to_output_file(output_filename, vulnerabilities)

    print(f"Analysis result saved to {output_filename}")

main()