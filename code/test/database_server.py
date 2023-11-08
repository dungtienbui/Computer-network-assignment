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

# DB_PATH = None

# current_directory = os.path.dirname(__file__)
# os.chdir(current_directory)

# def set_server_db_path(new_path):
#     global DB_PATH
#     DB_PATH = new_path

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
    
    def get_all_file_of_host(self, hostname):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM file_table WHERE hostname = ?", (hostname,))
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
    def get_lname_of_host(self, fname, hostname):
        cursor = self.conn.cursor()
        cursor.execute("SELECT lname FROM file_table WHERE fname = ? AND hostname = ?", (fname, hostname,))
        return cursor.fetchall()
    def close(self):
        self.conn.close()
    
if __name__ == "__main__":
    # set_server_db_path("server_db")
    db = Database('test.db')
    
    # db.insert_host('dung', '1234', '1.1.1.1')
    # db.insert_host('dung1', '1234a', '1.1.1.2')
    # db.insert_host('dung2', '1234b', '1.1.1.3')
    # db.insert_host('dung3', '1234c', '1.1.1.4')
    # db.insert_file('a.pdf', '/us/a.pdf', 'dung')
    # db.insert_file('b.pdf', '/us/b.pdf', 'dung')
    # db.insert_file('c.pdf', '/us/c.pdf', 'dung1')
    # db.insert_file('a.pdf', '/us/d.pdf', 'dung2')
    # db.insert_file('a.pdf', '/us/e.pdf', 'dung3')
    # db.insert_file('c.pdf', '/us/f.pdf', 'dung3')
    # db.insert_file('g.pdf', '/us/a.pdf', 'dung')
    # db.insert_file('d.pdf', '/us/b.pdf', 'dung')
    # db.insert_file('e.pdf', '/us/c.pdf', 'dung1')
    # db.insert_file('f.pdf', '/us/d.pdf', 'dung2')
    # db.insert_file('g.pdf', '/us/e.pdf', 'dung3')
    # db.insert_file('j.pdf', '/us/f.pdf', 'dung3')
        
    #     db.insert_file('f.pdf', '/us/f.pdf', 'dung5')
        
    #     host_data = db.get_allData_host_table()
    #     for x in host_data:
    #         print(x)
        
    #     print('-----------------------------------')
    #     file_data = db.get_allData_file_table()
    #     for x in file_data:
    #         print(x)
            
    #     print('-----------------------------------')
    #     file_find = db.search_file('c.pdf')
    #     for x in file_find:
    #         print(x)
            
    #     print('-----------------------------------')
    #     allFileOfHost = db.get_all_file_of_host('dung3')
    #     for x in allFileOfHost:
    #         print(x)
            
    #     db.delete_file_of_host('a.pdf', 'dung3')
    #     db.delete_host('dung1')
        
    #     print('-----------------------------------')
    #     file_data = db.get_allData_file_table()
    #     for x in file_data:
    #         print(x)
            
    # print('-----------------------------------')      
    # host_data = db.get_allData_host_table()
    # for x in host_data:
    #     print(x)
    
    # db.rename_fname_of_host('a.pdf', 'dung2', 'newname')
    
    print('-----------------------------------')      
    host_data = db.get_allData_file_table()
    for x in host_data:
        print(x)
        
    print('-----------------------------------')
    hostname_find = db.get_lname_of_host('a.pdf', 'dung')
    if hostname_find == []:
        print("Not find")
    else:
        print(hostname_find[0][0])

    # print('-----------------------------------')
    # for x in file_find:
    #     print(x)
    #     y = x[0]
    #     if y == "dung1":
    #         print("ok")
    db.close()
