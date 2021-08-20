# Python program to implement client side of chat room.
import socket
import select
import sys
from _thread import*

def generateKey(string, keyS):
    key = list(keyS)
    if len(string) == len(key):
        return(keyS)
    else:
        for i in range(len(string) - len(key)):
            key.append(key[i%len(key)])
        return("".join(key))

def encrypt(string,key):
    cipher_text = []
    for i in range (len(string)):
        if string[i]=="":
            cipher_text.append("")
        elif string[i].isalpha() == True:
            x = (ord(string[i]) + ord(key[i]))%26
            x +=ord('A')
            cipher_text.append(chr(x))
        else:
            cipher_text.append(string[i])
            return("".join(cipher_text))

def decrypt(cipher_text,key):
    orig_text = []
    for i in range(len(cipher_text)):
        if cipher_text[i] == "":
            orig_text.append("")
        elif cipher_text[i].isalpha() == True:
            x = (ord(cipher_text[i]) - ord(key[i]) + 26)%26
            x+=ord('A')
            orig_text.append(chr(x))
        else:
            orig_text.append(cipher_text[i])
    return("".join(orig_text))



server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if len(sys.argv) != 3:
    print ("Correct usage: script, IP address, port number")
    exit()
IP_address = str(sys.argv[1])
Port = int(sys.argv[2])
server.connect((IP_address, Port))

keyword="VELLORE"

while True: 

    # maintains a list of possible input streams
    sockets_list = [sys.stdin, server]

    """ There are two possible input situations. Either the
    user wants to give  manual input to send to other people,
    or the server is sending a message  to be printed on the
    screen. Select returns from sockets_list, the stream that
    is reader for input. So for example, if the server wants
    to send a message, then the if condition will hold true
    below.If the user wants to send a message, the else
    condition will evaluate as true"""
    read_sockets,write_socket, error_socket = select.select(sockets_list,[],[])

    for socks in read_sockets:
        if socks == server:
            message = socks.recv(2048)
            message=message.decode("utf-8")
            message = message.upper()
            key = generateKey(message,keyword)
            message = decrypt(message,key)
            print (message)
        else:
            message = sys.stdin.readline()
            message = message.upper()

            key = generateKey(message,keyword)
            message = encrypt(message,key)
            server.sendall(message.encode("utf-8"))

            message = decrypt(message,key)
            sys.stdout.write("<You>")
            sys.stdout.write(message)
            sys.stdout.flush()


server.close()
