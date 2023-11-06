#------------------------------
# database in server
# store: 
#       host: [hostname (primary)] [password] [IP_addr] []
#       file: [fname (primary)] [lname] [hostname (foreign)]
#------------------------------
import os
import sqlite3

#----------check db is exit----------------------
# input: absolute path
def isExit_database(db_file_path):
    return os.path.exists(db_file_path)

#-----------create a db-----------------
# input: absolute path
# return true => db not exit -> create a db successfully
# return false => db exit -> create a db unsuccessfully
def create_database(db_file_path):
    if isExit_database(db_file_path):
        return False
    else:
        con = sqlite3.connect(db_file_path)
        cur = con.cursor()
        cur.execute("CREATE TABLE host(hostname, passwork, IPAddr)")
        cur.execute("CREATE TABLE file(fname, lname, hostname)")
        cur.close()
        con.close()
        return True

def add_host(db_file_path, hostname, password, IP_addr):
    if isExit_database(db_file_path):
        con = sqlite3.connect(db_file_path)
        cur = con.cursor()
        data = [hostname, password, IP_addr]
        cur.execute("INSERT INTO movie VALUES(?, ?, ?)", data)
        con.commit()
        con.close()
        return True
    else:
        return False
    
def search_host(c):
    x = 0

if __name__ == "__main__":
    x = 0