import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from npi_lookup import get_npi_data, store_npi_data
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, NPI, Address, Taxonomy


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

    def test_store_npi_data(self):
        # Test storing valid data
        data = {
            "npi": 1234567890,
            "name": "John Smith",
            "type": "Individual",
            "addresses": ["123 Main St, Anytown, NY, 12345"],
            "taxonomies": ["Psychologist"]
        }
        store_npi_data(data)

        engine = create_engine(f"sqlite:///npi_lookup.db")
        Session = sessionmaker(bind=engine)
        session = Session()

        npi = session.query(NPI).filter(NPI.npi == data["npi"]).one()
        assert npi.name == data["name"]
        assert npi.type == data["type"]

        addresses = session.query(Address).filter(Address.npi == data["npi"]).all()
        assert len(addresses) == 1
        assert addresses[0].address == data["addresses"][0]

        taxonomies = session.query(Taxonomy).filter(Taxonomy.npi == data["npi"]).all()
        assert len(taxonomies) == 1
        assert taxonomies[0].taxonomy == data["taxonomies"][0]

        session.close()


if __name__ == '__main__':
    unittest.main()
