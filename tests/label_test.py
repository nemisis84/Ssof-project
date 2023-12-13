import os
import sys

# Add the parent directory to the sys.path to allow relative imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.Label import Label
from src.MultiLabel import MultiLabel
from src.MultiLabelling import MultiLabelling
from src.Pattern import Pattern

label1 = Label([("sourceX", {"SanA", "SanB"}), ("SourceY", {"SanH", "SanM"})])
label1.add_source(("source1", {"sanG"}))
label1.add_source(("sourceF", {"sanT", "sanJ"})) # Try to add excisting source
label1.add_sanitizer("sourceX", "sanitizer1")
print("Sources in label1", label1.get_sources())
print("Source names in label1", label1.get_source_names())
print("Sanitizers in label1", label1.get_sanitizers("SourceX"))

label2 = Label([("SourceZ", {"SanC", "SanD"}), ("SourceE", {"SanW", "SanQ"})])
label2.add_source(("source5", {"sanG"}))

combined_label = label1.combine(label2)
print("Sources in combined label:", combined_label.get_sources())
# Test adding new source to label1 to see if it appears in combined_label
label1.add_source(("SpecialLABEL", {"SANNNNN"}))
print("Sources in label1", label1.get_sources())
print("Sources in combined label:", combined_label.get_sources())