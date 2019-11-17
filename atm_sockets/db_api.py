import sqlite3
import json
LIMIT = 800

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return None

def select_all_users(conn):
    """
    Query all rows in the User table
    :param conn: the Connection object
    :return: str: json from the table
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM User")
    rows = cur.fetchall()
    # creating a json
    table_json = json.dumps(rows)
    return table_json

def select_user(conn,id):
    """
    Query all rows in the User table
    :param conn: the Connection object
    :param id: User's id that we want to be selected
    :return: str: json of a user's table row
    """
    cur = conn.cursor()
    sql = '''SELECT * FROM User WHERE id=?'''
    cur.execute(sql,(id,))
    row = cur.fetchall()
    row_json = json.dumps(row)
    return row_json

def insert_user(conn,user):
    """
    Create a new user into the User table
    :param conn:
    :param user: a tuple (id,balance,daily_balance)
    :return: user's id
    """
    sql = ''' INSERT INTO User VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql,user)
    return cur.lastrowid

def delete_user(conn,id):
    """
    Delete a rows in the User table
    :param conn: Connection to the SQLite database
    :param id: User's id that we want to be deleted
    :return:
    """
    sql = '''DELETE FROM User WHERE id=?'''
    cur = conn.cursor()
    str1=cur.execute(sql,(id,))

def update_user(conn, user):
    """
    update id, balance, and daily_balance of user
    :param conn:
    :param user: a tuple (id,balance,daily_balance)
    :return: user id
    """
    user = (user[1],user[2],user[0])
    sql = ''' UPDATE User
              SET balance = ? ,
                  daily_balance = ?
              WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, user)

def daily_to_zero(conn):
    sql = ''' UPDATE User
              SET daily_balance = 0'''
    cur = conn.cursor()
    cur.execute(sql)
    
    

def commit_changes(conn):
    conn.commit()

def rollback(conn):
    conn.rollback()

def deposit(conn,dep):
    """ update (increase) user's balance
    :param conn:
    :param dep : a  (y,x) tuple with x as id and y as deposit value
    """
    sql = ''' UPDATE User
              SET balance = balance + ? 
              WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, dep)



def withdrawal(conn,withd):
    """
    Decreases balance by value only if daily balance is bellow it's limit
    :param conn:
    :param withd: a (x,y) tuple with x as id and y as withdrawal value
    :return: str
    """

    sql = ''' Select balance,daily_balance
              From User 
              WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, (withd[0],))
    daily = cur.fetchall()
    if int(daily[0][1]) + int(withd[1]) <= LIMIT and int(daily[0][0]) - int(withd[1]) >=0 :
        sql = ''' UPDATE User
                  SET daily_balance = daily_balance + ? ,
                  balance = balance - ?
                  WHERE id = ?'''
        cur = conn.cursor()
        cur.execute(sql, (int(withd[1]),int(withd[1]),withd[0]))
        return "withdrawal completed"
    else:
        return "You cant withdrawal check daily LIMIT or your balance"

def main():
    database = "C:/Users/Xhino/Desktop/katanemimenos/ex_1/atm_db.db"
    # create a database connection
    conn = create_connection(database)
    with conn:
        select_all_users(conn)
