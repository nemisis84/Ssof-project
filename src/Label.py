class Label:
    def __init__(self, sources: list):
        self._sources = sources # [(source, {san1, san2}), (source2, {san1, san2}), ...]

    def add_source(self, source):
        if isinstance(source, tuple):
            self._sources.append(source)
        else:
            print("Source needs to be tuple: (source, {san1,san2})")

    def add_sanitizer(self, source, sanitizer):
        for sor, san in self._sources:
            if sor == source:
                san.add(sanitizer)
                return
        print("No matching source")

    def get_sources(self):
        return self._sources

    def get_source_names(self):
        # Only grabs source_names
        return list(map(lambda x: x[0], self.get_sources()))
    
    def get_linenos(self):
        return list(map(lambda x: x[2], self.get_sources()))

    def get_sanitizers(self, source):
        for sor, san in self._sources:
            if sor == source:
                return san.copy()

    def combine(self, other_label):
        sources = self.get_sources() + other_label.get_sources()
        combined_label = Label(sources)
        return combined_label
    
    def deep_copy(self):
        result_sources = []
        for source, sanitizers, lineno in self._sources:
            result_sanitizers = set()
            for sanitizer in sanitizers:
                result_sanitizers.add(sanitizer)
            
            result_sources.append((source, result_sanitizers))
            #Might be wrong
            result_sources.append((result_sources, lineno))
        
        return Label(result_sources)