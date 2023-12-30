import copy

class Label:
    def __init__(self, sources: list, sanitized_flow = None):
        self.sources = sources # [(source, source_lineno, [[san1, san1_lineno], [san2, san2_lineno]]), ...]
        self.sanitized_flow = sanitized_flow
        # print("aaaa aaaaaaaa: " + str(self.sanitized_flow))

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
        
    def add_sanitized_flow(self, source, nested_sanitizers, sanitized_flow):
        for (sor, _, sanitizers) in self.sources:
            if sor == source:
                #Might only start at 1
                self.sanitized_flow = sanitized_flow
                sanitizers.append(nested_sanitizers)
                return
        print("No matching source")

    def get_sanitized_flow_number(self):
        return self.sanitized_flow
    
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
        if(self.sanitized_flow == other_label.get_sanitized_flow_number()):
            sanitized_flow = self.sanitized_flow
            
        combined_label = Label(sources, sanitized_flow=sanitized_flow)
        return combined_label

    def deep_copy(self):
        result_sources = []
        for source, lineno, sanitizers in self.sources:
            result_sanitizers = copy.deepcopy(sanitizers)
            result_sources.append((source, lineno, result_sanitizers))
        return Label(result_sources)