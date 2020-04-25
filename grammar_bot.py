# The grammar robot's logic.

from string import punctuation


class GrammarBot:

    def __init__(self):

        # Pairs of words that the bot will suggest are swapped for each other.
        one_way_swaps = [('accept', 'except'),
                         ('accepts', 'excepts'),
                         ('affect', 'effect'),
                         ('affects', 'effects'),
                         ('allusion', 'illusion'),
                         ('allusions', 'illusions'),
                         ('ascent', 'assent'),
                         ('ascents', 'assents'),
                         ('breath', 'breathe'),
                         ('breaths', 'breathes'),
                         ('capital', 'capitol'),
                         ('cite', 'sight'),
                         ('cites', 'sights'),
                         ('compliment', 'complement'),
                         ('compliments', 'complements'),
                         ('conscience', 'conscious'),
                         ('council', 'counsel'),
                         ('councils', 'counsels'),
                         ('elicit', 'illicit'),
                         ('immanent', 'imminent'),
                         ('lead', 'led'),
                         ('lie', 'lay'),
                         ('lies', 'lays'),
                         ('lose', 'loose'),
                         ('loses', 'looses'),
                         ('passed', 'past'),
                         ('precede', 'proceed'),
                         ('precedes', 'proceeds'),
                         ('principal', 'principle'),
                         ('principals', 'principles'),
                         ('quote', 'quotation'),
                         ('quotes', 'quotations'),
                         ('reluctant', 'reticent'),
                         ('stationary', 'stationery'),
                         ('than', 'then'),
                         ('their', 'there'),
                         ('through', 'threw'),
                         ('too', 'two'),
                         ('vain', 'vein'),
                         ('who', 'whom')]

        # For each one way swap, work out its opposite. And make list of keywords to look for.
        self.two_way_swaps = []
        for (first, second) in one_way_swaps:
            self.two_way_swaps.append((first, second))
            self.two_way_swaps.append((second, first))

    def grammar_check(self, message: str) -> str:
        """Returns a suggested substitution if the parm message contains a grammatical error,
        otherwise returns and empty string."""

        # Turn the message into a list of words, all lower case, with all punctuation marks removed.
        for each_punctuation_mark in punctuation:
            message = message.replace(each_punctuation_mark, ' ')
        word_list = message.lower().split()

        # Skip tweets that have none of the key words in them. Some replies seem to have neither.
        # Also skip tweets that have more than 1 keyword in them. They might be discussing the grammar difficulty!
        keyword_count = 0
        suggestion = ''
        for (keyword, substitute) in self.two_way_swaps:
            if keyword in word_list:
                keyword_count += 1
                suggestion = substitute

        if keyword_count == 1:
            return suggestion
        else:
            return ''
