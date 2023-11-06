#----------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------
# database in server
# store: 
#       host_table: [hostname (primary)] [password] [IP_addr] []
#       file_table: [fname (primary)] [lname] [hostname (foreign)]
#----------------------------------------------------------------------------------------
import sqlite3

class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS host_table (
            hostname TEXT PRIMARY KEY NOT NULL,
            password TEXT,
            IP_addr TEXT
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS file_table (
            fname TEXT PRIMARY KEY NOT NULL,
            lname TEXT,
            hostname TEXT NOT NULL,
            FOREIGN KEY (hostname) REFERENCES host_table(hostname) ON DELETE CASCADE
        )
        """)
        self.conn.commit()

    def insert_host(self, hostname, password, IP_addr):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO host_table VALUES (?, ?, ?)", (hostname, password, IP_addr))
        self.conn.commit()
        
    def delete_host(self, hostname):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM host_table WHERE hostname = ?", (hostname,))
        self.conn.commit()
        
    def insert_file(self, fname, lname, hostname):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO file_table VALUES (?, ?, ?)", (fname, lname, hostname))
        self.conn.commit()
        
    def delete_file_on_host(self, fname, hostname):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM file_table WHERE fname = ? AND hostname = ?", (fname, hostname, ))
        self.conn.commit()
        
    def get_allData_host_table(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM host_table")
        return cursor.fetchall()
    
    def get_info_hostname(self, hostname):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM host_table WHERE hostname = ?", (hostname,))
        return cursor.fetchall()
    
    def search_file(self, fname):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM file_table WHERE fname = ?", (fname,))
        return cursor.fetchall()
    
    
    
    def close(self):
        self.conn.close()

if __name__ == "__main__":
    db = Database("mydatabase.db")
    db.close()
