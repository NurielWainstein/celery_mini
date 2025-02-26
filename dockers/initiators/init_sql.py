import psycopg2

from config import SQL_PORT, SQL_HOST_NAME, SQL_DBNAME, SQL_USER, SQL_PASSWORD

# Establishing the connection
conn = None
try:
    conn = psycopg2.connect(
        dbname=SQL_DBNAME, user=SQL_USER, password=SQL_PASSWORD, host=SQL_HOST_NAME, port=SQL_PORT
    )
    cursor = conn.cursor()

    # SQL statement to create the "categories" table
    create_categories_table_query = '''
    CREATE TABLE IF NOT EXISTS categories (
        name TEXT PRIMARY KEY,
        region TEXT NOT NULL,
        type TEXT NOT NULL,
        count INTEGER NOT NULL
    );
    '''

    # Execute the queries
    cursor.execute(create_categories_table_query)

    # Commit the transactions
    conn.commit()

    print("Tables created successfully.")

except Exception as error:
    print(f"Error connecting to PostgreSQL: {error}")
finally:
    # Closing the cursor and connection
    if conn:
        cursor.close()
        conn.close()
