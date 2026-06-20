"""
pyexcel.internal.garbagecollector
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Simple garbage collector

:copyright: (c) 2015-2025 by Onni Software Ltd.
:license: New BSD License
"""

from pyexcel import docstrings as docs
from pyexcel._compact import append_doc
from threading import local
from typing import Any, Iterator, List, cast


class _ThreadLocalGarbage:
    def __init__(self):
        self._storage = local()

    def _items(self) -> List[Any]:
        items = getattr(self._storage, "items", None)
        if items is None:
            items = []
            self._storage.items = items
        return cast(List[Any], items)

    def append(self, item: Any):
        self._items().append(item)

    def clear(self) -> None:
        self._items().clear()

    def drain(self) -> List[Any]:
        items = list(self._items())
        self._storage.items = []
        return items

    def __len__(self) -> int:
        return len(self._items())

    def __iter__(self) -> Iterator[Any]:
        return iter(self._items())


GARBAGE = _ThreadLocalGarbage()


def append(item: Any):
    """
    add garbage to the current thread's list of garbages
    """
    GARBAGE.append(item)


@append_doc(docs.FREE_RESOURCES)
def free_resources():
    """
    Close file handles opened by signature functions that starts with 'i'
    """
    resources = GARBAGE.drain()
    first_exception = None
    for item in resources:
        try:
            item.close()
        except Exception as exc:
            if first_exception is None:
                first_exception = exc
    if first_exception is not None:
        raise first_exception


def reset():
    """
    After everything has been closed, reset the array
    """
    GARBAGE.clear()
