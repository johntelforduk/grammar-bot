# Script to test the GrammarBot class.

from grammar_bot import GrammarBot
import unittest


class TestGrammarBot(unittest.TestCase):

    def test_grammar_check(self):
        this_bot = GrammarBot()

        self.assertEqual(this_bot.grammar_check('I will take that as a compliment.'), 'complement')
        self.assertEqual(this_bot.grammar_check('Dave complements our team.'), 'compliment')
        self.assertEqual(this_bot.grammar_check('No keywords here.'), '')
        self.assertEqual(this_bot.grammar_check('I find complement and compliment confusing.'), '')
        self.assertEqual(this_bot.grammar_check('Compliment, compliments, compliments!'), 'complement')
        self.assertEqual(this_bot.grammar_check('Compliment'), 'complement')


if __name__ == '__main__':
    unittest.main()
