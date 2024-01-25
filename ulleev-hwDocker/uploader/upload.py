# import psycopg2
import mariadb
import os
from loguru import logger
import pandas as pd


class MariaDB:
    def __init__(self, user: str, password: str, host: str, db: str, port: int) -> None:
        self.user = user
        self.password = password
        self.host = host
        self.db = db
        self.port = port

    @classmethod
    def init_from_env(cls):
        db_creds = dict(
            user=os.getenv('MYSQL_USER', 'root'),
            password=os.getenv('MYSQL_PASSWORD', 'root'),
            host=os.environ.get("DBHOST"),
            db=os.getenv('MYSQL_DB', 'db'),
            port=int(os.getenv('PORT', '5432')),
        )
        return cls(**db_creds)

    def create_connection(self):
        return mariadb.connect(user=self.user, password=self.password,
                                host=self.host, port=self.port, dbname="data")

    def is_empty(self, table_name: str):
        con = self.create_connection()
        cur = con.cursor()
        cur.execute("SELECT * FROM information_schema.tables WHERE table_name=%s", (table_name,))
        res = cur.rowcount
        logger.info(res)
        con.close()
        return not bool(res)

    def get_table(self, table_name: str) -> pd.DataFrame:
        con = self.create_connection()
        cur = con.cursor()
        cur.execute(f"SELECT * from {table_name}")
        data = cur.fetchall()
        logger.info(data)
        con.close()
        return pd.DataFrame(data, columns=['name', 'age'])


def upload_data():
    logger.info("Start upload data in db")

    db = MariaDB.init_from_env()
    con = db.create_connection()
    table_name = os.getenv('TABLE_NAME', 'people_age')
    logger.info("Connection completed successfully")

    cur = con.cursor()
    if db.is_empty(table_name):
        logger.info("Table don't exit, create")

        cur.execute(''' CREATE TABLE {} (
                        name VARCHAR PRIMARY KEY,
                        age INT  NOT NULL );'''.format(table_name))
        logger.info("Insert data in table")
        with open('data/data.csv', 'r') as f:
            next(f)
            cur.copy_from(f, table_name, sep=',')
        con.commit()
        logger.info("Table created and filled successfully")
    else:
        logger.info('Table already exit')

    logger.info('Check data in table')
    logger.info(db.get_table(table_name))
    con.close()


if __name__ == '__main__':
    upload_data()
