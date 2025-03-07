import MySQLdb

try:
    # First connect without specifying the database
    database = MySQLdb.connect(
        host="localhost",
        user="root",
        passwd="524123"
    )
    
    cursor = database.cursor()
    
    # Create database if it doesn't exist
    cursor.execute("CREATE DATABASE IF NOT EXISTS dcrm")
    print("Database created successfully!")
    
    # Close the initial connection
    cursor.close()
    database.close()
    
    # Reconnect with the database specified
    database = MySQLdb.connect(
        host="localhost",
        user="root",
        passwd="524123",
        db="dcrm"
    )
    print("Connected to database successfully!")
    
except MySQLdb.Error as e:
    print(f"Error connecting to MySQL: {e}")
finally:
    if 'database' in locals():
        database.close()


