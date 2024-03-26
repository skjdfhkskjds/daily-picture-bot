import sqlite3


class DbGateway:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = None

    def create_connection(self) -> bool:
        """ create a db connection to SQLite database """
        if self.is_connected():
            return False
        try:
            self.conn = sqlite3.connect(self.db_path)
            return True
        except sqlite3.Error as e:
            print(e)
        return False

    def close_connection(self) -> bool:
        if self.is_connected():
            self.conn.close()
            self.conn = None
            return True
        return False

    def is_connected(self) -> bool:
        return self.conn is not None


class ImgGateway(DbGateway):
    def create_table(self) -> bool:
        """ create a table (if not exists) for storing image hashes """
        if not self.is_connected():
            return False
        try:
            c = self.conn.cursor()
            c.execute(
                '''CREATE TABLE IF NOT EXISTS images (hash TEXT UNIQUE)''')
            return True
        except sqlite3.Error as e:
            print(e)
        return False

    def insert_hash(self, image_hash) -> bool:
        """ insert image hash into the images table """
        if not self.is_connected():
            return False
        sql = ''' INSERT OR IGNORE INTO images(hash) VALUES(?) '''
        try:
            cur = self.conn.cursor()
            cur.execute(sql, (image_hash,))
            self.conn.commit()
            print(cur.lastrowid)
            return True
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            # self.conn.rollback()
            return False

    def check_hash_exists(self, image_hash) -> bool:
        """ check if image hash exists in the db """
        if not self.is_connected():
            return False
        cur = self.conn.cursor()
        cur.execute("SELECT 1 FROM images WHERE hash=?", (image_hash,))
        return cur.fetchone() is not None

