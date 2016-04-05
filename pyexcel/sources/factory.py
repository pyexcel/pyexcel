class SourceFactory:
    """
    The factory method to support multiple datasources in getters and savers
    """
    sources = {
        "sheet": {
            "read": [],
            "write": []
        },
        "book":{
            "read": [],
            "write": []
        }
    }

    @classmethod
    def register_a_source(self, target, action, source):
        self.sources[target][action].append(source)

    @classmethod
    def _get_generic_source(self, target, action, **keywords):
        for source in self.sources[target][action]:
            if source.is_my_business(action, **keywords):
                s = source(**keywords)
                return s
        return None

    @classmethod
    def get_source(self, **keywords):
        return self._get_generic_source(
            'sheet',
            'read',
            **keywords)

    @classmethod
    def get_book_source(self, **keywords):
        return self._get_generic_source(
            'book',
            'read',
            **keywords)

    @classmethod
    def get_writeable_source(self, **keywords):
        return self._get_generic_source(
            'sheet',
            'write',
            **keywords)

    @classmethod
    def get_writeable_book_source(self, **keywords):
        return self._get_generic_source(
            'book',
            'write',
            **keywords)
