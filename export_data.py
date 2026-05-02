from pymongo import MongoClient
import pandas as pd

# Paste your MongoDB Atlas connection string here
client = MongoClient("mongodb+srv://Abin:TrivianBoyz@cluster0.duswltu.mongodb.net/lmsDB?appName=Cluster0")

# Put your actual database name here
db = client["lmsDB"]

# Get all collections
collections = db.list_collection_names()

print("Collections found:", collections)

# Export each collection to separate CSV
for col in collections:
    data = list(db[col].find())

    print(f"{col}: {len(data)} records")

    if len(data) == 0:
        continue

    df = pd.DataFrame(data)

    if "_id" in df.columns:
        df.drop("_id", axis=1, inplace=True)

    df.to_csv(f"{col}.csv", index=False)

print("All collections exported successfully!")