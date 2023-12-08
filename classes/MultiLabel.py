from Pattern import Pattern
from Label import Label

class MultiLabel:
    def __init__(self, labels_dict = {}):
        self._labels = labels_dict # {pattern_name: {label1}}
    
    def get_labels(self, pattern_name):
        return self._labels[pattern_name]

    def get_patterns(self):
        return self._labels.keys()   

    def add_label(self, pattern_name, label):
        if pattern_name in self._labels:
            self._labels[pattern_name].add(label)
        else:
            self._labels[pattern_name] = {label}

    def combine(self, other_multilabel):
        result = MultiLabel(self._labels)
        for pattern, labels in other_multilabel._labels.items():
            for label in labels:
                result.add_label(pattern, label)
        return result


if __name__ == "__main__":
    label1 = Label([("sourceX", {"SanA", "SanB"}), ("SourceY", {"SanH", "SanM"})])
    label2 = Label([("SourceZ", {"SanC", "SanD"}), ("SourceE", {"SanW", "SanQ"})])


    pattern1 = Pattern(
        name="pattern1",
        sources=["sourceA", "sourceB", "sourceZ"],
        sanitizers=["san1", "san2", "san26"],
        sinks=["some_sink"]
    )

    pattern2 = Pattern(
        name="pattern2",
        sources=["sourceC", "sourceD"],
        sanitizers=["san3", "san4"],
        sinks=["some_other_sink"]
    )

    multi_label = MultiLabel({"pattern1":{label1}, "pattern2":{label2}})
    
    assert(len(multi_label.get_labels("pattern2")) == 1)
    for label in multi_label.get_labels("pattern1"):
        assert(label.get_source_names() == ['sourceX', 'SourceY'])
        assert(label.get_sanitizers("sourceX") == {"SanA", "SanB"})
    
    assert(len(multi_label.get_labels("pattern2")) == 1)
    for label in multi_label.get_labels("pattern2"):
        assert(label.get_source_names() == ['SourceZ', 'SourceE'])
        assert(label.get_sanitizers("SourceZ") == {"SanC", "SanD"})

    
    label3 = Label([("source5", {"sanG"})])

    multi_label2 = MultiLabel({"pattern1":{label3}})
    multi_label_combi = multi_label.combine(multi_label2)

    # assert that both labels are in combination
    assert any(label.get_source_names() == ["sourceX", "SourceY"] for label in multi_label_combi.get_labels("pattern1"))
    assert any(label.get_source_names() == ["SourceZ", "SourceE"] for label in multi_label_combi.get_labels("pattern2"))
