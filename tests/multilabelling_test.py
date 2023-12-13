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

multilabel = MultiLabel({"pattern1": (pattern1, label1), "pattern2": (pattern2, label2)})
multilabelling = MultiLabelling({"var": multilabel})

# Test get_multilabels
assert multilabel in multilabelling.get_multi_labels().values()

# Test get_multilabel
assert multilabelling.get_multi_label("var") == multilabel

# Test mutator
multilabelling.mutator("var", "var2")
assert list(multilabelling.get_multi_labels().keys()) == ["var2"]

# Test deepcopy
multilabelling_deepcopy = multilabelling.deep_copy()

label3 = Label([("source5", {"sanG"})])
pattern3 = Pattern("pattern3", ["sanG"], [], [])
multilabel.add_label(pattern3, label3)

assert(multilabelling_deepcopy.get_multi_labels()["var2"].get_pattern_names() !=
      multilabelling.get_multi_labels()["var2"].get_pattern_names())