"""
Database Manager Module

This module implements the `DBManager` class, which is used for
connecting to a PostgreSQL database and managing database queries.

Key Features:
- Singleton class.
- Sets the connection string for the database.
- Connects to the database.
- Executes a database query and returns the result.

Classes:
----------
- DBManager:
"""
from typing import Optional
import psycopg
from dotenv import load_dotenv
from loguru import logger
from psycopg import connect

from settings import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
from singleton import SingletonMeta


class DBManager(metaclass=SingletonMeta):
    """
    Manages database interactions and provides utility methods
    to handle database connections and queries. Acts as a singleton.

    :ivar db_name: Name of the database to connect to.
    :type db_name: str
    :ivar db_user: Database username for authentication.
    :type db_user: str
    :ivar db_password: Password for the database user.
    :type db_password: str
    :ivar db_host: Host address of the database server.
    :type db_host: str
    :ivar db_port: Port number for the database connection.
    :type db_port: str
    :ivar conn_str: Connection string formatted for database connectivity.
    :type conn_str: Optional[str]
    :ivar conn: Active connection object to the database.
    :type conn: Optional[psycopg.Connection]
    """
    def __init__(self, env_file='../.env'):
        load_dotenv(env_file)
        self.db_name = DB_NAME
        self.db_user = DB_USER
        self.db_password = DB_PASSWORD
        self.db_host = DB_HOST
        self.db_port = DB_PORT
        self.conn_str = None
        self.set_conn_str()
        self.conn = None
        self.conn = self.connect()

    def set_conn_str(self) -> None:
        """
        Sets the connection string for the database connection.

        :rtype: None
        :return: This method does not return any value.
        """
        self.conn_str = (f"dbname={self.db_name} user={self.db_user} "
                         f"password={self.db_password} host={self.db_host} "
                         f"port={self.db_port}")
        logger.info(f'Setting connection string {self.conn_str}')

    def connect(self) -> psycopg.Connection:
        """
        Establishes a connection to a PostgreSQL database.

        :return:
            A connection object representing the database connection.

        :raises psycopg.Error:
        """
        try:
            self.conn = connect(self.conn_str)
            return self.conn
        except psycopg.Error as e:
            logger.error(f'Database connection error: {e}')

    def execute_query(self, query: str) -> None:
        """
        Executes a given SQL query within a database connection context.

        :param query: The SQL query to be executed.
        :type query: str
        :return: None
        :rtype: None
        :raises psycopg.Error:
        """
        try:
            with self.connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    conn.commit()
        except psycopg.Error as e:
            logger.error(f'Database query error: {e}')

    def execute_fetch_query(self, query: str, n: int = None) -> Optional[list]:
        """
        Executes a database query to fetch data and returns the results.
        Fetches all records if `n` is not specified;
        otherwise, fetches up to `n` records.

        :param query: The SQL query string to be executed on the database.
        :type query: str
        :param n: Optional number of rows to be fetched.
                    If not provided, all rows will be fetched.
        :type n: int, optional
        :return: A list of fetched database rows or None if the query fails.
        :rtype: Optional[list]
        """
        try:
            with self.connect() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query)
                    if not n:
                        return cursor.fetchall()
                    return cursor.fetchmany(n)
        except psycopg.Error as e:
            logger.error(f'Database fetch error: {e}')

    def init_tables(self):
        """
        Initializes database tables by executing SQL commands read from a file.

        Reads SQL commands from the 'init_tables.sql' file located in the same
        directory.
        The contents of the file are expected to contain the SQL queries
        needed to create or initialize database tables.

        :raises psycopg.Error: If there is an error executing the SQL commands.
        :return: None
        """
        try:
            with open('init_tables.sql', 'r') as file:
                sql = file.read()
            self.execute_query(sql)
        except psycopg.Error as e:
            logger.error(f'tables init error: {e}')

    def close(self):
        """
        Closes the active database connection

        :return: None
        """
        self.conn.close()
        self.conn = None