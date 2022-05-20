import os
from dotenv import load_dotenv
from mysql.connector import pooling

load_dotenv()


MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_DATABASE = 'movie'


# class Database:
#     def __init__(self):
#         self.pool = pooling.MySQLConnectionPool(
#             pool_name='pool',
#             pool_size=5,
#             pool_reset_session=True,
#             host=MYSQL_HOST,
#             database=MYSQL_DATABASE,
#             user=MYSQL_USER,
#             password=MYSQL_PASSWORD,
#         )
#
#     def get_connection(self):
#         self.get_connection()


pool = pooling.MySQLConnectionPool(
            pool_name='pool',
            pool_size=5,
            pool_reset_session=True,
            host=MYSQL_HOST,
            database=MYSQL_DATABASE,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD)
