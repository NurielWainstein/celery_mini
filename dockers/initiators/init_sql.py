import psycopg2

# Database connection parameters
host = "localhost"
port = "5432"
dbname = "celery_db"
user = "postgres"
password = "1234"

# Establishing the connection
try:
    conn = psycopg2.connect(
        dbname=dbname, user=user, password=password, host=host, port=port
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
