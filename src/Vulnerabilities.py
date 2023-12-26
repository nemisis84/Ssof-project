class Vulnerabilities():

    def __init__(self):
        self.vulnerabilities = [] # [{"vulnerability": "A_1", "source": ["b", 1], "sink": ["e", 2], "unsanitized_flows": "no", "sanitized_flows": [[["f", 2]]]}, {"vulnerability": "A_2", "source": ["b", 1], "sink": ["c", 2], "unsanitized_flows": "yes", "sanitized_flows": [[["f", 2]]]}, {"vulnerability": "A_3", "source": ["b", 1], "sink": ["e", 3], "unsanitized_flows": "yes", "sanitized_flows": [[["f", 2]]]}, {"vulnerability": "B_1", "source": ["b", 1], "sink": ["c", 2], "unsanitized_flows": "no", "sanitized_flows": [[["e", 2], ["d", 2]], [["d", 2]]]}]

    def get_vulnerability(self, vulnerability_name):
        for vul_dict in self.vulnerabilities:
            if vulnerability_name == vul_dict["vulnerability"][:-2]:
                return vul_dict
        return None

    def get_all_vulnerabilities(self):
        return self.vulnerabilities
    
    def name_helper(self, pattern_name):
        
        if len(self.get_all_vulnerabilities()) == 0:
            return pattern_name + "_1"
        
        counter = 1

        for vulnerability in self.vulnerabilities:
            if vulnerability["vulnerability"][:-2] == pattern_name:
                counter += 1

        return pattern_name + "_" + str(counter)

    def report_vulnerability(self, sink, multilabel, sink_lineno):
        
        

        for (pattern, label) in multilabel.get_pattern_to_label_mapping().values():
            
            if sink in pattern.get_sinks():
                sources = label.get_sources()

                for source, sanitizers, lineno in sources:
                    vulnerability = {}
                    vulnerability["vulnerability"] = self.name_helper(pattern.get_name())
                    vulnerability["source"] = (source, lineno)
                    vulnerability["sink"] = (sink, sink_lineno)
                    vulnerability["sanitized_flows"] = sanitizers.copy()
                    if not vulnerability["sanitized_flows"]:
                        vulnerability["unsanitized_flows"] = "Yes"
                    else:
                        # TODO: Find out how to decide this
                        vulnerability["unsanitized_flows"] = "No"
                    
                    vulnerability_reported = False
                    for vul in self.get_all_vulnerabilities():
                        if vul["source"] == vulnerability["source"] and vul["sink"] == vulnerability["sink"]:
                            vulnerability_reported = True
                    
                    if not vulnerability_reported:
                        self.vulnerabilities.append(vulnerability)
                        print(f"Report vulnerability with sink: {sink} and source: {source}")

if __name__ == "__main__":
    from Label import Label
    from MultiLabel import MultiLabel
    from Pattern import Pattern
    label1 = Label([("sourceX", {"SanA", "SanB"}), ("SourceY", {"SanH", "SanM"})])
    label2 = Label([("SourceZ", {"SanC", "SanD"}), ("SourceE", {"SanW", "SanQ"})])

    pattern1 = Pattern("pattern1", ["sourceX", "SourceY"], [], ["sink1", "sink4"])
    pattern2 = Pattern("pattern2", ["SourceZ", "SourceE"], [], ["sink2", "sink3"])

    multilabel = MultiLabel({"pattern1": (pattern1, label1), "pattern2": (pattern2, label2)})


    vulnerabilities = Vulnerabilities()
    vulnerabilities.report_vulnerability("sink1", multilabel)
    vulnerabilities.report_vulnerability("sink3", multilabel)
    # vulnerabilities.report_vulnerability("sink2", multilabel)
    

    print(vulnerabilities.get_all_vulnerabilities())