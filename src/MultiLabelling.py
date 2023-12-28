class MultiLabelling():
    def __init__(self, multi_labels=None):
        if multi_labels is None:
            multi_labels = {}
        self.multi_labels = multi_labels # {"variable_name": multi_label}

    def add_multilabel(self, variable_name, multi_label):
        self.multi_labels[variable_name] = multi_label

    def get_multi_labels(self):
        # Returns the entire dictionary of multi-labels
        return self.multi_labels

    def get_multi_label(self, variable_name):
        # Returns the multi-label for a specific variable name
        return self.multi_labels.get(variable_name)

    def mutator(self, old_variable_name, new_variable_name):
        # Updates the multi-label variable (key) for a given variable name
        if old_variable_name in self.multi_labels.keys():
            self.multi_labels[new_variable_name] = self.multi_labels[old_variable_name]
            self.multi_labels.pop(old_variable_name)
        else:
            print(f"Variable name '{old_variable_name}' not found.")

    def deep_copy(self):
        result_dictionary = dict()
        for variable_name, multilabel in self.multi_labels.items():
            result_dictionary[variable_name] = multilabel.deep_copy()
        
        return MultiLabelling(result_dictionary)