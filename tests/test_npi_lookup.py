import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from npi_lookup import get_npi_data

class TestNPILookup(unittest.TestCase):
    pass

class TestNPILookup(unittest.TestCase):
    def test_fetch_data(self):
        npi = '1114160116'  # Replace with a valid NPI number
        data = get_npi_data(npi)
        self.assertIsNotNone(data)
        self.assertIn('npi', data)
        self.assertIn('name', data)
        self.assertIn('addresses', data)
        self.assertIn('type', data)
        self.assertGreater(len(data['taxonomies']), 0)

    def test_fetch_invalid_npi_data(self):
        npi = '0000000000'  # Replace with an invalid NPI number
        data = get_npi_data(npi)
        self.assertIsNone(data)


if __name__ == '__main__':
    unittest.main()
