import psycopg2
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()

conn = psycopg2.connect(
    dbname="mydb",
    user="admin",
    password="admin",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

for _ in range(100):
    cursor.execute(
        "INSERT INTO Users (first_name, last_name, email, phone, registration_date, loyalty_status) VALUES (%s, %s, %s, %s, %s, %s)",
        (fake.first_name(), fake.last_name(), fake.email(), fake.phone_number(), fake.date_this_year(),
         random.choice(['Gold', 'Silver', 'Bronze']))
    )

categories = ['Электроника', 'Одежда', 'Книги', 'Мебель']
for category in categories:
    cursor.execute("INSERT INTO ProductCategories (name) VALUES (%s)", (category,))

for _ in range(50):
    cursor.execute(
        "INSERT INTO Products (name, description, category_id, price, stock_quantity, creation_date) VALUES (%s, %s, %s, %s, %s, %s)",
        (fake.word(), fake.text(), random.randint(1, 4), round(random.uniform(10, 1000), 2), random.randint(10, 100), fake.date_this_year())
    )

for _ in range(200):
    user_id = random.randint(1, 100)
    order_date = fake.date_time_this_year()
    cursor.execute(
        "INSERT INTO Orders (user_id, order_date, total_amount, status, delivery_date) VALUES (%s, %s, %s, %s, %s)",
        (user_id, order_date, round(random.uniform(50, 500), 2), random.choice(['Pending', 'Completed']),
         order_date + timedelta(days=random.randint(1, 7)))
    )

for order_id in range(1, 201):
    for _ in range(random.randint(1, 5)):
        product_id = random.randint(1, 50)
        quantity = random.randint(1, 3)
        cursor.execute("SELECT price FROM Products WHERE product_id = %s", (product_id,))
        price = cursor.fetchone()[0]
        cursor.execute(
            "INSERT INTO OrderDetails (order_id, product_id, quantity, price_per_unit, total_price) VALUES (%s, %s, %s, %s, %s)",
            (order_id, product_id, quantity, price, price * quantity)
        )

conn.commit()
cursor.close()
conn.close()
