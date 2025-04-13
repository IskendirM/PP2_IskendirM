import psycopg2
from config import load_config

def get_score_by_username(username):
    """Fetch score by username."""
    
    sql = """SELECT username, score
             FROM players
             WHERE username = %s;"""
    
    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (username,))
                result = cur.fetchone()
                return int(result[1]) if result else None  # Return the score as int or 0 if not found
                
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Database error: {error}")
        return 0  # Return 0 in case of an error
