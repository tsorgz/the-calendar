import os
import psycopg2

def get_psql_info():
    """
    Retrieves a PostgreSQL connection.

    Reads in PostgreSQL connection details via environment variables.
    """
    conn_string = os.getenv('POSTGRES_URI')
    conn_string = conn_string.replace("postgres://", "")
    parts = conn_string.split("@")
    auth = parts[0].split(":")
    username = auth[0]
    password = auth[1]
    host_port = parts[1].split(":")
    host = host_port[0]
    port_db = host_port[1].split("/")
    port = int(port_db[0])
    database = port_db[1]

    psql_conn = psycopg2.connect(
        dbname=database,
        user=username,
        password=password,
        host=host,
        port=port
    )

    psql_cursor = psql_conn.cursor()

    return (psql_conn, psql_cursor)