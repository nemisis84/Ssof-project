from Pattern import Pattern
from Label import Label

class MultiLabel:
    def __init__(self, labels_dict = {}):
        self._labels = labels_dict # {pattern_name: {label1, label2}}
    
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
    label1 = Label({"sourceA", "sourceB"}, {"san1", "san2"})
    label2 = Label({"sourceC"}, {"san3"})

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
        assert(label.get_sources() == {"sourceA", "sourceB"})
        assert(label.get_sanitizers() == {"san1", "san2"})
    
    assert(len(multi_label.get_labels("pattern2")) == 1)
    for label in multi_label.get_labels("pattern2"):
        assert(label.get_sources() == {"sourceC"})
        assert(label.get_sanitizers() == {"san3"})

    
    label3 = Label({"sourceZ"}, {"san26"})

    multi_label2 = MultiLabel({"pattern1":{label3}})
    multi_label_combi = multi_label.combine(multi_label2)

    # assert that both labels are in combination
    assert any(label.get_sources() == {"sourceA", "sourceB"} for label in multi_label_combi.get_labels("pattern1"))
    assert any(label.get_sources() == {"sourceZ"} for label in multi_label_combi.get_labels("pattern1"))
