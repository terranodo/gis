import unittest
import gis


class TestGis(unittest.TestCase):

    def test_import(self):
        self.assertTrue(gis.__file__)


if __name__ == '__main__':
    unittest.main()
