
class Pattern:
    def __init__(self, name, sources, sanitizers, sinks):
        self._name = name
        self._sources = sources
        self._sanitizers = sanitizers
        self._sinks = sinks
    
    def get_name(self):
        return self._name

    def get_sources(self):
        return self._sources

    def get_sanitizers(self):
        return self._sanitizers

    def get_sinks(self):
        return self._sinks
    
    def contains_source(self, name):
        return name in self._sources

    def contains_sanitizer(self, name):
        return name in self._sanitizers

    def contains_sink(self, name):
        return name in self._sinks
    
    def deep_copy(self):
        return Pattern(
            self.get_name(),
            self.get_sources(),
            self.get_sanitizers(),
            self.get_sinks()
        )

# Example usage
vulnerability_pattern = Pattern(
    name="SQL Injection",
    sources=["user_input", "file_read"],
    sanitizers=["sanitize_sql_query"],
    sinks=["execute_query"]
)


