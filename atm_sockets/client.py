#! python3
import datetime
import sys
import socket
import time
import json
from prettytable import PrettyTable


class Client():
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
        print('Client started')
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = '127.0.0.1'
        self.server_port = 9999
        self.simulation_sleep_time = 3
        self.client_type = 0

    def show_options(self):
        self.menu_options = {'101': 'Select * view table',
                             '102': 'Select by id view one row',
                             '103': 'Delete by id delete one row',
                             '104': 'Update by id update one row',
                             '105': 'Insert a row',
                             '106': 'Commit changes',
                             '107': 'Rollback ',
                             '100': 'Exit',
                             '200': 'Deposit',
                             '201': 'Withdrawal'
                             }

        for key in self.menu_options:
            print(f'\n{key} is msg code for {self.menu_options[key]}')
        print('\n')

    def is_not_included_in_options(self, msg):
        return not msg in self.menu_options

    def connect_with_server_user(self):
        input_msg = 'Enter your command: '

        self.socket.connect((self.server_address, self.server_port))

        while True:
            out_msg = input(input_msg)

            input_msg = self.handle_client_msg(out_msg)

    def send_prints(self,msg):
        print(f'Your message: {msg}')
        print('Message sent \t time: ' + str(datetime.datetime.now().time()))
        self.socket.sendall(msg.encode('utf-8'))

    def clean_data(self,data):
        # cleaning data
        data = data.replace(" ", "")
        data = data.replace('[', '')
        data = data.split('],')
        data = [s.replace(']', '').split(',') for s in data]
        return data

    def print_received_table(self,data):
        x = PrettyTable()
        x.field_names = ["ID", "BALANCE", "DAILY_BALANCE"]
        for user in data:
            x.add_row(user)
        print(x)

    def print_received_msg(self,data):
        print('reply received \t time: ' + str(datetime.datetime.now().time()))
        print(data)

    def check_if_50s_and_20s(self,value):
        """
        Checking if value can be expressed as a sum of 50s and 20s
        :param value:
        :return: 0 if it can or 1 if it cant
        """
        if (value%50)%20!=0:
            return 1
        else:
            return 0
        

    def handle_client_msg(self, msg):
        """
        Gets and handles clients request
        Returns a string that is the msg prompt
        params:
            request:string
        """
        command = msg.split()
        code = int(command[0])
        input_msg = 'Enter your command: '

        #if self.is_not_included_in_options(command):
        #    input_msg = '(failure on last attempt)--Enter your command: '
        if code == client.EXIT:
            self.send_prints(msg)
            time.sleep(1)
            self.socket.close()
            sys.exit()
        elif code == client.SELECT_ALL:
            #send info
            self.send_prints(msg)
            data = self.socket.recv(1024).decode('utf-8')
            data = self.clean_data(data)
            #printing
            self.print_received_table(data)

        elif code == client.SELECT_ONE:
            #send info
            self.send_prints(msg)
            data = self.socket.recv(1024).decode('utf-8')
            data = self.clean_data(data)
            # printing
            self.print_received_table(data)

        elif code == client.DEPOSIT:
            code,id,value = command
            if int(value) <= 0 :
                print("Deposit should not be negative!")
            elif int(value) % 5 != 0:
                print("Deposit should  be multiple of 5!")
            else:
                self.send_prints(msg)
                data = self.socket.recv(1024).decode('utf-8')
                self.print_received_msg(data)

        elif code == client.WITHDRAWAL:
            code, id, value = command
            if int(value) <= 0 :
                print("withdrawal should not be negative!")
            elif self.check_if_50s_and_20s( int(value)):
                print("ATM returns only 50s and 20s")
            else:
                self.send_prints(msg)
                data = self.socket.recv(1024).decode('utf-8')
                self.print_received_msg(data)

        else:
            # send info
            self.send_prints(msg)
            data = self.socket.recv(1024).decode('utf-8')
            self.print_received_msg(data)
        return input_msg



if __name__ == "__main__":
    client = Client()
    client.show_options()

    if len(sys.argv) == 1:
        client.connect_with_server_user()
