import os
import sys

# Add the parent directory to the sys.path to allow relative imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.MultiLabel import MultiLabel

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
        multi_label_illegal_flow = MultiLabel({})

        for pattern_name, (pattern, label) in multilablel.get_pattern_to_label_mapping().items():
            if pattern.contains_sink(name):
                multi_label_illegal_flow.add_label(pattern, label)
        
        return multi_label_illegal_flow