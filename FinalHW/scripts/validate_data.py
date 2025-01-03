import psycopg2
import mysql.connector
import logging

logging.basicConfig(level=logging.INFO)

def validate_table_counts(pg_conn, mysql_conn, table_name):
    pg_cursor = pg_conn.cursor()
    mysql_cursor = mysql_conn.cursor()

    pg_cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
    pg_count = pg_cursor.fetchone()[0]

    mysql_cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
    mysql_count = mysql_cursor.fetchone()[0]

    if pg_count != mysql_count:
        logging.error(f"Ошибка в таблице {table_name}: количество строк не совпадает (PostgreSQL: {pg_count}, MySQL: {mysql_count}).")
    else:
        logging.info(f"Таблица {table_name}: количество строк совпадает ({pg_count} строк).")

def main():
    pg_conn = psycopg2.connect(
        dbname="mydb",
        user="admin",
        password="admin",
        host="localhost",
        port="5432"
    )
    mysql_conn = mysql.connector.connect(
        host="localhost",
        user="admin",
        password="admin",
        database="mydb"
    )

    tables = ['Users', 'ProductCategories', 'Products', 'Orders', 'OrderDetails']
    for table in tables:
        validate_table_counts(pg_conn, mysql_conn, table)

    pg_conn.close()
    mysql_conn.close()

if __name__ == "__main__":
    main()