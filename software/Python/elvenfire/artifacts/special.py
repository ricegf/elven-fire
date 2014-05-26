import random

from elvenfire import bonus5, bonus25
from elvenfire.artifacts import ArtifactError, _Artifact
from elvenfire.abilities.charabilities import *


"""Greater Artifacts that are truly special.

SpecialArtifact -- wish rings and other mold-breaking artifacts
STBattery       -- strength batteries

"""


class SpecialArtifact (_Artifact):

    """A truly special artifact.

    Class Attributes:
      typelist -- possible artifact types

    New Attributes:
      self.type    -- from self.typelist; kept pure while self.name may be
                      updated with additional information
      self.ability -- (Self-Powered Ring / Cloak of Vision only) 
                      MentalAbility provided by artifact
      self.IQ      -- (Gem of Summoning only) effective IQ of artifact
      self.size    -- (Flying Carpet) number of hexes
                      (Charm) effect on each attribute roll

    """

    typelist = ['Wish Ring', 'Self-Powered Ring', 'Gem of Summoning', 
                'Belt of Fetching', 'Gem of Maintain Illusion',
                'Flying Carpet', 'Shapeshifter', 'Cloak of Vision',
                'Gem of True Seeing', 'Lens of Translation', 'Charm',
                'Unicorn Horn']

    def __init__(self, type=None, ability=None, IIQ=None, IQ=None, size=None):
        self.ability = ability
        self.IIQ = IIQ
        self.IQ = IQ
        self.size = size

        if type is None:
            if ability is not None:
                if ability.name != 'Vision':
                    type = 'Self-Powered Ring'
                else:
                    type = random.choice(('Self-Powered Ring',
                                          'Cloak of Vision'))
            elif IIQ is not None:
                type = random.choice(('Self-Powered Ring', 'Cloak of Vision'))
            elif IQ is not None:
                type = 'Gem of Summoning'
            elif size is not None:
                if size > 2:
                    type = 'Flying Carpet'
                else:
                    type = random.choice(('Flying Carpet', 'Charm'))

        _Artifact.__init__(self, type)

        if (self.ability is not None and self.type != 'Self-Powered Ring' and
                                         self.type != 'Cloak of Vision'):
            raise ArtifactError("Ability does not apply to %s!" % self.type)
        elif self.IIQ is not None and self.ability is None:
            raise ArtifactError("No IIQ necessary for %s!" % self.type)
        elif self.IQ is not None and self.type != 'Gem of Summoning':
            raise ArtifactError("No IQ necessary for %s!" % self.type)
        elif (self.size is not None and self.type != 'Flying Carpet' and
                                        self.type != 'Charm'):
            raise ArtifactError("No size necessary for %s!" % self.type)

    def _lookup(self):
        self.type = self.name

        if self.type == 'Wish Ring':
            self.value = 100000
                          #########!#########!#########!#########!#########!#########!#########!#########!
            self.desc = ('A wish will raise an attribute point of a character or pet by 1, specify the\n' +
                         ' result of one die roll (except joining the Council of Six), return a character\n' +
                         ' or animal to life (same day only), create a golem, or allow the character to\n' +
                         ' activate any ability (even one he does not know) as if his IQ was 20 or 8\n' +
                         ' higher, exactly one time. No other uses for a wish are known to exist.')

        elif self.type == 'Self-Powered Ring':
            if self.ability is None:
                self.ability = MentalAbilityWithOpposites(None, self.IIQ)
            elif not isinstance(self.ability, MentalAbility):
                raise ArtifactError("Invalid ability: %s" % self.ability)
            self.IIQ = self.ability.IIQ
            self.name += " of %s" % self.ability
            self.value = 25 * self.ability.AC
                          #########!#########!#########!#########!#########!#########!#########!#########!
            self.desc = ('This ring does not require any ST to maintain the associated mental ability\n' +
                         ' (thus, the ability can be left "on" permanently).')
            self.desc += "\n\n%s" % self.ability.description()

        elif self.type == 'Gem of Summoning':
            if self.IQ is None:
                self.IQ = bonus25()
                if self.IQ < 10:
                    self.IQ += 8
            elif not (isinstance(self.IQ, int) and 9 <= self.IQ <= 25):
                raise ArtifactError("Invalid IQ: %s" % self.IQ)
            self.name += " (IQ %s)" % self.IQ
            self.value = 10 * self.IQ**2
                          #########!#########!#########!#########!#########!#########!#########!#########!
            self.desc = ('A special form of a normal summoning gem makes this a reusable, self-powered\n' +
                         ' item. Holds its own IQ, which determines the power of the creature(s) it can\n' +
                         ' summon. The glowing gem is held in hand for one round to summon its\n' +
                         ' creature(s); the glow then fades until the gem is recharged (via Aid or a\n' +
                         ' service in town; required ST is the power of the creature(s) the gem can\n' +
                         ' summon divided by 5).')

        elif self.type == 'Belt of Fetching':
            self.value = 10000
                          #########!#########!#########!#########!#########!#########!#########!#########!
            self.desc = ('Telepathic, includes 20 slots. When the wearer thinks of a gem, scroll, potion,\n' +
                         ' or book that is currently on the character, that item will be presented for\n' +
                         ' use in the same turn.')
        elif self.type == 'Gem of Maintain Illusion':
            self.value = 10000
                          #########!#########!#########!#########!#########!#########!#########!#########!
            self.desc = ('Allows one illusion or image (created normally) to remain until disbelieved.\n' +
                         ' The illusion must remain within sight of its creator. The creator can see\n' +
                         ' through the eyes of the illusion or image at will.')

        elif self.type == 'Flying Carpet':
            if self.size is None:
                self.size = bonus25()
            elif not (isinstance(self.size, int) and 1 <= self.size <= 25):
                raise ArtifactError("Invalid size: %s" % self.size)
            self.name += ' (%s hexes)' % self.size
            self.desc = 'Carries a maximum of 50 kg per hex. MA=16/48'
            self.value = 2000 * self.size          # 2k each for hexes 1-7
            if self.size <= 7: return
            self.value += 1000 * (self.size - 7)   # 3k each for hexes 8-12
            if self.size <= 12: return
            self.value += 1000 * (self.size - 12)  # 4k each for hexes 13-16
            if self.size <= 16: return
            self.value += 1000 * (self.size - 16)  # 5k each for hexes 17-20
            if self.size <= 20: return
            self.value += 1000 * (self.size - 20)  # 6k each for hexes 21-25

        elif self.type == 'Shapeshifter':
            self.value = 2000
                          #########!#########!#########!#########!#########!#########!#########!#########!
            self.desc = ('Intricately carved agate figure worn around the neck. At start of action phase,\n' +
                         ' wearer may concentrate on any creature s/he has sufficient IQ to summon\n' +
                         ' (regardless of whether s/he has the Summon ability), and agate will morph into\n' +
                         ' the shape of that creature. Wearer will also shapeshift into that creature,\n' +
                         ' adopting all abilities and attributes thereof, except that the IQ and the\n' +
                         ' ST+DX total may not change. Wearer can return to original form at any instant,\n' +
                         ' or change to a different creature at the start of his action phase.')

        elif self.type == 'Cloak of Vision':
            if self.ability is None:
                self.ability = MentalAbility('Vision', self.IIQ)
            elif not (isinstance(self.ability, MentalAbility) and 
                      self.ability.name == 'Vision'):
                raise ArtifactError("Invalid Vision ability: %s" % 
                                    self.ability)
            self.name += " %s" % self.ability.IIQ
            self.value = 1000 * (1, 2, 5, 10, 25)[self.ability.IIQ-1]
                          #########!#########!#########!#########!#########!#########!#########!#########!
            self.desc = ('Permits wearer to create and permanently maintain the protections of the Vision\n' +
                         ' ability on himself.')
            self.desc += "\n\n%s" % self.ability.description()

        elif self.type == 'Gem of True Seeing':
            self.value = 20000
                          #########!#########!#########!#########!#########!#########!#########!#########!
            self.desc = ('Enables user to determine if a creature is real, called, cloned, an illusion,\n' +
                         ' or an image, and identifies all protective spells on a creature. Usually\n' +
                         ' mounted in a pendant for constant use.')

        elif self.type == 'Lens of Translation':
            self.value = 6000
                          #########!#########!#########!#########!#########!#########!#########!#########!
            self.desc = ('This amulet, when using an ability from a book, reduces the Dx penalty by 4\n' +
                         ' (so IIQ=1 or IIQ=2 abilities used from a book through a Lens of Translation\n' +
                         ' confer no Dx penalty). A book or scroll in any language may be read (but not\n' +
                         ' written) by this Lens.')

        elif self.type == 'Charm':
            if self.size is None:
                self.size = random.choice((1, 1, 2))
            elif not (isinstance(self.size, int) and 1 <= self.size <= 2):
                raise ArtifactError("Invalid charm size: %s" % self.size)
            self.name += " +%s" % self.size
            # 30k for +1, 100k for +2
            self.value = 30000 + 70000 * (self.size - 1)
                          #########!#########!#########!#########!#########!#########!#########!#########!
            self.desc = ("Amulet that changes every ability roll (e.g. 3vDx) attempted by character in\n" +
                         " the character's choice of direction.")

        elif self.type == 'Unicorn Horn':
            self.value = 6500
                          #########!#########!#########!#########!#########!#########!#########!#########!
            self.desc = ('Water drunk (by a living creature) from a unicorn horn removes the effects of\n' +
                         ' damage and poison instantly, whether from gas, contact, weapon, or a poisonous\n' +
                         ' creature.')

        else:
            raise ArtifactError('Unknown special artifact: %s' % self.type)


class STBattery (_Artifact):

    """Wearable gem that makes ST available for the use of mental abilities.

    New Attributes:
      self.charges -- number of ST points available for use

    """

    def __init__(self, charges=None):
        self.charges = charges
        _Artifact.__init__(self)

    def _randomize(self):
        if self.charges is None:
            self.charges = bonus25()
        elif not (isinstance(self.charges, int) and (1 <= self.charges <= 25)):
            raise ArtifactError('Invalid # of charges for ST battery: %s' %
                                self.charges)
        self.name = "ST Battery (%s charges)" % self.charges

    def _lookup(self):
                      #########!#########!#########!#########!#########!#########!#########!#########!
        self.desc = ('A special type of wearable gem that makes additional ST available for the use\n' +
                     ' of mental abilities.')
        # Value: 1k each for first 10 points; 2k each for next 10;
        # then 3k, 4k, 5k, 7k, and 10k each to a max of 25
        self.value = 1000 * min(10, self.charges)
        if self.charges > 10:
            self.value += 2000 * min(10, self.charges - 10)
        if self.charges > 20:
            self.value += 3000
        if self.charges > 21:
            self.value += 4000
        if self.charges > 22:
            self.value += 5000
        if self.charges > 23:
            self.value += 7000
        if self.charges > 24:
            self.value += 10000
        


    