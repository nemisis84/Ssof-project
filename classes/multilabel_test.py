from Label import Label
from MultiLabel import MultiLabel
from MultiLabelling import MultiLabelling
from Pattern import Pattern

label1 = Label([("sourceX", {"SanA", "SanB"}), ("SourceY", {"SanH", "SanM"})])
label2 = Label([("SourceZ", {"SanC", "SanD"}), ("SourceE", {"SanW", "SanQ"})])

pattern1 = Pattern("pattern1", ["sourceX", "SourceY"], [], [])
pattern2 = Pattern("pattern2", ["SourceZ", "SourceE"], [], [])

multi_label = MultiLabel({pattern1.get_name():(pattern1, label1), pattern2.get_name():(pattern2, label2)})

label  = multi_label.get_label(pattern1)
assert(label.get_source_names() == ['sourceX', 'SourceY'])
assert(label.get_sanitizers("sourceX") == {"SanA", "SanB"})

label = multi_label.get_label(pattern2)
assert(label.get_source_names() == ['SourceZ', 'SourceE'])
assert(label.get_sanitizers("SourceZ") == {"SanC", "SanD"})

label3 = Label([("source5", {"sanG"})])

pattern3 = Pattern("pattern3", ["sanG"], [], [])

multi_label3 = MultiLabel({pattern3.get_name():(pattern3, label3)})
multi_label_combi = multi_label.combine(multi_label3)

assert(multi_label_combi.get_pattern_names()) == ['pattern1', 'pattern2', 'pattern3']