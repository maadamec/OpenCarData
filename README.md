# OpenCarData

OpenCarData is a Python project for crawling car resellers websites and scraping information about the prices and offered cars. The project is designed to be modular, so it can be easily extended to support new resellers and data sources.

## Installation - docker
Clone the repository:
```bash
git clone https://github.com/maadamec/OpenCarData.git
cd opencardata
```

Run docker compose:
```bash
docker-compose up
```

If you want to change user name, password and other attributes, change them in [.env](.env) file

## Installation - local development
Clone the repository and install the dependencies manually:

You will probably need to install postgresql to your system. On linux, you can do it with apt-get:

```bash
sudo apt-get install postgresql postgresql-contrib
```

or on Mac:

```bash
brew install postgresql
```

Clone the repository:

```bash
git clone https://github.com/maadamec/OpenCarData.git
cd opencardata
```

Prepare virtual environment and install dependencies:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

and then activate the virtual environment:

```bash

or on windows:

```shell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

Prepare the PostgreSQL database. If you don't have one prepared, you can easily create one with docker

```bash
docker run -itd -e POSTGRES_USER=username -e POSTGRES_PASSWORD=password -p 5432:5432 -v "<path to to directory where data can be persisted>:/var/lib/postgresql/data" --name postgresql postgres
```

Set the database connection string in the app.py file, so the application can publish data there:

```
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://<username>:<password>@<host>:<port>/<dbname>'
```

or set the environment variable:

```bash
export DATABASE_HOST=<host>
export DATABASE_PORT=<port>
export DATABASE_DB=<dbname>
export DATABASE_USER=<username>
export DATABASE_PASSWORD<password>
```

Run the main.py file

```bash
python main.py
```

## Usage
With every run
- New job record is created and all records created durring this run are associated with this job for traceability.
- First the resellers are crawled for actual offered cars and list of sold cars is updated.
- In second phase, all records in the database are crawled and the variable data are captured. 

## Before using
Please, before using this application, check autoesa [robots.txt](https://www.autoesa.cz/robots.txt) file for resources that should not be crawled.

## Contributing
If you want to contribute to OpenCarData, you can fork the repository and create a new branch for your changes.
Please make sure to write tests for any new functionality you add, and ensure that all the existing tests pass 
before submitting a pull request.

## License
OpenCarData is released under the MIT License. See LICENSE.txt for details.
