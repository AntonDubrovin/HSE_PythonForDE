from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.mysql.hooks.mysql import MySqlHook
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)

def replicate_data():
    postgres_hook = PostgresHook(postgres_conn_id='postgres_default')
    mysql_hook = MySqlHook(mysql_conn_id='mysql_default')

    tables = ['Users', 'ProductCategories', 'Products', 'Orders', 'OrderDetails']
    for table in tables:
        try:
            query = f"SELECT * FROM {table};"
            data = postgres_hook.get_records(query)
            if data:
                mysql_hook.insert_rows(table=table, rows=data)
            logging.info(f"Replicated {len(data)} rows from {table}.")
        except Exception as e:
            logging.error(f"Error replicating {table}: {e}")

def create_analytical_tables():
    mysql_hook = MySqlHook(mysql_conn_id='mysql_default')

    sales_by_category_query = """
    CREATE TABLE IF NOT EXISTS SalesByCategory AS
    SELECT 
        c.name AS category_name,
        SUM(od.total_price) AS total_sales,
        COUNT(DISTINCT o.order_id) AS total_orders
    FROM 
        OrderDetails od
    JOIN 
        Products p ON od.product_id = p.product_id
    JOIN 
        ProductCategories c ON p.category_id = c.category_id
    JOIN 
        Orders o ON od.order_id = o.order_id
    GROUP BY 
        c.name;
    """
    mysql_hook.run(sales_by_category_query)

    user_loyalty_query = """
    CREATE TABLE IF NOT EXISTS UserLoyalty AS
    SELECT 
        u.user_id,
        u.first_name,
        u.last_name,
        u.loyalty_status,
        COUNT(o.order_id) AS total_orders,
        SUM(o.total_amount) AS total_spent,
        MAX(o.order_date) AS last_order_date
    FROM 
        Users u
    LEFT JOIN 
        Orders o ON u.user_id = o.user_id
    GROUP BY 
        u.user_id, u.first_name, u.last_name, u.loyalty_status;
    """
    mysql_hook.run(user_loyalty_query)

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'replicate_postgres_to_mysql',
    default_args=default_args,
    schedule_interval='@daily',
)

replicate_task = PythonOperator(
    task_id='replicate_data',
    python_callable=replicate_data,
    dag=dag,
)

create_tables_task = PythonOperator(
    task_id='create_analytical_tables',
    python_callable=create_analytical_tables,
    dag=dag,
)

replicate_task >> create_tables_task