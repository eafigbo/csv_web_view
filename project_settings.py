# Name of MongoDB database to be used or path to SQLite file
DEFAULT_DB_NAME = "csv_test.db"

# Name of MongoDB collection to be used
DEFAULT_COLLECTION = "test_docs2"

# Server where MongoDB database is hosted
DEFAULT_DB_HOST = "localhost"

# Port where Mongo DB is running
DEFAULT_DB_PORT = 27017

# How many records you want displayed per page
DEFAULT_RECORDS_PER_PAGE = 1

# Display name of website
DEFAULT_SITE_NAME = "CSV Display"

# HTTP Port on which you want the web server to run
DEFAULT_PORT = 8080

# Directory for saving temp files
DEFAULT_TEMP_DIR = '/tmp'

DB_DRIVER_CLASS = 'db_driver.sqlite_driver.SQLiteDriver'

#SQL statement to create table in SQLite if it does not already exist
SQLITE_CREATE_TABLE_STATEMENT = """
                            CREATE TABLE IF NOT EXISTS "data" (
                                "json_field"	TEXT
                            );
                            """
