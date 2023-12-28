import os
import sys

# Add the parent directory to the sys.path to allow relative imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.Label import Label
from src.MultiLabel import MultiLabel
from src.Pattern import Pattern
from src.Pattern import Pattern
from src.Vulnerabilities import Vulnerabilities

# Updated test for the new structure
label1 = Label([("sourceX", 1, [("SanA", 2), ("SanB", 3)]), ("SourceY", 4, [("SanH", 5), ("SanM", 6)])])
label2 = Label([("SourceZ", 7, [("SanC", 8), ("SanD", 9)]), ("SourceE", 10, [("SanW", 11), ("SanQ", 12)])])

pattern1 = Pattern("pattern1", ["sourceX", "SourceY"], [], ["sink1", "sink4"], "yes")
pattern2 = Pattern("pattern2", ["SourceZ", "SourceE"], [], ["sink2", "sink3"], "yes")

multilabel = MultiLabel({"pattern1": (pattern1, label1), "pattern2": (pattern2, label2)})

vulnerabilities = Vulnerabilities()
vulnerabilities.report_vulnerability("sink1", multilabel, 1)
vulnerabilities.report_vulnerability("sink3", multilabel, 1)
vulnerabilities.report_vulnerability("sink2", multilabel, 1)

print(vulnerabilities.get_all_vulnerabilities())
print(vulnerabilities.get_vulnerability("pattern1"))
