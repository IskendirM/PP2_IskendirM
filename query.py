import psycopg2
from config import load_config

def get_persons():
    """ Fetch all persons from the numbers table """
    
    sql = """SELECT person_name, person_phone
             FROM Numbers;"""
    
    config = load_config()
    persons = []
    
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                persons = cur.fetchall()
                
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        
    finally:
        return persons

def get_numbers_by_name(person_name):
    """ Fetch numbers by person name """
    
    sql = """SELECT person_name, person_phone
             FROM Numbers
             WHERE person_name = %s;"""
    
    config = load_config()
    persons = []
    
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (person_name,))
                persons = cur.fetchall()
                
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        
    finally:
        return persons
    

if __name__ == "__main__":
    persons = get_persons()
    for person in persons:
        print(person)
    
    person_name = input("Enter the person's name to search: ")
    numbers = get_numbers_by_name(person_name)
    print(numbers) if numbers else print("No records found.")