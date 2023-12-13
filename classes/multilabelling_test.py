from Label import Label
from MultiLabel import MultiLabel
from MultiLabelling import MultiLabelling
from Pattern import Pattern

label1 = Label([("sourceX", {"SanA", "SanB"}), ("SourceY", {"SanH", "SanM"})])
label2 = Label([("SourceZ", {"SanC", "SanD"}), ("SourceE", {"SanW", "SanQ"})])

multi_label = MultiLabel({"pattern1": label1, "pattern2": label2})
multi_labelling = MultiLabelling({"var": multi_label})

# Test get_multi_labels
assert multi_label in multi_labelling.get_multi_labels().values()

# Test get_multi_label
assert multi_labelling.get_multi_label("var") == multi_label

# Test mutator
multi_labelling.mutator("var", "var2")
assert list(multi_labelling.get_multi_labels().keys()) == ["var2"]

print("All tests passed successfully.")