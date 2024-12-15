from kafka import KafkaConsumer
import json
from collections import defaultdict

def analyze_data():
    consumer = KafkaConsumer(
        'example_topic',
        bootstrap_servers='localhost:9092',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    user_actions = defaultdict(int)

    for message in consumer:
        record = message.value
        user_id = record['user_id']
        action = record['action']

        if action in ["click", "purchase"]:
            user_actions[user_id] += 1

    # Вывод пользователей с наибольшим количеством действий
    top_users = sorted(user_actions.items(), key=lambda x: x[1], reverse=True)[:5]
    for user_id, count in top_users:
        print(f"User ID: {user_id}, Actions: {count}")

if __name__ == "__main__":
    analyze_data()
