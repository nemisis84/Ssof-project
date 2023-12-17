import json
from Pattern import Pattern
from Ast import *
import ast
from astexport.export import export_dict

def main():
    #slice_input = input()
    #json_input = input()
    
    #If you want to test with an example
    
    slice_input = 'slices/5b-loops-unfolding.py'
    json_input = 'slices/5b-loops-unfolding.patterns.json'
    
    tree, json_dict = build_ats_tree(slice_input)
    patterns = read_json(json_input)
    
    #for trace in get_traces(tree):
    #    print(trace)
    
    
    
def read_json(file_path):
    patterns = []
    
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    for item in data:
        pattern = Pattern(item['vulnerability'], item['sources'], item['sanitizers'], item['sinks'], item['implicit']) #missing implicit flow flag
        patterns.append(pattern)
        
    return patterns


    
if __name__ == "__main__":
    main()
    
    