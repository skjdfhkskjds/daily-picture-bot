import sqlite3


def create_connection(db_file):
    """ create a db connection to SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn


def create_table(conn):
    """ create a table (if not exists) for storing image hashes """
    try:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS images (hash TEXT UNIQUE)''')
    except sqlite3.Error as e:
        print(e)


def insert_hash(conn, image_hash):
    """ insert image hash into the images table """
    sql = ''' INSERT OR IGNORE INTO images(hash) VALUES(?) '''
    cur = conn.cursor()
    cur.execute(sql, (image_hash,))
    conn.commit()
    return cur.lastrowid


def check_hash_exists(conn, image_hash):
    """ check if image hash exists in the db """
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM images WHERE hash=?", (image_hash,))
    return cur.fetchone() is not None
