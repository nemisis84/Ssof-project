from MultiLabel import MultiLabel
from Label import Label

class Vulnerabilities():

    def __init__(self, vulnerabilities):
        self.vulnerabilities = vulnerabilities # {"vulnerability_name": multilabel}

    def add_vulnerability(self, name, multilabel):
        if name not in self.vulnerabilities:
            self.vulnerabilities[name] = multilabel
        else:
            print("Vulnerability already recorded.")
    
    def report_vulnerability(self, name):
        result = {}
        if name not in self.vulnerabilities:
            return result
        result["vulnerability"] = name
        result["source"] = []
        result["sink"] = []
        result["unsanitized_flows"] = "Undecided"
        result["sanitized_flows"] = []

        
        for pattern, label in self.vulnerabilities[name].get_pattern_to_labels_mapping().items():
            result["source"].extend(label.get_source_names())
            # for source in label.get_source_names():
            #     print(label.get_source_names())
            #     result["sanitized_flows"].extend(list(label.get_sanitizers(source)))
        
        return result

if __name__ == "__main__":
    label1 = Label([("sourceX", {"SanA", "SanB"}), ("SourceY", {"SanH", "SanM"})])
    label2 = Label([("SourceZ", {"SanC", "SanD"}), ("SourceE", {"SanW", "SanQ"})])
    multi_label1 = MultiLabel({"pattern1":label1, "pattern2":label2})

    label3 = Label([("source5", {"sanG"})])
    multi_label2 = MultiLabel({"pattern7":label3})

    vulnerabilities = Vulnerabilities({"vulA": multi_label1})
    vulnerabilities.add_vulnerability("VulB", multi_label2)

    report = vulnerabilities.report_vulnerability("vulA")
    print(report)