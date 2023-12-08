from Pattern import Pattern
from Label import Label

class MultiLabel:
    def __init__(self, labels_dict = {}):
        self.pattern_to_label_mapping = labels_dict # {pattern_name: (pattern, label)}
    
    def get_pattern_to_label_mapping(self):
        return self.pattern_to_label_mapping

    def get_label(self, pattern):
        return self.pattern_to_label_mapping[pattern.get_name()][1]

    def get_pattern_names(self):
        return list(self.pattern_to_label_mapping.keys())

    def add_label(self, pattern, label):
        if pattern.get_name() in self.pattern_to_label_mapping:
            print("Pattern already excist.")
        else:
            self.pattern_to_label_mapping[pattern.get_name()] = (pattern, label)

    def combine(self, other_multilabel):
        result = MultiLabel(self.get_pattern_to_label_mapping())
        for pattern_name, (pattern, label) in other_multilabel.get_pattern_to_label_mapping().items():
            result.add_label(pattern, label)
            
        return result


if __name__ == "__main__":
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