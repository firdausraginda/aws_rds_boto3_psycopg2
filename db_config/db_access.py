from configparser import ConfigParser
import psycopg2
import os
import sys

db_config_file = os.path.join(os.path.dirname(__file__), '../database.ini')


def get_db_config(filename=db_config_file, section='postgresql'):
    """retrieve db configuration from database.ini file"""

    # create parser
    parser = ConfigParser()

    # read config file
    parser.read(filename)

    # initialize db dictionary
    db_config_items = {}

    # retrieve db config items
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db_config_items[param[0]] = param[1]
    else:
        raise Exception(
            'Section {0} not found in the {1}', format(section, filename))
        sys.exit(1)

    return db_config_items


def connect_to_db_rds():
    """connect to DB RDS"""

    try:
        # retrieve db config from database.ini file
        db_config_items = get_db_config()

        # connect to DB using db config in params
        connection = psycopg2.connect(**db_config_items)

    except Exception as err:
        raise err
        sys.exit(1)

    else:
        print('successfully connect to DB RDS')

    # initialize the cursor
    cursor = connection.cursor()

    return cursor, connection


def create_table():
    """create table users & products"""
    
    # build connection to db
    db_cursor, db_connection = connect_to_db_rds()

    # provide sql statements
    commands = (
        '''
        CREATE TABLE IF NOT EXISTS users (
            id VARCHAR PRIMARY KEY,
            name VARCHAR NOT NULL,
            phone VARCHAR NOT NULL
        );
        ''',
        '''
        CREATE TABLE IF NOT EXISTS products (
            id VARCHAR PRIMARY KEY,
            name VARCHAR NOT NULL,
            price BIGINT NOT NULL
        );
        ''',
        '''
        CREATE TABLE IF NOT EXISTS orders (
            id VARCHAR PRIMARY KEY,
            product_id VARCHAR REFERENCES products(id) ON DELETE CASCADE,
            user_id VARCHAR REFERENCES users(id) ON DELETE CASCADE,
            quantity INTEGER NOT NULL
        )
        '''
    )

    try:
        # execute sql commands
        for command in commands:
            db_cursor.execute(command)

        # commit changes
        db_connection.commit()

        # close connection
        db_cursor.close()
    
    except Exception as err:
        raise err
        sys.exit(1)
    
    else:
        print('successfully create table users, products, & orders')
    
    finally:
        # to close connection after build connection process
        if db_connection is not None:
            db_connection.close()

    return None


def insert_values():
    """insert values from sql files to table users & products"""
    
    # build connection to db
    db_cursor, db_connection = connect_to_db_rds()

    # set path to sql file
    path_to_insert_users_sql = os.path.join(
        os.path.dirname(__file__), './insert_users.sql')
    path_to_insert_products_sql = os.path.join(
        os.path.dirname(__file__), './insert_products.sql')
    path_to_insert_orders_sql = os.path.join(
        os.path.dirname(__file__), './insert_orders.sql')

    try:
        # execute command via SQL file
        db_cursor.execute(open(path_to_insert_users_sql, "r").read())
        db_cursor.execute(open(path_to_insert_products_sql, "r").read())
        db_cursor.execute(open(path_to_insert_orders_sql, "r").read())

        # commit changes
        db_connection.commit()

        # close connection
        db_cursor.close()

    except Exception as err:
        raise err
        sys.exit(1)

    else:
        print('successfully insert user, product, & order data')

    finally:
        
        # to close connection after build connection process
        if db_connection is not None:
            db_connection.close()
    
    return None


def get_data(table):
    """print data from table"""
    
    # build connection to db
    db_cursor, db_connection = connect_to_db_rds()

    try:
        # query data from table in func parameter
        db_cursor.execute(
            '''
            SELECT * FROM {} ;
            '''.format(table)
        )
        
        # fetch all query result and assign to query_results
        query_results = db_cursor.fetchall()

        # print every row data
        for query_result in query_results:
            print(query_result)
        
        # close connection
        db_cursor.close()

    except Exception as err:
        raise err
        sys.exit(1)

    else:
        print(f'successfully retrieve {table} data')

    finally:

        # to close connection after build connection process
        if db_connection is not None:
            db_connection.close()

    return None

if __name__ == '__main__':
    
    # build connection to db
    connect_to_db_rds()

    # create table
    create_table()

    # insert values
    insert_values()

    # print data users
    get_data('users')

    # print data products
    get_data('products')

    # print data orders
    get_data('orders')