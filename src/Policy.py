import os
import sys

# Add the parent directory to the sys.path to allow relative imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.MultiLabel import MultiLabel

class Policy:

    def __init__(self, patterns):
        self._patterns = patterns # [pattern1, pattern2, ...]

    def get_pattern(self, pattern_name):
        for pattern in self._patterns:
            if pattern.get_name() == pattern_name:
                return pattern
        return None
    
    def get_patterns(self):
        return self._patterns

    def get_names(self):
        return list(map(lambda x: x.get_name(), self._patterns))

    def get_relevant_patterns(self, variable_name, type):
        if type == "source":
            return [pattern for pattern in self._patterns if pattern.contains_source(variable_name)]
        elif type == "sanitizer":
            return [pattern for pattern in self._patterns if pattern.contains_sanitizer(variable_name)]
        elif type == "sink":
            return [pattern for pattern in self._patterns if pattern.contains_sink(variable_name)]

    def get_names_with_source(self, source):
        return [pattern.get_name() for pattern in self._patterns if pattern.contains_source(source)]

    def get_names_with_sanitizer(self, sanitizer):
        return [pattern.get_name() for pattern in self._patterns if pattern.contains_sanitizer(sanitizer)]
    
    def get_names_with_sink(self, sink):
        return [pattern.get_name() for pattern in self._patterns if pattern.contains_sink(sink)]

    def corresponding_illegal_flow(self, name, multi_label):
        multi_label_illegal_flow = MultiLabel({})

        for (pattern, label) in multi_label.get_pattern_to_label_mapping().values():
            if pattern.contains_sink(name):
                # Pass name and multilabel into report_vulnerability
                # print(f"illegal flow add label for pattern {pattern.get_name()}")
                add_multi_label = MultiLabel({})
                add_multi_label.add_label(pattern, label)
                multi_label_illegal_flow = multi_label_illegal_flow.combine(add_multi_label)
        
        return multi_label_illegal_flow