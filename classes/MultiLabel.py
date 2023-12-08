from Pattern import Pattern
from Label import Label

class MultiLabel:
    def __init__(self, labels_dict = {}):
        self.pattern_to_labels_mapping = labels_dict # {pattern_name: label1}
    
    def get_pattern_to_labels_mapping(self):
        return self.pattern_to_labels_mapping

    def get_labels(self, pattern_name):
        return self.pattern_to_labels_mapping[pattern_name]

    def get_patterns(self):
        return self.pattern_to_labels_mapping.keys()   

    def add_label(self, pattern_name, label):
        if pattern_name in self.pattern_to_labels_mapping:
            print("Pattern already excist.")
        else:
            self.pattern_to_labels_mapping[pattern_name] = {label}

    def combine(self, other_multilabel):
        result = MultiLabel(self.get_pattern_to_labels_mapping())
        for pattern, label in other_multilabel.get_pattern_to_labels_mapping().items():
            result.add_label(pattern, label)
        
        # for pattern, labels in other_multilabel.pattern_to_labels_mapping.items():
        #     for label in labels:
        #         result.add_label(pattern, label)
        return result


if __name__ == "__main__":
    label1 = Label([("sourceX", {"SanA", "SanB"}), ("SourceY", {"SanH", "SanM"})])
    label2 = Label([("SourceZ", {"SanC", "SanD"}), ("SourceE", {"SanW", "SanQ"})])


    multi_label = MultiLabel({"pattern1":label1, "pattern2":label2})
    
    label  = multi_label.get_labels("pattern1")
    assert(label.get_source_names() == ['sourceX', 'SourceY'])
    assert(label.get_sanitizers("sourceX") == {"SanA", "SanB"})
    
    label = multi_label.get_labels("pattern2")
    assert(label.get_source_names() == ['SourceZ', 'SourceE'])
    assert(label.get_sanitizers("SourceZ") == {"SanC", "SanD"})

    
    label3 = Label([("source5", {"sanG"})])

    multi_label2 = MultiLabel({"pattern7":label3})
    multi_label_combi = multi_label.combine(multi_label2)

    assert(list(multi_label_combi.get_patterns()) == ['pattern1', 'pattern2', 'pattern7'])
    # assert that both labels are in combination
    # assert any(label.get_source_names() == ["sourceX", "SourceY"] in multi_label_combi.get_labels("pattern1").get_source_names())
    # assert any(label.get_source_names() == ["SourceZ", "SourceE"] for label in multi_label_combi.get_labels("pattern2"))
