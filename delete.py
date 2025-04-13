import psycopg2
from config import load_config

def delete_person(person_name):
    sql = """DELETE FROM Numbers WHERE person_name = %s;"""

    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (person_name,))
                print(person_name, "deleted successfully")
            conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

if __name__ == "__main__":
    person_name = input("Enter the person's name to delete: ")
    delete_person(person_name)
