class SourceFactory:
    """
    The factory method to support multiple datasources in getters and savers
    """
    sources = {
        "input-read": [],
        "sheet-write": [],
        "book-write": [],
        "book-read": [],
        "sheet-read": []
    }

    @classmethod
    def register_sources(self, sources):
        for source in sources:
            for target in source.targets:
                for action in source.actions:
                    self.register_a_source(target, action, source)

    @classmethod
    def register_a_source(self, target, action, source):
        key = "%s-%s" % (target, action)
        self.sources[key].append(source)

    @classmethod
    def _get_generic_source(self, target, action, **keywords):
        key = "%s-%s" % (target, action)
        for source in self.sources[key]:
            if source.is_my_business(action, **keywords):
                s = source(**keywords)
                return s
        return None

    @classmethod
    def get_source(self, **keywords):
        source = self._get_generic_source(
            'input',
            'read',
            **keywords)
        if source is None:
            source = self._get_generic_source(
                'sheet',
                'read',
                **keywords)
        return source

    @classmethod
    def get_book_source(self, **keywords):
        source = self._get_generic_source(
            'input',
            'read',
            **keywords)
        if source is None:
            source = self._get_generic_source(
                'book',
                'read',
                **keywords)
        return source

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
