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
            if pattern_name in self.get_pattern_names():
                new_label = self.get_label(pattern).combine(label)
                result.pattern_to_label_mapping[pattern.get_name()] = (pattern, new_label)
            else:
                result.add_label(pattern, label)
        
        return result

    def deep_copy(self):
        result_mapping = dict()
        for pattern_name, (pattern, label) in self.pattern_to_label_mapping.items():
            result_mapping[pattern_name] = set((pattern.deep_copy(), label.deep_copy()))

        return MultiLabel(result_mapping)
