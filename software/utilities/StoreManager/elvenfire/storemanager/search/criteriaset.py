
from elvenfire.storemanager.search import _Criterion


class ANDCriteriaSet (_Criterion):

    """Item matches if it matches ALL child criteria."""

    def __init__(self, criteria):
        self.criteria = criteria

    def addcriterion(self, criterion):
        self.criteria.append(criterion)

    def match(self, item):
        for criterion in self.criteria:
            if not criterion.match(item):
                return False
        return True

    def __str__(self):
        return 'AND Criteria Set'


class ORCriteriaSet (_Criterion):

    """Item matches if it matches ANY child criteria."""

    def __init__(self, criteria):
        self.criteria = criteria

    def addcriterion(self, criterion):
        self.criteria.append(criterion)

    def match(self, item):
        for criterion in self.criteria:
            if criterion.match(item):
                return True
        return False

    def __str__(self):
        return 'OR Criteria Set'


class NOTCriteriaSet (_Criterion):
    def __init__(self, criterion):
        self.criteria = [criterion,]
    def match(self, item):
        return not self.criteria[0].match(item)
    def __str__(self):
        return 'NOT'





