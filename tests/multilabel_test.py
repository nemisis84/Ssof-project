import os
import sys

# Add the parent directory to the sys.path to allow relative imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.Label import Label
from src.MultiLabel import MultiLabel
from src.MultiLabelling import MultiLabelling
from src.Pattern import Pattern

# Updated test for the new structure
label1 = Label([("sourceX", 1, [("SanA", 1), ("SanB", 2)]), ("SourceY", 2, [("SanH", 3), ("SanM", 4)])])
label2 = Label([("SourceZ", 5, [("SanC", 9), ("SanD", 10)]), ("SourceE", 6, [("SanW", 11), ("SanQ", 12)])])

pattern1 = Pattern("pattern1", ["sourceX", "SourceY"], [], [], "yes")
pattern2 = Pattern("pattern2", ["SourceZ", "SourceE"], [], [], "yes")

multilabel = MultiLabel({pattern1.get_name(): (pattern1, label1), pattern2.get_name(): (pattern2, label2)})

label = multilabel.get_label(pattern1)
assert label.get_source_names() == ['sourceX', 'SourceY']
assert label.get_sanitizers("sourceX") == {"SanA": 1, "SanB": 2}

label = multilabel.get_label(pattern2)
assert label.get_source_names() == ['SourceZ', 'SourceE']
assert label.get_sanitizers("SourceZ") == {"SanC": 9, "SanD": 10}

label3 = Label([("source5", 7, [("sanG", 13)])])
pattern3 = Pattern("pattern3", ["sanG"], [], [], "yes")

multilabel3 = MultiLabel({pattern3.get_name(): (pattern3, label3)})
multilabel_combi = multilabel.combine(multilabel3)

assert multilabel_combi.get_pattern_names() == ['pattern1', 'pattern2', 'pattern3']

# Test deepcopy
multilabel_orig = MultiLabel({pattern1.get_name(): (pattern1, label1)})
multilabel_deepcopy = multilabel_orig.deep_copy()
multilabel_orig.add_label(pattern2, label2)

assert len(multilabel_deepcopy.get_pattern_to_label_mapping().keys()) == 1
assert len(multilabel_orig.get_pattern_to_label_mapping().keys()) == 2
