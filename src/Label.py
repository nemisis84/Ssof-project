import copy

class Label:
    def __init__(self, sources: list):
        self._sources = sources # [(source, {san1: lineno_san1, san2: lineno_san2}, lineno_source), (source2, {san1: lineno_san1, san2: lineno_san2}, lineno_source2, ...]

    def add_source(self, source):
        if isinstance(source, tuple):
            self._sources.append(source)
        else:
            print("Source needs to be tuple: (source, {san1,san2}, lineno)")

    def add_sanitizer(self, source, sanitizer, sanitizer_key):
        for sor, san, lineno in self._sources:
            if sor == source:
                # print("aaaa :" + str(sanitizer))
                san[sanitizer_key] = sanitizer[sanitizer_key]
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
        for sor, san, lineno in self._sources:
            if sor == source:
                return san.copy()

    def combine(self, other_label):
        sources = self.get_sources() + other_label.get_sources()
        combined_label = Label(sources)
        return combined_label
    
    def deep_copy(self):
        result_sources = []
        for source, sanitizers, lineno in self._sources:
            
            result_sanitizers = copy.deepcopy(sanitizers)
            
            result_sources.append((source, result_sanitizers))
            #Might be wrong
            result_sources.append((result_sources, lineno))
        
        return Label(result_sources)