class AttributeDict(dict):
    # A dict that supports attribute access.
    def __getattr__(self, key):
        return self[key]

    def __setattr__(self, key, value):
        self[key] = value
