import pymysql

def check_mysql_server(config):
    """Check if the MySQL server is running and accessible."""
    try:
        # Attempt to connect to the MySQL server
        conn = pymysql.connect(**config)
        conn.close()
        print("MySQL server is up and running!")
    except pymysql.MySQLError as e:
        print(f"Error connecting to MySQL server: {e}")

# MySQL server connection details
db_config = {
    'host': '122.176.146.28',
    'user': 'mysql',
    'password': 'Samepassword1!',
    'database': 'vizlabs',  # You can leave this out if just testing the connection
    'port': 3306  # MySQL default port
}

if __name__ == "__main__":
    check_mysql_server(db_config)
