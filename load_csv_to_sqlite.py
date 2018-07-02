#from src.db_handling import add_user, add_rating, add_stat, add_mensa, add_feedback, add_food
import csv, sqlite3
import pandas as pd
import os

db_path = "mensabot.db"
csv_files = ["feedback.csv", "food.csv", "foodrating.csv", "mensa.csv", "stat.csv", "user.csv"]

column_names = {
    "mensa": ["id", "name", "short_name"],
    "food": ["id", "description", "price", "date", "mensa_id"],
    "user": ["id", "chat_id", "subscription_time", "subbed_mensas"],
    "foodrating": ["id", "date", "rating", "user_id", "food_id"],
    "stat": ["id", "datetime", "total_users", "subbed_users", "ratings"],
    "feedback": ["id", "datetime", "feedback_text", "user_id"]
}

con = sqlite3.connect(db_path)

if __name__ == "__main__":    
    for csv_file in csv_files:
        table_name = os.path.splitext(os.path.basename(csv_file))[0]
        df = pd.read_csv(csv_file, names=column_names[table_name])

        try:
            df.to_sql(table_name, con, if_exists='append', index=False)
        except sqlite3.IntegrityError:
            print("Table already inserted.")