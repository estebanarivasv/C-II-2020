## Setting up the environment
### <b>Client</b> configuration 
1. Situate in `/client` folder.
2. Create a virtual environment.
3. Activate environment.

    `source /bin/activate`
4. Install the requirements in that environment.

    `pip3 install -r requirements.txt`

### <b>Server</b> configuration 
1. Install MySQL dependencies: 

    ```sudo apt-get install python3-dev default-libmysqlclient-dev build-essential```
2. Situate in `/server` folder
2. Create a virtual environment.
3. Activate environment.

    `source /bin/activate`
4. Install the requirements in that environment.

    `pip3 install -r requirements.txt`
5. Create a `.env` file. There's a template called `.env-example`. And specify the environment variables: `DB_URI, MYSQL_DATABASE, MYSQL_USER, MYSQL_PASSWORD`.
6. Run the `docker-compose.yml` file to start the MySQL server.
7. Add some operators to the table after created with the `app.py` file. There are some sample operators in these files: `sample_operators.csv`, `sample_operators.sql`.