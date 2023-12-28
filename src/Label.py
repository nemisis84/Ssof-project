import copy

class Label:
    def __init__(self, sources: list):
        self.sources = sources # [(source, source_lineno, [(san1, san1_lineno), (san2, san2_lineno)]), ...]

    def add_source(self, source):
        if isinstance(source, tuple):
            self.sources.append(source)
        else:
            print("Source needs to be tuple: (source, source_lineno, [(san1, san1_lineno), ...])")

    def add_sanitizer(self, source, sanitizer, sanitizer_lineno):
        for (sor, _, sanitizers) in self.sources:
            if sor == source:
                sanitizers.append((sanitizer, sanitizer_lineno))
                return
        print("No matching source")

    def get_sources(self):
        return self.sources

    def get_source_names(self):
        # Only grabs source_names
        return [source[0] for source in self.get_sources()]

    def get_linenos(self):
        return [source[1] for source in self.get_sources()]

    def get_sanitizers(self, source):
        for sor, lineno, sanitizers in self.sources:
            if sor == source:
                return dict(sanitizers)

    def combine(self, other_label):
        sources = self.get_sources() + other_label.get_sources()
        combined_label = Label(sources)
        return combined_label

    def deep_copy(self):
        result_sources = []
        for source, lineno, sanitizers in self.sources:
            result_sanitizers = copy.deepcopy(sanitizers)
            result_sources.append((source, lineno, result_sanitizers))
        return Label(result_sources)