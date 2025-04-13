import psycopg2
from config import load_config


def insert_player(username, score):
    """ Insert a new player into the players table """

    sql = """INSERT INTO players(username, score)
             VALUES(%s, %s) RETURNING player_id;"""

    player_id = None
    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # execute the INSERT statement
                cur.execute(sql, (username, score))

                # get the generated id back
                rows = cur.fetchone()
                if rows:
                    player_id = rows[0]

                # commit the changes to the database
                conn.commit()
                print("Player inserted successfully")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        return player_id
    
