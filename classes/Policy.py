class Policy:

    def __init__(self, patterns):
        self._patterns = set(patterns)

    def get_names(self):
        return list(filter(lambda x: x.is_name(), self._patterns))
    
    def get_sources(self):
        return list(filter(lambda x: x.is_sources(), self._patterns))

    def get_sanitizers(self):
        return list(filter(lambda x: x.is_sanitizers(), self._patterns))

    def get_sinks(self):
        return list(filter(lambda x: x.is_sinks(), self._patterns))

    def corresponding_illegal_flow(self, name, multilable):
        #Dependant on class MultiLable
