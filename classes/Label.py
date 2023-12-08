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

    def get_sanitizers(self, source):
        for sor, san in self._sources:
            if sor == source:
                return san.copy()

    def combine(self, other_label):
        sources = self.get_sources() + other_label.get_sources()
        combined_label = Label(sources)
        return combined_label

if __name__ == "__main__":
    label1 = Label([("sourceX", {"SanA", "SanB"}), ("SourceY", {"SanH", "SanM"})])
    label1.add_source(("source1", {"sanG"}))
    label1.add_source(("sourceF", {"sanT", "sanJ"})) # Try to add excisting source
    label1.add_sanitizer("sourceX", "sanitizer1")
    print("Sources in label1", label1.get_sources())
    print("Source names in label1", label1.get_source_names())
    print("Sanitizers in label1", label1.get_sanitizers("SourceX"))

    label2 = Label([("SourceZ", {"SanC", "SanD"}), ("SourceE", {"SanW", "SanQ"})])
    label2.add_source(("source5", {"sanG"}))
    
    combined_label = label1.combine(label2)
    print("Sources in combined label:", combined_label.get_sources())
    # Test adding new source to label1 to see if it appears in combined_label
    label1.add_source(("SpecialLABEL", {"SANNNNN"}))
    print("Sources in label1", label1.get_sources())
    print("Sources in combined label:", combined_label.get_sources())

