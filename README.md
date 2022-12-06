# QRkot_spreadseets

Charitable foundation for the support of cats.

The Foundation collects donations for various targeted projects: for medical care for needy cats, for arranging a cat colony in the basement, for feeding cats left without care - for any purpose related to supporting the cat population.

### Projects

Several target projects can be opened in the QRKot Foundation. Each project has a name, description and amount to be raised. After the required amount is collected, the project is closed.

### Donations

Each user can make a donation and accompany it with a comment. Donations are not targeted: they are made to the fund, and not to a specific project. Each donation received is automatically added to the first open project that has not yet collected the required amount.

### Report

You can get a report listing funded projects sorted by the time it took to close completely.


## How to start

First you need clone the repository:

```bash
git clone git@github.com:SergoSolo/cat_charity_fund.git
```

```
cd cat_charity_fund
```

Create and activate virtual environment:

```bash
python -m venv venv
```

* Activation for Linux/MacOS

    ```bash
    source venv/bin/activate
    ```

* Activation for windows

    ```bash
    source venv/scripts/activate
    ```

Install requirements: 

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Usage

### First:

In the .env file, describe the environment variables:

```
    DATABASE_URL=<connection to the database: sqlite+aiosqlite:///./development.db>
    SECRET=<Secret key>
    FIRST_SUPERUSER_EMAIL=<email superuser>
    FIRST_SUPERUSER_PASSWORD=<password superuser>
    TYPE=<service_account>
    PROJECT_ID=inbound-trainer-370105
    PRIVATE_KEY_ID=<private key id>
    PRIVATE_KEY=-----BEGIN PRIVATE KEY-----\<your private key>\n-----END PRIVATE KEY-----\n
    CLIENT_EMAIL=<client email>
    CLIENT_ID=<client id>
    AUTH_URI=<auth uri>
    TOKEN_URI=<token uri>
    AUTH_PROVIDER_X509_CERT_URL=< auth x509 cert url>
    CLIENT_X509_CERT_URL=<client x509 cert url>
    EMAIL=<email>

```

### Second:

In your terminal, issue the command for migrations:

```bash
alembic upgrade head
```

To start a project:

```bash
uvicorn app.main:app --reload
```

## You will find all the necessary information about api in the documentation:

- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/redoc


##  Used technologies:
- Python version 3.10
- FastAPI
- FastAPI Users
- Alembic
- SQLAlchemy
- Pydantic
- Google Drive API
- Google Sheets API


## Author:
> [Sergey](https://github.com/SergoSolo)