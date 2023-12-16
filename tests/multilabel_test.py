import os
import sys

# Add the parent directory to the sys.path to allow relative imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.Label import Label
from src.MultiLabel import MultiLabel
from src.MultiLabelling import MultiLabelling
from src.Pattern import Pattern

label1 = Label([("sourceX", {"SanA", "SanB"}), ("SourceY", {"SanH", "SanM"})])
label2 = Label([("SourceZ", {"SanC", "SanD"}), ("SourceE", {"SanW", "SanQ"})])

pattern1 = Pattern("pattern1", ["sourceX", "SourceY"], [], [])
pattern2 = Pattern("pattern2", ["SourceZ", "SourceE"], [], [])

multilabel = MultiLabel({pattern1.get_name():(pattern1, label1), pattern2.get_name():(pattern2, label2)})

label  = multilabel.get_label(pattern1)
assert(label.get_source_names() == ['sourceX', 'SourceY'])
assert(label.get_sanitizers("sourceX") == {"SanA", "SanB"})

label = multilabel.get_label(pattern2)
assert(label.get_source_names() == ['SourceZ', 'SourceE'])
assert(label.get_sanitizers("SourceZ") == {"SanC", "SanD"})

label3 = Label([("source5", {"sanG"})])
pattern3 = Pattern("pattern3", ["sanG"], [], [])

multilabel3 = MultiLabel({pattern3.get_name():(pattern3, label3)})
multilabel_combi = multilabel.combine(multilabel3)

assert(multilabel_combi.get_pattern_names()) == ['pattern1', 'pattern2', 'pattern3']


# test deepcopy
multilabel_orig = MultiLabel({pattern1.get_name():(pattern1, label1)})
multilabel_deepcopy = multilabel_orig.deep_copy()
multilabel_orig.add_label(pattern2, label2)

assert(len(multilabel_deepcopy.get_pattern_to_label_mapping().keys()) == 1)
assert(len(multilabel_orig.get_pattern_to_label_mapping().keys()) == 2)