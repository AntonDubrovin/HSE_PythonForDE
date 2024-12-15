import json
import random
from datetime import datetime, timedelta

actions = ["login", "logout", "purchase", "click"]

def generate_data(num_records=100):
    data = []
    for i in range(num_records):
        user_id = random.randint(1, 10)
        action = random.choice(actions)
        timestamp = (datetime.utcnow() - timedelta(minutes=random.randint(0, 60))).isoformat()
        data.append({"user_id": user_id, "action": action, "timestamp": timestamp})
    return data

if __name__ == "__main__":
    data = generate_data()
    for record in data:
        print(json.dumps(record))
