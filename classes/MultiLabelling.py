from Label import Label
from MultiLabel import MultiLabel

class MultiLabelling():
    def __init__(self, multi_labels):
        # This dictionary stores variable names as keys and their multi-labels as values
        self.multi_labels = multi_labels  # {"variable_name": multi_label}

    def get_multi_labels(self):
        # Returns the entire dictionary of multi-labels
        return self.multi_labels

    def get_multi_label(self, variable_name):
        # Returns the multi-label for a specific variable name
        return self.multi_labels.get(variable_name)

    def mutator(self, old_variable_name, new_variable_name):
        # Updates the multi-label varable (key) for a given variable name
        if old_variable_name in self.multi_labels.keys():
            self.multi_labels[new_variable_name] = self.multi_labels.pop(old_variable_name)
        else:
            print(f"Variable name '{old_variable_name}' not found.")


def main():
    label1 = Label([("sourceX", {"SanA", "SanB"}), ("SourceY", {"SanH", "SanM"})])
    label2 = Label([("SourceZ", {"SanC", "SanD"}), ("SourceE", {"SanW", "SanQ"})])

    multi_label = MultiLabel({"pattern1": label1, "pattern2": label2})
    multi_labelling = MultiLabelling({"var": multi_label})

    # Test get_multi_labels
    assert multi_label in multi_labelling.get_multi_labels().values()

    # Test get_multi_label
    assert multi_labelling.get_multi_label("var") == multi_label

    # Test mutator
    multi_labelling.mutator("var", "var2")
    assert list(multi_labelling.get_multi_labels().keys()) == ["var2"]

    print("All tests passed successfully.")

if __name__ == "__main__":
    main()