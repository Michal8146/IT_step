import socket
import threading

HOST = "127.0.0.1"
PORT = 12346


def receive_messages(sock):
    while True:
        try:
            message = sock.recv(1024).decode("utf-8")
            if message:
                print(message)
        except:
            break


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    thread = threading.Thread(target=receive_messages, args=(client,))
    thread.start()

    while True:
        msg = input()
        client.send(msg.encode())


if __name__ == "__main__":
    main()
