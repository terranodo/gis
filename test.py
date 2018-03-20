import unittest
import gis

class TestGis(unittest.TestCase):

    def test_udummy(self):
        self.assertEqual('foo'.upper(), 'FOO')

if __name__ == '__main__':
    unittest.main()
