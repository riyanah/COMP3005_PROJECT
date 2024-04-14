# COMP3005_A3

COMP3005 A3 Student Database

## Video Demonstration Link

[Click here](https://youtu.be/WTXzhKB9XFc) to view the video demonstration of the application. The video showcases the functionality of the application, including database operations and the effects of those operations.

https://youtu.be/WTXzhKB9XFc

### Prerequisites

What things you need to install the software and how to install them:

- PostgreSQL
- Python 3.x
- pip
- Virtualenv

### Installing

#### Clone the Repository

```bash
git clone https://github.com/riyanah/COMP3005_A3.git
cd COMP3005_A3
```

#### Set Up the Database

Navigate to the database directory and create a database.
Then run the scripts in the a3.sql file to set up your PostgreSQL database.
Replace DB_USER and DB_NAME with your PostgreSQL username and the name of your database, respectively.

```python
DB_NAME = "A3"
DB_USER = "user2"
DB_PASSWORD = "postgres"
DB_HOST = "localhost"
```

Step 3: Install Dependencies
Navigate back to the root directory and set up a Python virtual environment (optional):

```bash
python3 -m venv venv
source venv/bin/activate
```

Install the required Python packages:

```bash
pip install psycopg2-binary
```

Then to run the program:

```bash
python3 a3.py
```

Then test the CRUD functionality by uncommenting the lines needed.
