import os
import sys

# Add the parent directory to the sys.path to allow relative imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.Label import Label
from src.MultiLabel import MultiLabel
from src.Pattern import Pattern
from src.Pattern import Pattern
from src.Vulnerabilities import Vulnerabilities



label1 = Label([("sourceX", {"SanA", "SanB"}), ("SourceY", {"SanH", "SanM"})])
label2 = Label([("SourceZ", {"SanC", "SanD"}), ("SourceE", {"SanW", "SanQ"})])

pattern1 = Pattern("pattern1", ["sourceX", "SourceY"], [], ["sink1", "sink4"])
pattern2 = Pattern("pattern2", ["SourceZ", "SourceE"], [], ["sink2", "sink3"])

multilabel = MultiLabel({"pattern1": (pattern1, label1), "pattern2": (pattern2, label2)})


vulnerabilities = Vulnerabilities()
vulnerabilities.report_vulnerability("sink1", multilabel)
vulnerabilities.report_vulnerability("sink3", multilabel)
vulnerabilities.report_vulnerability("sink2", multilabel)


print(vulnerabilities.get_all_vulnerabilities())

print(vulnerabilities.get_vulnerability("pattern1"))