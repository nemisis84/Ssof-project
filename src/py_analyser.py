import json
import Pattern
import ast
from astexport.export import export_dict

def main():
    slice_input = input()
    json_input = input()
    
    ast_tree = build_ats_tree(slice_input)
    patterns = read_json(json_input)
    
    print(ast_tree)
    print(patterns)
    
     
#Not sure where the inplicit flag is going to go 
def read_json(file_path):
    patterns = []
    
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    for item in data:
        pattern = Pattern(item['vulnerability'], item['sources'], item['sanitizers'], item['sinks']) #missing implicit flow flag
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
    
    