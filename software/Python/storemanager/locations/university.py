from storemanager.locations import _Store
from elvenfire.abilities.charabilities import PhysicalOrMentalAbility

class Class:

    """Public class available for students.

    Attributes:
      ability        -- 
      tuition        -- 
      days_remaining -- 

    Class Attributes:
      classtimes     -- number of days for each IIQ

    """

    classtimes = (1, 2, 4, 8, 16)

    def __init__(self, ability=None):
        self.ability = ability
        if ability is None:
            self.ability = PhysicalOrMentalAbility()
        self.tuition = int(self.ability.AC / 10) * 2
        self.days_remaining = self.classtimes[self.ability.IIQ-1]

    def update(self):
        self.days_remaining -= 1
        return self.days_remaining <= 0

    def __str__(self):
        return str(self.ability)

    def readable(self):
        return "%-37s Tuition: $%6s" % (self, self.tuition)


class University (_Store):

    """University with classes available each weekday.

    Attributes:
      courses       -- array of 5 arrays; classes starting this week
      activecourses -- courses currently in progress (as of Friday)

    """

    def __init__(self, name, size, desc=None):
        self.activecourses = []

        # Determine name & description
        self.name = name
        if self.name is None:
            self.name = self.randomname()
        self.description = desc
        if self.description is None:
            self.description = self.defaultdesc()

        # Determine die rolls based on size
        if 'd' in str(size):
            num, die = size.split('d')
            if num == '':
                num = 1
            self.numdice, self.diesize = int(num), int(die)
        else:
            self.townsize = int(size)
            self.randomdice()

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
        return random.choice(('ELF University', 'Grand Hall'))

    def defaultdesc(self):
        """Return a default description."""
        return "Classes available the current week."

    def randomitem(self):
        """Return an appropriate random ability."""
        return Class()

    def randomdice(self):
        """Determine die rolls based on townsize."""
        self.numdice = self.townsize
        self.diesize = 4

    def purchase(self, item):
        pass

    def update(self):
        """Update"""
        self.courses = [[] for i in range(5)]
        for day in range(5):
            self._updateday(day)

    def _updateday(self, day):
        newsize = self._storesize()
        while newsize > len(self.activecourses):
            newcourse = self.randomitem()
            self.courses[day].append(newcourse)
            self.activecourses.append(newcourse)
        for course in self.activecourses:
            if course.update():
                self.activecourses.remove(course)


