#! python3
import socket
import threading
import json
import time
import random
import datetime
import sys
import sqlite3
import time
from db_api import *


class Server(object):
    EXIT = 100
    SELECT_ALL = 101
    SELECT_ONE = 102
    DELETE_ONE = 103
    UPDATE_ONE = 104
    INSERT_ONE = 105
    COMMIT_CHANGES = 106
    ROLLBACK_DATABASE = 107
    DEPOSIT = 200
    WITHDRAWAL = 201
    def __init__(self):
        print("SERVER started")
        self.lock = threading.Lock()
        self.address = '127.0.0.1'
        self.port = 9999
        self.database = "C:/Users/Xhino/Desktop/kat_ex1/atm_db.db"
        #self.thread_reset = threading.Thread(target = self.reset)
        #self.thread_reset.start()


    def reset(self):
        while True:
            print('Daily_balance set to ZERO')
            conn = create_connection(self.database)
            daily_to_zero(conn)
            commit_changes(conn)
            conn.close()
            time.sleep(60)


    def handle_client(self, connection):
        """
        Gets the client's message via conncetion socket
        and handles it (calls the proper function).
        params:
        connection: socket
        """
        conn = create_connection(self.database)
        out_msg = ""
        while True:
            try:
                in_msg = connection.recv(1024).decode('utf-8')
                time = str(datetime.datetime.now().time())
                print(f'received msg : {in_msg} \t time: {time}')

                code = int(in_msg[:3])

                if code == Server.EXIT :
                    conn.close()
                    out_msg = "Exiting..."
                    connection.close()

                elif code == Server.SELECT_ALL :
                    out_msg = select_all_users(conn)

                elif code == Server.SELECT_ONE :
                    code,id = in_msg.split()
                    out_msg=select_user(conn,id)

                elif code == Server.DELETE_ONE :
                    code, id = in_msg.split()
                    delete_user(conn, id)
                    out_msg = "User deleted"

                elif code == Server.UPDATE_ONE :
                    code,id,balance,daily = in_msg.split()
                    user = (id,balance,daily)
                    update_user(conn, user)
                    out_msg = "User updated"

                elif code == Server.INSERT_ONE:
                    code, id, balance, daily = in_msg.split()
                    user = (id, balance, daily)
                    insert_user(conn, user)
                    out_msg = "User inserted"

                elif code == Server.COMMIT_CHANGES:
                    commit_changes(conn)
                    out_msg = "changes commited"

                elif code == Server.ROLLBACK_DATABASE:
                    rollback(conn)
                    out_msg = "changes rolled back"

                elif code == Server.DEPOSIT:
                    code, id, value = in_msg.split()
                    dep = (int(value),int(id))
                    deposit(conn,dep)
                    out_msg = "deposit completed"

                elif code == Server.WITHDRAWAL:
                    code, id, value = in_msg.split()
                    wit = (id, value)
                    out_msg = withdrawal(conn, wit)

                else:
                    out_msg = "error code"
            except:
                print("error")
                
                connection.close()
            commit_changes(conn)    # commits changes
            connection.sendall(out_msg.encode('utf-8'))


    def start_listening(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connection_sock:
            # socket.SO_REUSEADDR--> if in TIME_WAIT then you can reuse the port
            connection_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            connection_sock.bind((self.address, self.port))
            connection_sock.listen(5)  # max queue 5

            while True:
                connection, address = connection_sock.accept()
                print(f'Connection opened for {address}')
                threading.Thread(
                    target=self.handle_client,
                    args=(connection,)).start()

if __name__ == "__main__":
    SERVER = Server()
    SERVER.start_listening()
