import socket
import threading
from datetime import datetime

from config import HOST, PORT, MAIN_DB_PATH
from utils import authenticate_user, user_choose_room
from db_manager import DBManager

rooms = {}


def broadcast(message, room, client_socket):
    for client in rooms[room]:
        if client != client_socket:
            try:
                client.send(message)
            except:
                client.close()
                rooms[room].remove(client)


def handle_client(client_socket, db_manager):
    user = authenticate_user(client_socket, db_manager)

    if user is None:
        client_socket.send(b"Spatne prihlasovaci udaje.")
        client_socket.close()
        return

    user_id, login = user
    print(f"Prihlasil se {login}")

    room = user_choose_room(client_socket, db_manager)

    if room not in rooms:
        rooms[room] = []

    rooms[room].append(client_socket)
    print(f"{login} vstoupil do mistnosti {room}")

    # Zjistíme room_id
    room_row = db_manager.fetchone(
        "SELECT id FROM rooms WHERE name=?;",
        (room,)
    )
    room_id = room_row[0]

    while True:
        try:
            message = client_socket.recv(1024)

            if not message:
                break

            text = message.decode("utf-8")

            now = datetime.now().isoformat(timespec="seconds")

            db_manager.execute(
                "INSERT INTO messages (time, sender_id, content, room_id) "
                "VALUES (?, ?, ?, ?);",
                (now, user_id, text, room_id)
            )

            formatted = f"{login}: {text}".encode()
            broadcast(formatted, room, client_socket)

        except:
            break

    client_socket.close()
    rooms[room].remove(client_socket)

    if not rooms[room]:
        del rooms[room]


def main():
    db_manager = DBManager(MAIN_DB_PATH, dev_mode=True)
    print("Databaze inicializovana.")

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)

    print("Server bezi...")

    while True:
        client_socket, addr = server.accept()
        print(f"{addr} se pripojil.")

        client_thread = threading.Thread(
            target=handle_client,
            args=(client_socket, db_manager)
        )
        client_thread.start()


if __name__ == "__main__":
    main()
