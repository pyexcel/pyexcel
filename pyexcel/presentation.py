"""
    pyexcel.sheets.presentation
    ~~~~~~~~~~~~~~~~~~~

    Provide readable string prestation

    :copyright: (c) 2014-2015 by Onni Software Ltd.
    :license: New BSD License, see LICENSE for more details
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
