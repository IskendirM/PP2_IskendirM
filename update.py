import psycopg2
from config import load_config

def update_score(username, score):

    sql = """UPDATE players
             SET score = %s
             WHERE username = %s;"""
    
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (score, username))
            conn.commit()
            print("Score updated successfully")

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

