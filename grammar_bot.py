# The grammar robot's logic.


class GrammarBot:

    def __init__(self):

        # The robot should never tweet to the same person twice. This object maintains a suppression list of
        # users that the bot has sent tweets to in history.

        # Pairs of words that the bot will suggest are swapped for each other.
        one_way_swaps = [('accept', 'except'),
                         ('affect', 'effect'),
                         ('allusion', 'illusion'),
                         ('ascent', 'assent'),
                         ('breath', 'breathe'),
                         ('capital', 'capitol'),
                         ('cite', 'sight'),
                         ('compliment', 'complement'),
                         ('conscience', 'conscious'),
                         ('council', 'counsel'),
                         ('elicit', 'illicit'),
                         ('immanent', 'imminent'),
                         ('lead', 'led'),
                         ('lie', 'lay'),
                         ('lose', 'loose'),
                         ('passed', 'past'),
                         ('precede', 'proceed'),
                         ('principal', 'principle'),
                         ('quote', 'quotation'),
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
        self.keywords = []
        for (first, second) in one_way_swaps:
            self.two_way_swaps.append((first, second))
            self.two_way_swaps.append((second, first))
            self.keywords.append(first)
            self.keywords.append(second)

    def grammar_check(self, message: str) -> str:
        """Returns a suggested substitution if the parm message contains a grammatical error,
        otherwise returns and empty string."""

        # Skip tweets that have none of the key words in them. Some replies seem to have neither.
        # Also skip tweets that have more than 1 keyword in them. They might be discussing the grammar difficulty!
        keyword_count = 0
        suggestion = ''
        for (keyword, substitute) in self.two_way_swaps:
            if keyword in message.lower():                  # Normalise tweets to lower case.
                keyword_count += 1
                suggestion = substitute

        if keyword_count == 1:
            return suggestion
        else:
            return ''
