import os
import sys

# Add the parent directory to the sys.path to allow relative imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.Label import Label
from src.MultiLabel import MultiLabel
from src.MultiLabelling import MultiLabelling
from src.Pattern import Pattern

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

vulnerability_pattern_deepcopy = vulnerability_pattern.deep_copy()

assert(vulnerability_pattern_deepcopy.get_name() == vulnerability_pattern.get_name())
assert(vulnerability_pattern_deepcopy.get_sources() == vulnerability_pattern.get_sources())
assert(vulnerability_pattern_deepcopy.get_sanitizers() == vulnerability_pattern.get_sanitizers())
assert(vulnerability_pattern_deepcopy.get_sinks() == vulnerability_pattern.get_sinks())