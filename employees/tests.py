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

    def test_get_item(self):
        a = [ { 'id': 1, 'name': 'test1' }, { 'id': 2, 'name': 'test2' }, { 'id': 3, 'name': 'test3' } ]
        r = utils.get_item(a, lambda item: item['id'] == 2)
        self.assertIsNotNone(r)
        self.assertEqual(r['name'], 'test2')

    def test_char_range(self):
        myrng = [ 'A', 'B', 'C', 'D' ]
        rng = list(utils.char_range('A', 'D'))
        isEqual = utils.compare(myrng, rng)
        self.assertTrue(isEqual)
