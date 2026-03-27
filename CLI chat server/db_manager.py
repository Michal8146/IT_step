import sqlite3
from datetime import datetime


class DBManager:
    def __init__(self, db_path: str = "chat.db", dev_mode: bool = False):
        self.db_path = db_path
        self.dev_mode = dev_mode
        self._initialize_database()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def _table_exists(self, conn: sqlite3.Connection, table_name: str) -> bool:
        row = conn.execute(
            "SELECT 1 FROM sqlite_master WHERE type='table' AND name=? LIMIT 1;",
            (table_name,),
        ).fetchone()
        return row is not None

    def _initialize_database(self) -> None:
        with self._get_connection() as conn:
            users_exists = self._table_exists(conn, "users")
            rooms_exists = self._table_exists(conn, "rooms")
            messages_exists = self._table_exists(conn, "messages")

            if not (users_exists and rooms_exists and messages_exists):
                self._create_tables(conn)

                if self.dev_mode:
                    self._seed_dev_data(conn)

    def _create_tables(self, conn: sqlite3.Connection) -> None:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS rooms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        );

        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            time TEXT NOT NULL,
            sender_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            room_id INTEGER NOT NULL,
            FOREIGN KEY (sender_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (room_id) REFERENCES rooms(id) ON DELETE CASCADE
        );
        """)
        conn.commit()

    def _seed_dev_data(self, conn: sqlite3.Connection) -> None:
        users = [
            ("alice", "alice123"),
            ("bob", "bob123"),
            ("admin", "admin123"),
        ]
        rooms = [
            ("general",),
            ("python",),
            ("random",),
        ]

        conn.executemany(
            "INSERT OR IGNORE INTO users (login, password) VALUES (?, ?);",
            users
        )
        conn.executemany(
            "INSERT OR IGNORE INTO rooms (name) VALUES (?);",
            rooms
        )

        user_id = dict(conn.execute("SELECT login, id FROM users;").fetchall())
        room_id = dict(conn.execute("SELECT name, id FROM rooms;").fetchall())

        now = datetime.now().isoformat(timespec="seconds")

        messages = [
            (now, user_id["alice"], "Ahojte! Toto je testovacia správa 😊", room_id["general"]),
            (now, user_id["bob"], "Čaute, kto dnes rieši Python?", room_id["python"]),
        ]

        conn.executemany(
            "INSERT INTO messages (time, sender_id, content, room_id) VALUES (?, ?, ?, ?);",
            messages
        )

        conn.commit()

    def execute(self, query: str, params: tuple = ()):
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute(query, params)
            conn.commit()
            return cur

    def fetchall(self, query: str, params: tuple = ()):
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute(query, params)
            return cur.fetchall()

    def fetchone(self, query: str, params: tuple = ()):
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute(query, params)
            return cur.fetchone()
