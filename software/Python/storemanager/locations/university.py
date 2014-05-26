import random

from elvenfire.abilities.charabilities import UniversityAbility
from storemanager.stockitems import _StockItem
from storemanager.locations import _Store

class Class (_StockItem):

    """Public class available for students.

    Attributes:
      first_day      -- weekday that class begins
      ability        -- the Ability being taught
      value          -- tuition cost to enroll
      days_remaining -- class days remaining

    Class Attributes:
      enum(Monday, Tuesday, Wednesday, Thursday, Friday, AllDays)
      Days           -- tuple of strings for above enum
      classtimes     -- number of days for each IIQ
      
    """

    classtimes = (1, 2, 4, 8, 16)
    Monday, Tuesday, Wednesday, Thursday, Friday, AllDays = 0, 1, 2, 3, 4, 5
    Days = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "every day")

    def __init__(self, day=AllDays, ability=None):
        self.first_day = day
        self.ability = ability
        if ability is None:
            self.ability = UniversityAbility()
        self.name = str(self.ability) + " Class"
        self.value = int(self.ability.AC / 10) * 2
        self.days_remaining = self.classtimes[self.ability.IIQ-1]
        self.desc = "Learn %s in %s days for only $%s!" % (self.ability,
                                                           self.days_remaining,
                                                           self.value)
        self.markup = 100

    def update(self):
        """Mark a day passed, and return True if the course is complete."""
        self.days_remaining -= 1
        return self.days_remaining <= 0

    def __str__(self):
        return "%s: $%s" % (self.name, self.price())

    def readable(self):
        return "%-37s (starts %s) Tuition: $%6s" % (self.name,
                                                    Class.Days[self.first_day],
                                                    self.price())

    def short(self):
        return str(self.ability)

    def description(self):
        return "%s course beginning %s for $%s" % (self.ability,
                                                   Class.Days[self.first_day],
                                                   self.price())
    
    def __lt__(self, other):
        """Sort by day, then (reverse) tuition."""
        if self.first_day == other.first_day:
            return self.price() > other.price()
        return self.first_day < other.first_day

    def reduce_markup(self):
        """University classes are not marked up."""
        pass


class University (_Store):

    """University with classes available each weekday.

    Attributes:
      courses       -- array of 5 arrays; classes starting this week
      activecourses -- courses currently in progress (as of Friday)

    Note that many of the attributes inherited from _Store do not apply
    (e.g. healingpotion, healingmarkup). Additionally, the inventory
    attribute is ignored in favor of the multi-layer courses.

    """

    def __init__(self, name, size, desc=None):
        """Extend _Store.__init__ to initialize course lists."""
        _Store.__init__(self, name, size, desc)
        self.activecourses = []
        self.update()

    def __str__(self):
        numcourses = sum([len(i) for i in self.courses])
        s = 's' if numcourses > 1 else ''
        return '%s (%s course%s)' % (self.name, numcourses, s)

    def readable(self):
        """Return university catalog, in human-readable format."""
        numcourses = sum([len(i) for i in self.courses])
        val = "\n\n********************************************************\n"
        val += ' %s (%s courses)\n' % (self.name, numcourses)
        val += '********************************************************\n\n'
        for day in range(5):
            val += '\n%s:\n' % ['Monday', 'Tuesday', 'Wednesday',
                                'Thursday', 'Friday'][day]
            for course in self.courses[day]:
                val += '  ' + course.readable() + '\n'
        return val

    def randomname(self):
        """Return a random name."""
        return random.choice(('ELF University', 'Grand Hall', 'Lessons R Us',
                              'Learn With Us', 'Tutors for Rent', 'PCU',
                              'ELF U', 'We School U', 'Four Elements University',
                              'Brain of Brawn', 'The How-Not-To-Die College'))

    def defaultdesc(self):
        """Return a default description."""
        return "Classes available the current week."

    def randomdice(self):
        """Determine die rolls based on townsize."""
        self.numdice = self.townsize
        self.diesize = 4

    def randomitem(self, day=Class.AllDays):
        """Return an appropriate random ability."""
        return Class(day)

    def getitems(self, day=Class.AllDays):
        """Return list of this week's classes."""
        if day == Class.AllDays:
            return self.courses[0] + self.courses[1] + self.courses[2] + self.courses[3] + self.courses[4]
        elif day == Class.Monday:
            return self.courses[0]
        elif day == Class.Tuesday:
            return self.courses[1]
        elif day == Class.Wednesday:
            return self.courses[2]
        elif day == Class.Thursday:
            return self.courses[3]
        elif day == Class.Friday:
            return self.courses[4]

    def purchase(self, item):
        """Courses are not removed on enrollment."""
        pass

    def additem(self, item):
        """Courses cannot be added manually."""
        pass

    def update(self):
        """Generate a new week's classes."""
        self.courses = [[] for i in range(5)]
        for day in range(5):
            self._updateday(day)
        return []

    def _updateday(self, day):
        """Generate a single day of classes."""
        newsize = self._storesize()
        while newsize > len(self.activecourses):
            newcourse = self.randomitem(day)
            self.courses[day].append(newcourse)
            self.activecourses.append(newcourse)
        for course in self.activecourses:
            if course.update():
                self.activecourses.remove(course)


