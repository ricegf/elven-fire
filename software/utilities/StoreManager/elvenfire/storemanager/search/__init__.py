from elvenfire.storemanager import StoreMgrError


class SearchError (StoreMgrError):
    pass


class _Criterion:

    """Abstract class: criterion by which to search available items.

    To Implement:
      __init__()  -- accepts initial settings;
                     no need to call Criterion.__init__()
      match(item) -- returns boolean indicating whether the item matches

    """

    def __init__(self):
        raise NotImplementedError()

    def match(self, item):
        """Return boolean indicating whether item matches this criterion."""
        raise NotImplementedError()

    def filter(self, itemlist):
        """Return only matching items out of itemlist."""
        return [i for i in itemlist if self.match(i)]

    def search(self, loc):
        """Return matching items from specified Town/Store."""
        return self.filter(loc.getitems())

