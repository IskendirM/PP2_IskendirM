import psycopg2
import csv

import update
from config import load_config

# 77078970278

def insert_person(person_name, person_phone):
    """Inserts a new person into the Numbers table if not exists."""

    if len(person_phone) != 11:
        raise ValueError("person_phone must be 11 digits long.")
    if not person_phone.isdigit():
        raise ValueError("person_phone must contain only digits.")

    insert_sql = """
        INSERT INTO Numbers (person_name, person_phone)
        VALUES (%s, %s)
        RETURNING person_id;
    """

    check_sql = """
        SELECT person_name, person_phone
        FROM Numbers
        WHERE person_name = %s OR person_phone = %s;
    """

    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:

                # check if person already exists
                cur.execute(check_sql, (person_name, person_phone))
                existing = cur.fetchall()

                if existing:
                    for record in existing:
                        existing_name, existing_phone = record
                        if person_name == existing_name and person_phone == existing_phone:
                            print("Person with this name and phone already exists.")
                            return False
                        elif person_name == existing_name:
                            update.update_phone(person_name, person_phone)
                            print("Phone number updated for existing name.")
                            return True
                        elif person_phone == existing_phone:
                            update.update_name(person_name, person_phone)
                            print("Name updated for existing phone.")
                            return True

                # insert new person
                cur.execute(insert_sql, (person_name, person_phone))
                new_id = cur.fetchone()[0]
                conn.commit()
                print(f"Data recorded successfully with ID: {new_id}")
                return True

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Database error: {error}")
        return False

def insert_many_persons(person_list):
    """ Insert multiple persons into the numbers table """
    
    sql = "INSERT INTO numbers(person_name, person_phone) VALUES (%s, %s) RETURNING *"
    config = load_config()
    
    try:
        # Validate all phone numbers first
        for name, phone in person_list:
            if len(phone) != 11:
                print(f"{name}'s phone number must be 11 digits long.")
                continue
            elif not phone.isdigit():
                print(f"{name}'s phone number must contain only digits.")
                continue
            else:
                insert_person(name, phone)
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
    name = str(input("Enter name: "))
    phone = input("Enter phone: ")

    insert_person(name, phone)


    