import socket


def main_client():
    HOST = '127.0.0.1'
    PORT = 8000
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST,PORT))

    while True:
        cmd = input("Please input msg:") #input a filename of xml, e.g. 20210803141245_2119A000527.xml
        cmd = cmd.encode()
        s.send(cmd) # server will return json data back
        data = s.recv(6144)
        print("server send : %s " % (data.decode('utf-8')))
        
    
    s.close()



if __name__ == "__main__":
    main_client()