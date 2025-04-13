import psycopg2
from config import load_config

def update_phone(person_name, person_phone):
    updated_rows = 0

    sql = """UPDATE Numbers
             SET person_phone = %s
             WHERE person_name = %s;"""
    
    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (person_phone, person_name))
                updated_rows = cur.rowcount
                
            conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        return updated_rows
    
if __name__ == "__main__":
    person_name = input("Enter the person's name: ")
    person_phone = input("Enter the person's phone number: ")
    updated_rows = update_phone(person_name, person_phone)
    print(f"{updated_rows} row(s) updated.")