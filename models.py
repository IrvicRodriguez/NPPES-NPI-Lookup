from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime


Base = declarative_base()

class NPI(Base):
    __tablename__ = 'npi'

    npi = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    created = Column(TIMESTAMP, nullable=False, default=datetime.utcnow)
    updated = Column(TIMESTAMP, nullable=False, default=datetime.utcnow)

    addresses = relationship("Address", back_populates="npi_relation")
    taxonomies = relationship("Taxonomy", back_populates="npi_relation")
    telephone = Column(String(15))

class Address(Base):
    __tablename__ = 'addresses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    npi = Column(Integer, ForeignKey('npi.npi'))
    address = Column(String, nullable=False)

    npi_relation = relationship("NPI", back_populates="addresses")

class Taxonomy(Base):
    __tablename__ = 'taxonomies'

    id = Column(Integer, primary_key=True, autoincrement=True)
    npi = Column(Integer, ForeignKey('npi.npi'))
    taxonomy = Column(String, nullable=False)

    npi_relation = relationship("NPI", back_populates="taxonomies")
