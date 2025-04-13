import psycopg2
import csv
from config import load_config


def insert_person(person_name, person_phone):
    """ Insert a new vendor into the vendors table """

    sql = """INSERT INTO Numbers(person_name, person_phone)
             VALUES(%s, %s) RETURNING person_id;"""

    person_id = None
    config = load_config()

    try:
        with  psycopg2.connect(**config) as conn:
            with  conn.cursor() as cur:
                # execute the INSERT statement
                cur.execute(sql, (person_name, person_phone))


                # get the generated id back
                rows = cur.fetchone()
                if rows:
                    person_id = rows[0]

                # commit the changes to the database
                conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        return person_id

def insert_many_persons(person_dict):

    print(type(person_dict)) # <class 'list'>
    """ Insert multiple persons into the numbers table  """

    sql = "INSERT INTO numbers(person_name, person_phone) VALUES (%s, %s) RETURNING *"
    config = load_config()
    try:
        with  psycopg2.connect(**config) as conn:
            with  conn.cursor() as cur:
                # execute the INSERT statement
                cur.executemany(sql, person_dict)

            # commit the changes to the database
            conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def insert_from_csv(csv_file):
    config = load_config()
    try:
        with  psycopg2.connect(**config) as conn:
            with  conn.cursor() as cur:
                with open(csv_file, 'r') as f:
                    reader = csv.reader(f)
                    next(f)

                    for row in reader:
                        # Ensure both person_name and person_phone are provided from the CSV row
                        cur.execute("INSERT INTO numbers(person_name, person_phone) VALUES(%s, %s)", (row[0], row[1]))
                
                conn.commit()
                cur.close()
                print("data inserted successfully")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn:
            conn.close()

def clear_table():
    """ Clear the table """
    config = load_config()
    try:
        with  psycopg2.connect(**config) as conn:
            with  conn.cursor() as cur:
                cur.execute("DELETE FROM Numbers")
                conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

if __name__ == '__main__':
    clear_table()
    
    insert_many_persons([
        ("Kanye", "111-222-3333"),
        ("Lil Baby", "444-555-6666"),
        ("J Cole", "777-888-9999"),
        ("Lil Wayne", "000-111-2222"),
    ])

    name = input("Enter your name: ")
    phone = input("Enter your phone number: ")

    insert_person("Drake", "123-456-7890")
    insert_person("Tyler, the Creator", "987-654-3210")
    insert_person(name, phone)
    insert_person("A$AP Rocky", "111-222-3333")

    insert_from_csv("data.csv")