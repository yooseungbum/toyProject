from crawling import lotto_crawling, powerBall_crawling
import sqlalchemy as db
import yaml
import pandas as pd

# 서버접속정보 등 설정값 로딩.
def load_config():
    global config
    with open("config.yaml", "r", encoding='utf8') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

# Toysmyth:3308 MariaDB에 접속
def mysql_connect():
    # Connect to a MySQL server
    # :return connection: Global MySQL database connection

    global connection
    connection = db.create_engine(
        "mysql+pymysql://"
        + str(config["my_user"])
        + ":"
        + str(config["my_pw"])
        + "@"
        + str(config["my_addr"])
        + ":"
        + str(config["my_port"])
        + "/"
        + str(config["my_db"])
    )

# 쿼리를 실행하여 데이터를 df로 반환
def run_query(sql):
    # Runs a given SQL query via the global database connection.
    # param sql: MySQL query
    # return: Pandas dataframe containing results

    return pd.read_sql(sql, connection)

# DB 접속 종료
def db_disconnect():
    # Closes the MySQL database connection.
    connection.dispose()

if __name__ == '__main__':
    # lotto_crawling()
    powerBall_crawling()


