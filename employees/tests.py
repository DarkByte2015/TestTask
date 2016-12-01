from django.test import TestCase
from . import utils

class UtilsTestCase(TestCase):
    def test_compare(self):
        a = [ 1, 2, 3 ]
        b = [ 1, 2, 3 ]
        c = [ 3, 2, 1 ]
        self.assertTrue(utils.compare(a, b))
        self.assertFalse(utils.compare(a, c))

    def test_flatten(self):
        lst = [ [ 1, 2, 3 ], [ 4, [ 5, 6 ] ] ]
        mylst = [ 1, 2, 3, 4, 5, 6 ]
        flst = list(utils.flatten(lst))
        isEqual = utils.compare(mylst, flst)
        self.assertTrue(isEqual)

    def test_letter_range(self):
        myrng = [ 'A', 'B', 'C', 'D' ]
        rng = list(utils.letter_range('A', 'D'))
        isEqual = utils.compare(myrng, rng)
        self.assertTrue(isEqual)

    def test_distribute_by_letters(self):
        employees = [ 'Колесников', 'Павлов', 'Макаров' ]
        letters, avg = utils.distribute_by_letters(employees)
        self.assertEqual(avg, 1)
