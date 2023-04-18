#import needed modules
import requests
import sqlite3
import sys
from typing import Optional

#create database name
DATABASE_NAME = "npi_lookup.db"

#create tables for data model
CREATE_NPI_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS npi (
    npi INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
"""

CREATE_ADDRESSES_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS addresses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    npi INTEGER NOT NULL,
    address TEXT NOT NULL,
    FOREIGN KEY (npi) REFERENCES npi (npi)
);
"""

CREATE_TAXONOMIES_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS taxonomies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    npi INTEGER NOT NULL,
    taxonomy TEXT NOT NULL,
    FOREIGN KEY (npi) REFERENCES npi (npi)
);
"""




def get_npi_data(npi: int) -> Optional[dict]:
    """def get_npi_data grabs data from the NPPES API using version 2.1.
    The function grabs the json response of an NPI and processes it to be inserted into the database."""
    url = f"https://npiregistry.cms.hhs.gov/api/?number={npi}&version=2.1"
    response = requests.get(url)
    #code logic for errors
    if response.status_code != 200:
        print(f"Error: API request failed with status code {response.status_code}")
        return None
    #pass json data to a variable
    data = response.json()
    #if you dont get a result returned print error and return none.
    if data["result_count"] == 0:
        print(f"Error: NPI {npi} not found")
        return None
    #grab the specific fields we want for now.
    result = data["results"][0]
    basic_info = result["basic"]
    addresses = result["addresses"]
    taxonomies = result["taxonomies"]
    name = basic_info["first_name"] + " " + basic_info["last_name"]
    type = result["enumeration_type"]
    address_list = [addr["address_1"] + ", " + addr["city"] + ", " + addr["state"] + ", " + addr["postal_code"] for addr in addresses]
    taxonomy_list = [tax["desc"] for tax in taxonomies]

    return {
        "npi": npi,
        "name": name,
        "addresses": address_list,
        "type": "Individual" if type == "NPI-1" else "Organization",
        "taxonomies": taxonomy_list
    }


def store_npi_data(data: dict) -> None:
    """def store_npi_data grabs the data variable and proceeds to insert data into tables"""
    #connect to sqlite
    with sqlite3.connect(DATABASE_NAME) as conn:
        conn.execute(CREATE_NPI_TABLE_SQL)
        conn.execute(CREATE_ADDRESSES_TABLE_SQL)
        conn.execute(CREATE_TAXONOMIES_TABLE_SQL)
        #run inserts
        conn.execute(
            "INSERT OR REPLACE INTO npi (npi, name, type, updated) VALUES (?, ?, ?, CURRENT_TIMESTAMP)",
            (data["npi"], data["name"], data["type"])
        )

        conn.execute("DELETE FROM addresses WHERE npi = ?", (data["npi"],))
        for address in data["addresses"]:
            conn.execute("INSERT INTO addresses (npi, address) VALUES (?, ?)", (data["npi"], address))

        conn.execute("DELETE FROM taxonomies WHERE npi = ?", (data["npi"],))
        for taxonomy in data["taxonomies"]:
            conn.execute("INSERT INTO taxonomies (npi, taxonomy) VALUES (?, ?)", (data["npi"], taxonomy))

        conn.commit()



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <NPI>")
        sys.exit(1)

    npi = int(sys.argv[1])
    data = get_npi_data(npi)

    if data is not None:
        store_npi_data(data)
        print("NPI data stored successfully")
