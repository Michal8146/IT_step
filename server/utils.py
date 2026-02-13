def authenticate_user(client, db_manager):
    while True:
        client.send("Zadej login:password\n".encode())

        try:
            data = client.recv(1024).decode("utf-8").strip()
            login, password = data.split(":")
        except:
            client.send("Spatny format. Pouzij login:password\n".encode())
            continue

        user = db_manager.fetchone(
            "SELECT id, login FROM users WHERE login=? AND password=?;",
            (login.strip(), password.strip())
        )

        if user:
            client.send("Prihlaseni uspesne.\n".encode())
            return user

        client.send("Spatne prihlasovaci udaje. Zkus to znovu.\n".encode())


def db_get_rooms(db_manager):
    rows = db_manager.fetchall("SELECT name FROM rooms;")
    return [row[0] for row in rows]


def user_choose_room(client, db_manager):
    rooms = db_get_rooms(db_manager)

    client.send("Vyber mistnost:\n".encode())

    while True:
        client.send((", ".join(rooms) + "\n").encode())
        room = client.recv(1024).decode("utf-8").strip()

        if room in rooms:
            return room

        client.send("Neplatna mistnost.\n".encode())
