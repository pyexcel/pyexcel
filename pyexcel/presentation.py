"""
    pyexcel.sheets.presentation
    ~~~~~~~~~~~~~~~~~~~

    Provide readable string prestation

    :copyright: (c) 2014 by C. W.
    :license: GPL v3
"""
STRINGIFICATION = {}


def outsource(func):
    def inner(self):
        plugin = STRINGIFICATION.get(str(self.__class__), None)
        if plugin:
            return plugin(self)
        else:
            return func(self)
    return inner
