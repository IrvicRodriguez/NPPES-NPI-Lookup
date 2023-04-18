# NPI Lookup

This project retrieves and stores information about healthcare providers using their National Provider Identifier (NPI) 
from the [NPPES NPI Registry](https://npiregistry.cms.hhs.gov). The data is fetched using the NPPES API and stored in an SQLite database.

## Installation

1. Clone this repository:

https://github.com/IrvicRodriguez/NPPES-NPI-Lookup

2. Create and activate a virtual environment (optional but recommended): 

python3 -m venv venv
source venv/bin/activate

3. Install the required Python packages:

pip install -r requirements.txt

## Usage

To fetch and store NPI data for a specific NPI, run the following command:

python npi_lookup.py `<NPI>`


Replace `<NPI>` with the NPI number you want to look up. The script will fetch the provider's data from the NPPES API and store it in an SQLite database named `npi_lookup.db`.

## Configuration

By default, the script uses an SQLite database named `npi_lookup.db`. If you want to change the database name, update the `DATABASE_NAME` variable in the `npi_lookup.py` script.

## To run unit testing: 
run: python tests/test_npi_lookup.py

`Expected output should be:  python tests/test_npi_lookup.py

Error: NPI 0000000000 not found
..
----------------------------------------------------------------------
Ran 3 tests in 0.532s

OK
`

## Extending data model:

There is a branch called extending data model. This is in a pull request to hightlight the changes for the functions to get data and store it. Also, it shows the models.py file being changed to add a telephone column.
if you wish to play with the automated data migration for a phone. make the pull request branch the active one and then run: `alembic upgrade head`

you should see an output like: 
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade d952e8585942 -> 2dcc5211493f, Adding telephone column 2

Then you can go ahead and check the database to see the new column in the NPI table. 

If you run the command to insert or update data for an NPI: `python npi_lookup.py 1134416456` you should see the phone number added to the row.

Furthermore, unit test will fail in pull request branch until you run the migration command and insert new data that brings in a phone. 
