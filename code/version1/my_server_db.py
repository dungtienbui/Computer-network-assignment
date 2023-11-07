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
import os

# DB_NAME = None

# current_directory = os.path.dirname(__file__)
# os.chdir(current_directory)

# def set_server_db_name(name):
#     global DB_NAME
#     DB_NAME = name

class Database:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        self.conn.execute("PRAGMA foreign_keys = 1")
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS host_table (
            hostname TEXT PRIMARY KEY,
            password TEXT,
            IP_addr TEXT
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS file_table (
            fname TEXT NOT NULL,
            lname TEXT NOT NULL,
            hostname TEXT NOT NULL,
            PRIMARY KEY (fname, hostname)
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
        
    def delete_file_of_host(self, fname, hostname):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM file_table WHERE fname = ? AND hostname = ?", (fname, hostname, ))
        self.conn.commit()
        
    def rename_fname_of_host(self, fname, hostname, newname):
        cursor = self.conn.cursor()
        cursor.execute("UPDATE file_table SET fname = ? WHERE fname = ? AND hostname = ?", (newname, fname, hostname,))
        self.conn.commit()
    
    def get_allData_host_table(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM host_table")
        return cursor.fetchall()
    
    def get_allData_file_table(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM file_table")
        return cursor.fetchall()
    
    def get_info_hostname(self, hostname):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM host_table WHERE hostname = ?", (hostname,))
        return cursor.fetchall()
    
    def search_file(self, fname):
        cursor = self.conn.cursor()
        cursor.execute("SELECT file_table.hostname, host_table.IP_addr FROM file_table JOIN host_table ON file_table.hostname = host_table.hostname WHERE fname = ?", (fname,))
        return cursor.fetchall()
    
    def get_lname_of_host(self, fname, hostname):
        cursor = self.conn.cursor()
        cursor.execute("SELECT lname FROM file_table WHERE fname = ? AND hostname = ?", (fname, hostname,))
        return cursor.fetchall()
    
    def get_all_file_of_host(self, hostname):
        cursor = self.conn.cursor()
        cursor.execute("SELECT fname, lname FROM file_table WHERE hostname = ?", (hostname,))
        return cursor.fetchall()
    
    def get_hostname_byIP(self, IP_addr):
        cursor = self.conn.cursor()
        cursor.execute("SELECT hostname FROM host_table WHERE IP_addr = ?", (IP_addr,))
        return cursor.fetchall()
    
    def check_file_of_host(self, hostname, fname):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM file_table WHERE hostname = ? AND fname = ?", (hostname, fname))
        return cursor.fetchall()
    
    def get_ip_by_hostname(self, hostname):
        cursor = self.conn.cursor()
        cursor.execute("SELECT IP_addr FROM host_table WHERE hostname = ?", (hostname,))
        return cursor.fetchall()
    
    def close(self):
        self.conn.close()

# if __name__ == "__main__":
#     set_server_db_name("server_db")
#     db = Database(DB_NAME)
#     db.close()
