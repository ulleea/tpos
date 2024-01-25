import mariadb
import os
from loguru import logger
import pandas as pd

from time import sleep

import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse, JSONResponse


# same code with uploader service
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


app = FastAPI()

CONNECTION_TIMEOUT = 100


@app.on_event('startup')
def startup():
    global CONNECTION_TIMEOUT
    table_name = os.environ.get("TABLE_NAME")
    db = MariaDB.init_from_env()

    wait_time = 0
    logger.info("wait data in db")
    while db.is_empty(table_name):
        if wait_time > CONNECTION_TIMEOUT:
            raise Exception(f'table: {table_name} is empty > {CONNECTION_TIMEOUT}')

        sleep(1)
        logger.info("wait data in db")
        wait_time += 1

    logger.info("data in db")


@app.get('/health')
def health(_: Request):
    logger.info('health ok')
    # return Response(content="Ok\n", status_code=200)
    return JSONResponse(content={"status": "OK"}, status_code=200)


@app.get('/', response_class=HTMLResponse)
def get_all_table(_: Request):
    table_name = os.environ.get("TABLE_NAME")
    logger.info('get data from db')
    db = MariaDB.init_from_env()
    df = db.get_table(table_name)
    logger.info(df)
    return df.to_html(index=False, justify='center')


def main():
    # "0.0.0.0" "192.168.1.25"
    uvicorn.run(app, host="192.168.1.26", port=int(os.getenv('SERVICE_PORT', "8000")))


if __name__ == '__main__':
    main()
