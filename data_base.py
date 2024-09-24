import data_stream
import psycopg2
from config_db import host, user, password, db_name


try:
    conn = psycopg2.connect(
        host = host,
        user = user,
        password = password,
        database = db_name
    )

    conn.autocommit = True

    with conn.cursor() as cursor:

        def insert_data(values):
            cursor.execute(
            f"""CREATE TABLE IF NOT EXISTS {values[0]} (
                close_price REAL NOT NULL,
                time TIMESTAMP NOT NULL
                );
                
                INSERT INTO {values[0]} VALUES ({values[1]}, '{values[2]}');
                """)
            
        def select_data(values):
            cursor.execute(
                f"""
                SELECT close_price 
                FROM {values[0]} 
                WHERE time = (SELECT MAX(time) from {values[0]})
                """)
            print(cursor.fetchall(), f"Figi: {values[0]}" )

        #################################
        for values in data_stream.data():
            insert_data(values)
            select_data(values)


except Exception as ex:
    print("Error while working with PostgreSQL", ex)
finally:
    if conn:
        conn.close()
        print("PostgreSQL connection closed")






