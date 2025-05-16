import random
from faker import Faker
import pandas as pd

fake = Faker()

data = {
    "name": [],
    "email": []
}

for _ in range(100):
    name = fake.name()
    # Randomly mess with case and add spaces
    name = f" {name.upper() if random.random() > 0.5 else name.lower()} "
    if random.random() > 0.5:
        name = " " + name + "  "
    
    email = fake.email()
    email = f" {email.upper() if random.random() > 0.5 else email.lower()} "
    if random.random() > 0.5:
        email = " " + email + "  "
    
    data["name"].append(name)
    data["email"].append(email)

df = pd.DataFrame(data)
df.to_csv("raw_customers_100.csv", index=False)

print("CSV with 100 customers generated as raw_customers_100.csv")
