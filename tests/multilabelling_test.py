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

multilabel = MultiLabel({"pattern1": (pattern1, label1), "pattern2": (pattern2, label2)})
multilabelling = MultiLabelling()
multilabelling.add_multilabel("var", multilabel)

# Test get_multilabels
assert multilabel in multilabelling.get_multi_labels().values()

# Test get_multilabel
assert multilabelling.get_multi_label("var") == multilabel

# Test mutator
multilabelling.mutator("var", "var2")
assert list(multilabelling.get_multi_labels().keys()) == ["var2"]

# Test deepcopy
multilabelling_deepcopy = multilabelling.deep_copy()

label3 = Label([("source5", 7, [("sanG", 13)])])
pattern3 = Pattern("pattern3", ["sanG"], [], [], "yes")
multilabel.add_label(pattern3, label3)

assert multilabelling_deepcopy.get_multi_labels()["var2"].get_pattern_names() != multilabelling.get_multi_labels()["var2"].get_pattern_names()
