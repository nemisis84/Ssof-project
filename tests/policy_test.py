import os
import sys

# Add the parent directory to the sys.path to allow relative imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.Label import Label
from src.MultiLabel import MultiLabel
from src.Pattern import Pattern
from src.Policy import Policy

vulnerability_pattern1 = Pattern(
    name="SQL Injection",
    sources=["user_input", "random_file", "B"],
    sanitizers=["sanitize_something"],
    sinks=["some_sink"]
)
vulnerability_pattern2 = Pattern(
    name="A",
    sources=["B", "C"],
    sanitizers=["san"],
    sinks=["sink"]
)
policy1 = Policy([vulnerability_pattern1, vulnerability_pattern2])

assert(policy1.get_names() == ["SQL Injection", "A"])
assert(policy1.get_names_with_sink("some_sink") == ["SQL Injection"])
assert(policy1.get_names_with_sanitizer("san") == ["A"])
assert(policy1.get_names_with_source("B") == ["SQL Injection", "A"])

label1 = Label([("sourceX", {"SanA", "SanB"}), ("SourceY", {"SanH", "SanM"})])
label2 = Label([("SourceZ", {"SanC", "SanD"}), ("SourceE", {"SanW", "SanQ"})])

pattern1 = Pattern("pattern1", ["sourceX", "SourceY"], [], ["sink1"])
pattern2 = Pattern("pattern2", ["SourceZ", "SourceE"], [], ["sink2"])

multilabel = MultiLabel({pattern1.get_name():(pattern1, label1), pattern2.get_name():(pattern2,label2)})

multilabel_illegal = policy1.corresponding_illegal_flow("sink1", multilabel)

assert(list(multilabel_illegal.get_pattern_names()) == ["pattern1"])
assert(multilabel_illegal.get_label(pattern1).get_source_names() == ["sourceX", "SourceY"])