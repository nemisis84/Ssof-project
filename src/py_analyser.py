import json
from Pattern import Pattern
import ast
from astexport.export import export_dict

def main():
    slice_input = input()
    json_input = input()
    
    #If you want to test with an example
    
    #slice_input = "/home/ssof/Desktop/Ssoft/Ssof-project/slices/1a-basic-flow.py"
    #json_input = "/home/ssof/Desktop/Ssoft/Ssof-project/slices/1a-basic-flow.patterns.json"
    
    ast_tree = build_ats_tree(slice_input)
    patterns = read_json(json_input)
    
    
    
def read_json(file_path):
    patterns = []
    
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    for item in data:
        pattern = Pattern(item['vulnerability'], item['sources'], item['sanitizers'], item['sinks'], item['implicit']) #missing implicit flow flag
        patterns.append(pattern)
        
    return patterns


def build_ats_tree(file_path):
    
    with open(file_path, 'r') as file:
        source = file.read()

    # create ast and json objects
    tree = ast.parse(source, file_path)
    json_dict = export_dict(tree)
    
    return json_dict


    
if __name__ == "__main__":
    main()
    
    