"""
    pyexcel.sheets.presentation
    ~~~~~~~~~~~~~~~~~~~

    Provide readable string prestation

    :copyright: (c) 2014-2015 by C. W.
    :license: GPL v3
"""
"""External presentation plugin register"""
STRINGIFICATION = {}


def outsource(func):
    """Presentation injector"""
    def inner(self):
        plugin = STRINGIFICATION.get(str(self.__class__), None)
        if plugin:
            return plugin(self)
        else:
            return func(self)
    return inner
