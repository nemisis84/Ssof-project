from Pattern import Pattern
from Label import Label
from MultiLabel import MultiLabel

class Policy:

    def __init__(self, patterns):
        self._patterns = patterns # [pattern1, pattern2, ...]

    def get_names(self):
        return list(filter(lambda x: x.is_name(), self._patterns))
    
    def get_sources(self):
        return list(filter(lambda x: x.is_sources(), self._patterns))

    def get_sanitizers(self):
        return list(filter(lambda x: x.is_sanitizers(), self._patterns))

    def get_sinks(self):
        return list(filter(lambda x: x.is_sinks(), self._patterns))

    def corresponding_illegal_flow(self, name, multilable):
        filtered_patterns = [element for element in multilable.get_patterns() if element in self._patterns]
        
        new_multilable_labels = None
        
        for pattern in filtered_patterns:
            if pattern.get_name() == name or pattern.get_sources() == name or \
                pattern.get_sanitizers() == name or pattern.get_sinks() == name:
                new_multilable_labels[pattern] = multilable.get_labels(pattern)
                
            

if __name__ == "__main__":
    label1 = Label(("sourceX", "SourceY"), ("SanA", "SanB"))
    label2 = Label(("sourceA", "SourceZ"), ("SanC", "SanD"))

    pattern1 = Pattern(
    name="pattern1",
    sources=["sourceA", "sourceX"],
    sanitizers=["SanA", "SanD"],
    sinks=["some_sink"]
    )
    
    pattern2 = Pattern(
    name="pattern2",
    sources=["sourceA", "sourceY"],
    sanitizers=["SanA", "SanE"],
    sinks=["other_sink"]
    )

    multi_label = MultiLabel({"pattern1":[label1], "pattern2":[label2]})
    
    policy = Policy([pattern1, pattern2])
    
    print(policy.get_names())
    print(policy.get_sources())
    print(policy.get_sanitizers())
    print(policy.get_sinks())
    print(policy.corresponding_illegal_flow("sourceA", multi_label))
    