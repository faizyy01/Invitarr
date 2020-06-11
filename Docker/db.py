import sqlite3

DB_URL = '/root/config/plex.db'

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("Connected to db")
    except Error as e:
        print("error in connecting to db")
    finally:
        if conn:
            return conn

def checkTableExists(dbcon, tablename):
    dbcur = dbcon.cursor()
    dbcur.execute("""SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='{0}';""".format(tablename.replace('\'', '\'\'')))
    if dbcur.fetchone()[0] == 1:
        dbcur.close()
        return True
    dbcur.close()
    return False

conn = create_connection(DB_URL)

# Checking if table exists
if checkTableExists(conn, 'USERS'):
	print('Table exists.')
else:
    conn.execute('''
    CREATE TABLE "USERS" (
    "id"	INTEGER NOT NULL UNIQUE,
    "discord_username"	TEXT NOT NULL UNIQUE,
    "email"	TEXT NOT NULL,
    PRIMARY KEY("id" AUTOINCREMENT)
    );
    ''')

def save_user(username, email):
    if username and email:
        conn.execute("INSERT INTO USERS (discord_username, email) VALUES ('"+ username +"', '" + email +  "')");
        conn.commit()
        print("User added to db.")
    else:
        return "Username or email cannot be empty"

def get_useremail(username):
    if username:
        try:
            cursor = conn.execute('SELECT discord_username, email from USERS where discord_username="{}";'.format(username))
            for row in cursor:
                email = row[1]
            if email:
                return email
            else:
                return "No users found"
        except:
            return "error in fetching from db"
    else:
        return "username cannot be empty"

def delete_user(username):
    if username:
        try:
            conn.execute('DELETE from USERS where discord_username="{}";'.format(username))
            conn.commit()
            return True
        except:
            return False
    else:
        return "username cannot be empty"
