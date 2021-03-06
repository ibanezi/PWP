# PWP SPRING 2021
# CalorieTracker
# Group information
* Student 1. Bekim Abazi, babazi(miukumauku)student.oulu.fi
* Student 2. Miika Kylander, mkylande(miukumauku)student.oulu.fi
* Student 3. Niklas Riikonen, niriikon(miukumauku)student.oulu.fi

__Remember to include all required documentation and HOWTOs, including how to create and populate the database, how to run and test the API, the url to the entrypoint and instructions on how to setup and run the client__
-----
# Setting up the database
## Dependencies
The requirements and dependencies needed for this project are included in the requirements.txt file.  
You can install them by running `pip install -r requirements.txt`.

## Database version
The project uses SQLite 3.34.0

## Database setup
You can setup the database by running `setup.py` with python. This creates a database from the models in `CalorieTracker/models.py` with a few example instances. The     database is created in `CalorieTracker/test.db`

## Database testing
Database tests are located in the `tests` folder. Simply run `pytest` to run all test files located in the folder or `pytest db_test.py` if you want to run only the database tests.
