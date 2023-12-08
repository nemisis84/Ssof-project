from Pattern import Pattern
from Label import Label
from MultiLabel import MultiLabel

class Policy:

    def __init__(self, patterns):
        self._patterns = patterns # [pattern1, pattern2, ...]

    def get_names(self):
        return list(map(lambda x: x.get_name(), self._patterns))

    def get_names_with_source(self, source):
        return [pattern.get_name() for pattern in self._patterns if pattern.contains_source(source)]

    def get_names_with_sanitizer(self, sanitizer):
        return [pattern.get_name() for pattern in self._patterns if pattern.contains_sanitizer(sanitizer)]
    
    def get_names_with_sink(self, sink):
        return [pattern.get_name() for pattern in self._patterns if pattern.contains_sink(sink)]

    def corresponding_illegal_flow(self, name, multilablel):
        multi_label = MultiLabel({})
        for pattern, label in multilablel.get_pattern_to_labels_mapping().items():
            if name in label.get_source_names():
                print(name + " found in label")
                multi_label.add_label(pattern, label)
            for source in label.get_source_names():
                if name in label.get_sanitizers(source):
                    print(name + " found in label")
                    multi_label.add_label(pattern, label)
        return multi_label



if __name__ == "__main__":
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

    multi_label = MultiLabel({"pattern1":label1, "pattern2":label2})
    vul_multilabel = policy1.corresponding_illegal_flow("SanA", multi_label)

    assert(list(vul_multilabel.get_patterns()) == ["pattern1"])
    assert(list(vul_multilabel.get_label("pattern1"))[0].get_source_names() == ["sourceX", "SourceY"])