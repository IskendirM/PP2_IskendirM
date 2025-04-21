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

def get_records_by_pattern(pattern):
            

            """ Fetch records based on a pattern """
            
            sql = """SELECT person_name, person_phone
                     FROM Numbers
                     WHERE person_name ILIKE %s OR person_phone ILIKE %s;"""
            
            config = load_config()
            records = []
            
            try:
                with psycopg2.connect(**config) as conn:
                    with conn.cursor() as cur:
                        cur.execute(sql, (f"%{pattern}%", f"%{pattern}%"))
                        records = cur.fetchall()
                        
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)
                
            finally:
                return records

def get_paginated_data(limit, offset):
    """ Fetch paginated data """
    config = load_config()
    
    sql = """SELECT person_name, person_phone
             FROM Numbers
             LIMIT %s OFFSET %s;"""
    
    with psycopg2.connect(**config) as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (limit, offset))
            records = cur.fetchall()
            return records
if __name__ == "__main__":
    # persons = get_persons()
    # for person in persons:
    #     print(person)
    
    # person_name = input("Enter the person's name to search: ")
    # numbers = get_numbers_by_name(person_name)
    # print(numbers) if numbers else print("No records found.")

    pattern = input("Enter a pattern to search (name or phone): ")
    records = get_records_by_pattern(pattern)
    if records:
        for record in records:
            print(record)
    else:
        print("No records found.")

    # limit is 10 which means 10 records will be fetched and offset is 1 which means it will skip the first record and fetch the next 10 records.
    limit = int(input("Enter the limit for pagination: "))
    offset = int(input("Enter the offset for pagination: "))
    
    print(get_paginated_data(limit, offset)) # Example usage of pagination where limit is 10 and offset is 1