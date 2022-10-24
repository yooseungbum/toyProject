from crawling import lotto_crawling, powerBall_crawling
import db_utils as db
import sys

if __name__ == '__main__':
    # db 연결
    try:
        db.mysql_connect()
        print("mariaDB connected")
    except Exception as err:
        print("connecting mariaDB error!!")
        print(err)
        sys.exit()
    # lotto_crawling()
    powerBall_crawling()

    # db 연결 종료
    db.db_disconnect()


