
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
    
    def is_source(self, name):
        return name in self._sources

    def is_sanitizer(self, name):
        return name in self._sanitizers

    def is_sink(self, name):
        return name in self._sinks

# Example usage
vulnerability_pattern = Pattern(
    name="SQL Injection",
    sources=["user_input", "file_read"],
    sanitizers=["sanitize_sql_query"],
    sinks=["execute_query"]
)


if __name__ == "__main__":
    vulnerability_pattern = Pattern(
        name="SQL Injection",
        sources=["user_input", "random_file"],
        sanitizers=["sanitize_something"],
        sinks=["some_sink"]
    )
    # Testing is_* functions
    print("Is 'user_input' a source?", vulnerability_pattern.is_source("user_input"))
    print("Is 'sanitize_sql_query' a sanitizer?", vulnerability_pattern.is_sanitizer("sanitize_sql_query"))
    print("Is 'my_sink' a sink?", vulnerability_pattern.is_sink("my_sink"))
    # Testing getter
    print(f"Get the sanitizers: {vulnerability_pattern.get_sanitizers()}")
    print(f"Get the sinks: {vulnerability_pattern.get_sinks()}")
    print(f"Get the name: {vulnerability_pattern.get_name()}")
    print(f"Get the sources: {vulnerability_pattern.get_sources()}")

