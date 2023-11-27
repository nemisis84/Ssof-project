from Pattern import Pattern
from Label import Label

class MultiLabel:
    def __init__(self, label):
        self._labels = label # {pattern_name: [label1, label2]}
    
    def get_labels(self, pattern_name):
        return self._labels[pattern_name]

    def get_patterns(self):
        return self._labels.keys()    

    def add_label(self, pattern_name, label):
        self._labels[pattern_name] = label

    def add_source_to_label(self, pattern, source):
        # Patterns is a list of the patterns available. 
        pattern_name = pattern.get_name()
        if pattern_name in self._labels and pattern.is_source(source):
            # If pattern is key in labels and had this source:
            self._labels[pattern_name].add_source(source)
            return True
        else: return False

    def add_sanitizer_to_label(self, pattern, sanitizer):
        # Patterns is a list of the patterns available.
        pattern_name = pattern.get_name()

        if pattern_name in self._labels and sanitizer in pattern.get_sanitizers():
            # If pattern is key in labels and had this source:
            self._labels[pattern_name].add_source(sanitizer)
            return True
        else: return False

if __name__ == "__main__":
    label1 = Label(("sourceX", "SourceY"), ("SanA", "SanB"))
    label2 = Label(("sourceA", "SourceZ"), ("SanC", "SanD"))

    pattern1 = Pattern(
    name="pattern1",
    sources=["sourceA", "sourceX"],
    sanitizers=["SanA", "SanD"],
    sinks=["some_sink"]
    )

    multi_label = MultiLabel({"pattern1":[label1], "pattern2":[label2]})
    print(multi_label.get_labels("pattern1"))
    print(multi_label.get_patterns())
    print(multi_label.add_sanitizer_to_label(pattern1, "SanD"))
    print(multi_label.add_sanitizer_to_label(pattern1, "sanV"))