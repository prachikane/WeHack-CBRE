import sqlite3

def send_sql_query(query):
    print("Sending SQL query:", query)
    # Connect to the SQLite database
    conn = sqlite3.connect('fake_database.db')

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # Example SQL query
    #vendors, invoice, assets
    #sql_query = "SELECT * FROM vendors;"

    # Execute the query
    cursor.execute(query)

    column_names = [description[0] for description in cursor.description]

    # Fetch the results, if any
    results = cursor.fetchall()

    print(results)

    # Don't forget to close the connection when done
    conn.close()
    return results,column_names