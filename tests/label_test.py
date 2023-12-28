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
label1.add_source(("source1", 3, [("sanG", 5)]))
label1.add_source(("sourceF", 4, [("sanT", 6), ("sanJ", 7)]))  # Try to add existing source
label1.add_sanitizer("sourceX", "sanitizer1", 8)
print("Sources in label1", label1.get_sources())
print("Source names in label1", label1.get_source_names())
print("Sanitizers in label1", label1.get_sanitizers("sourceX"))

label2 = Label([("SourceZ", 5, [("SanC", 9), ("SanD", 10)]), ("SourceE", 6, [("SanW", 11), ("SanQ", 12)])])
label2.add_source(("source5", 7, [("sanG", 13)]))

combined_label = label1.combine(label2)
print("Sources in combined label:", combined_label.get_sources())

label1_deepcopy = label1.deep_copy()

# Test adding a new source to label1 to see if it appears in combined_label
label1.add_source(("SpecialLABEL", 8, [("SANNNNN", 14)]))
print("Sources in label1", label1.get_sources())
print("Sources in combined label:", combined_label.get_sources())

print("Sources in deepcopy of label1", label1_deepcopy.get_sources())
