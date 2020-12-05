import unittest, bots, random
from bots import get_nim_sum

basic_starts = (
    ((1,2), (1,1)),
    ((1,3), (1,1)),
    ((1,1,2), (1,1,0))
)

def generate_list(num = 10, lengths = []):
    "Generates num lists of varying lengths."
    if not lengths:
        lengths = [i for i in range(1,num*5,5)]
    index =  0
    while index < num:
        yield tuple(random.randint(1,100) for counter in range(lengths[index]))
        index += 1

class SmartPlayTest(unittest.TestCase):
    "Tests wether the SmartBots play is working."
    def test_known_starts(self):
        "Should perform the only winning moves at the known positions."
        bot = bots.SmartBot()
        for start_list, optimal_move in basic_starts:
            l2 = list(start_list)
            bot.make_move(l2)
            self.assertEqual(tuple(l2), optimal_move)
    def test_random_starts(self):
        "Should always win when starting in winning position"
        players = (bots.SmartBot(), bots.RandomBot())
        for starting_list in generate_list(100, [random.randint(1,50) for i in range(100)]):
            nim_sum = get_nim_sum(starting_list)
            current_list = list(starting_list)

            turn = 0
            while current_list:
                if not players[turn%2].make_move(current_list):
                    break
                turn += 1
            winner = (turn+1)%2
            if nim_sum:
                self.assertEqual(winner, 0)


class Validness(unittest.TestCase):
    "Tests that all performed moves are valid."

    def valid_move_helper(self, bot):
        """Bots should make valid moves. Meaning always remove at least 1, and never more than possible."""
        for start_list, optimal_move in basic_starts:
            l2 = list(start_list)
            bot.make_move(l2)
            self.assertNotEqual(start_list, tuple(l2))
            self.assertFalse([x for x in l2 if x<0])
        for start_list in generate_list():
            l2 = list(start_list)
            bot.make_move(l2)
            self.assertNotEqual(start_list, tuple(l2))
            self.assertFalse([x for x in l2 if x<0])

    def false_returns_helper(self, bot):
        "Bot should return false when there is no move left."
        lose_states = ((), (0,), (0,0), (0,0,0,0,0,0,0,0,0,0))
        for state in lose_states:
            l = list(state)
            self.assertIs(bot.make_move(l), False)
            self.assertEqual(tuple(l), state)

    def test_valid_random(self):
        """RandomBot should make valid moves. Meaning always remove at least 1, and never more than possible."""
        self.valid_move_helper(bots.RandomBot())
    def test_valid_smart(self):
        """SmartBot should make valid moves. Meaning always remove at least 1, and never more than possible."""
        self.valid_move_helper(bots.SmartBot())
    def test_false_returns_random(self):
        "Random bot should return false when there is no move left."
        self.false_returns_helper(bots.RandomBot())
    def test_false_returns_smart(self):
        "Smart bot should return false when there is no move left."
        self.false_returns_helper(bots.SmartBot())

if __name__ == "__main__":
    unittest.main()

