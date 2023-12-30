import copy

class Label:
    def __init__(self, sources: list, position = None):
        self.sources = sources # [(source, source_lineno, [[san1, san1_lineno], [san2, san2_lineno]]), ...]
        self.position = position
        # print("aaaa aaaaaaaa: " + str(self.position))

    def add_source(self, source):
        if isinstance(source, tuple):
            self.sources.append(source)
        else:
            print("Source needs to be tuple: (source, source_lineno, [(san1, san1_lineno), ...])")

    def add_sanitizer(self, source, sanitizer, sanitizer_lineno):
        for (sor, _, sanitizers) in self.sources:
            if sor == source:
                sanitizers.append([[sanitizer, sanitizer_lineno]])
                return
        print("No matching source")
        
    def add_sanitizer_and_position(self, source, nested_sanitizers, position):
        for (sor, _, sanitizers) in self.sources:
            if sor == source:
                #Might only start at 1
                self.position = position
                sanitizers.append(nested_sanitizers)
                return
        print("No matching source")

    def get_sanitizer_and_position(self):
        return self.position
    
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
        if(self.position == other_label.get_position_number()):
            position = self.position
            
        combined_label = Label(sources, position=position)
        return combined_label

    def deep_copy(self):
        result_sources = []
        for source, lineno, sanitizers in self.sources:
            result_sanitizers = copy.deepcopy(sanitizers)
            result_sources.append((source, lineno, result_sanitizers))
        return Label(result_sources)