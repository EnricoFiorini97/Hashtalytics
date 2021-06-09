import sqlite3
import os

def tweet_search_by_user(user_screen_name="@nasa"):
    return f"SELECT * FROM 'api_tweet' as T WHERE T.user_screen_name = '{user_screen_name}' ORDER BY T.created_at DESC"


def tweet_search_by_hashtag(hashtag="#twitter"):
    return f"SELECT * FROM 'api_tweet' as T WHERE T.ent_hashtags LIKE '%{hashtag}%' ORDER BY T.created_at DESC"


def tweet_search_by_text(text="twitter"):
    return f"SELECT * FROM 'api_tweet' as T WHERE T.text LIKE '%{text}%' ORDER BY T.created_at DESC"


def custom_query(query=" SELECT * FROM 'api_tweet' "):
    if query is None:
        raise ValueError("Query must be a non-empty string.")
    try:
        path = os.path.dirname(os.path.realpath(__file__))
        sqliteConnection = sqlite3.connect(str(path)[:-3] + 'db.sqlite3')
        sqliteConnection.row_factory = sqlite3.Row
        cursor = sqliteConnection.cursor()
        cursor.execute(query)
        record = [dict(r) for r in cursor.fetchall()]
        cursor.close()
        return record
    except sqlite3.Error:
        print("Error occured while connecting to DB. Check your DB path.")


