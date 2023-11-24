class Label:
    def __init__(self, sources, sanitizers):
        self._sources = set(sources)
        self._sanitizers = set(sanitizers)

    def add_source(self, source):
        self._sources.add(source)

    def add_sanitizer(self, sanitizer):
        self._sanitizers.add(sanitizer)

    def get_sources(self):
        return self._sources.copy()

    def get_sanitizers(self):
        return self._sanitizers.copy()

    def combine(self, other_label):
        sources = self._sources.union(other_label.get_sources())
        sanitizers = self._sanitizers.union(other_label.get_sanitizers())
        combined_label = Label(sources, sanitizers)
        return combined_label

if __name__ == "__main__":
    label1 = Label(("sourceX", "SourceY"), ("SanA", "SanB"))
    label1.add_source("source1")
    label1.add_source("sourceX") # Try to add excisting source
    label1.add_sanitizer("sanitizer1")
    print("Sources in label1", label1.get_sources())
    print("Sanitizers in label1", label1.get_sanitizers())

    label2 = Label(("sourceA", "SourceZ"), ("SanC", "SanD"))
    label2.add_source("source2")
    
    combined_label = label1.combine(label2)
    print("Sources in combined label:", combined_label.get_sources())
    print("Sanitizers in combined label:", combined_label.get_sanitizers())
    # Test adding new source to label1 to see if it appears in combined_label
    label1.add_source("SpecialLABEL")
    print("Sources in label1", label1.get_sources())
    print("Sources in combined label:", combined_label.get_sources())

