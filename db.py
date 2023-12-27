import sqlite3


class db:
    def __init__(self):
        # Инициализация базы данных
        self.conn = sqlite3.connect('messenger.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS chats (
                chat_id TEXT,
                username text,
                FOREIGN KEY (username) REFERENCES users (username)
            )
        ''')  # chat_id - 12,123,234...
        self.conn.commit()

    def new_chat(self):
        self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS chat (
                        sender TEXT,
                        chat_id TEXT,
                        messages text,
                        FOREIGN KEY (chat_id) REFERENCES chats(chat_id)
                    )
                ''')
        self.conn.commit()
        # query = "INSERT INTO chat (chat_id, messages) VALUES (?,?)"
        # self.cursor.execute(query, [1, "{'a': 123}"])
        # self.conn.commit()
        # query = "INSERT INTO chat (chat_id, messages) VALUES (?,?)"
        # self.cursor.execute(query, [2, "{'b': 123}"])
        # self.conn.commit()
        # query = "INSERT INTO chat (chat_id, messages) VALUES (?,?)"
        # self.cursor.execute(query, [3, "{'c': 123}"])
        # self.conn.commit()
        # query = "INSERT INTO chats (chat_id, username) VALUES (?,?)"
        # self.cursor.execute(query, ["1,2,3", "1"])
        # self.conn.commit()

    def get_all_chats(self, sender):
        ###
        print(sender)
        ###
        query = f"SELECT chat_id FROM chats WHERE username = ?"
        self.cursor.execute(query, (1,))
        ###
        print(self.cursor.rowcount)
        ###
        chats_data = self.cursor.fetchone()
        chats_id = []
        ###
        if chats_data == None:
            chats_data = [" , "]

        print(chats_data)
        ###
        for i in str(chats_data[0]).split(','):
            try:
                if i != None:
                    # print(i)
                    chats_id.append(int(i))
                else:
                    return None
            except:
                return {1: "qwerty"}
        texts = {}
        for i in chats_id:
            query = f"SELECT messages FROM chat WHERE chat_id = {i}"
            self.cursor.execute(query)
            texts[i] = self.cursor.fetchone()
        return texts

    def get_chat(self, chatId):
        print("!!!", chatId)
        query = f"SELECT * FROM chat WHERE chat_id = {chatId}"
        self.cursor.execute(query)
        chat_data = self.cursor.fetchall()
        print("chat_data",chat_data)
        return chat_data

    def select_user(self, user_id):
        query = f"SELECT * FROM users WHERE id = {user_id}"
        self.cursor.execute(query)
        user_data = self.cursor.fetchone()
        return user_data

    def insert_user(self, username, password):
        query = f"INSERT INTO users (username, password) VALUES ('{username}','{password}')"
        self.cursor.execute(query)
        self.conn.commit()
        query = "INSERT INTO chats (chat_id, username) VALUES (?,?)"
        self.cursor.execute(query, ["1,2,3", "1"])
        self.conn.commit()

    def get_user(self, username, password):
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        self.cursor.execute(query)
        user_data = self.cursor.fetchone()
        return user_data

    def insert_message(self, sender, content, timestamp, chatid):
        print("chatid", chatid)
        self.cursor.execute('INSERT INTO messages (sender, content, timestamp) VALUES (?, ?, ?)',
                            (sender, content, timestamp))
        self.conn.commit()
        self.cursor.execute(f'INSERT INTO chat (sender, chat_id,messages) VALUES (?,?, ?)',
                            (sender, chatid, content))
        self.conn.commit()
