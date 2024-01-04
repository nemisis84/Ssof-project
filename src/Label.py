import copy

class Label:
    def __init__(self, sources: list):
        self.sources = sources # [(source, source_lineno, [[(san1, san1_lineno), (san2, san2_lineno)], [(san3, san3_lineno)]]), ...]

    def add_source(self, source):
        if isinstance(source, tuple):
            self.sources.append(source)
        else:
            print("Source needs to be tuple: (source, source_lineno, [(san1, san1_lineno), ...])")

    def get_sources(self):
        return self.sources

    def get_source_names(self):
        # Only grabs source_names
        return [source[0] for source in self.get_sources()]

    def get_linenos(self):
        return [source[1] for source in self.get_sources()]

    # add sanitizer to all existing flows for source
    def add_sanitizer(self, source, sanitizer, sanitizer_lineno):
        for (sor, _, sanitizer_flows) in self.sources:
            if sor == source:
                for sanitizer_flow in sanitizer_flows:
                    sanitizer_flow.append((sanitizer, sanitizer_lineno))
                return
        print("No matching source")

    # add sanitizer flow to specific source
    def add_sanitizer_flow_to_source(self, source, sanitizer_flow):
        for (sor, _, sanitizer_flows) in self.sources:
            if sor == source:
                sanitizer_flows.append(sanitizer_flow)
                return
        print("No matching source")

    def remove_empty_sanitizer_flows(self):
        for (_, _, sanitizer_flows) in self.sources:
            sanitizer_flows[:] = [flow for flow in sanitizer_flows if flow] # filter empty lists out

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