from Label import Label
from MultiLabel import MultiLabel
from MultiLabelling import MultiLabelling
from Pattern import Pattern
vulnerability_pattern = Pattern(
    name="SQL Injection",
    sources=["user_input", "random_file"],
    sanitizers=["sanitize_something"],
    sinks=["some_sink"]
)
# Testing contains_* functions
print("Is 'user_input' a source?", vulnerability_pattern.contains_source("user_input"))
print("Is 'sanitize_sql_query' a sanitizer?", vulnerability_pattern.contains_sanitizer("sanitize_sql_query"))
print("Is 'my_sink' a sink?", vulnerability_pattern.contains_sink("my_sink"))
# Testing getter
print(f"Get the sanitizers: {vulnerability_pattern.get_sanitizers()}")
print(f"Get the sinks: {vulnerability_pattern.get_sinks()}")
print(f"Get the name: {vulnerability_pattern.get_name()}")
print(f"Get the sources: {vulnerability_pattern.get_sources()}")