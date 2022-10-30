import mysql.connector


class Database:
    def __init__(self, DB_HOST, DB_USER, DB_PASSWORD, DB_NAME):
        self.host = DB_HOST
        self.name = DB_NAME
        self.user = DB_USER
        self.password = DB_PASSWORD
        self.conn = mysql.connector.connect(host=self.host, user=self.user, password=self.password, db =self.name)
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTO_INCREMENT, user_name text, email text, password text, comment_text text, hashtags text, is_loggedin text, total_comments text)")
        self.conn.commit()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS user_comment_count (id INTEGER PRIMARY KEY AUTO_INCREMENT, user_name text, date_var text, comment_count text)")
        self.conn.commit()

    def createUser(self, userName, email, password, comment, hashtags):
        self.cur.execute(
            f"INSERT INTO users VALUES(NULL, '{userName}', '{email}', '{password}', '{comment}', '{hashtags}', '0', '0')"
        )
        self.conn.commit()

    def fetch(self):
        self.cur.execute("SELECT * FROM users")
        rows = self.cur.fetchall()
        return rows

    def remove(self, id):
        self.cur.execute(f"DELETE FROM users WHERE id={id}")
        self.conn.commit()

db = Database(
        "database-twi.c5wuc1hsxwv9.ap-southeast-1.rds.amazonaws.com", 
        "admin", 
        "qfmrAnuJgzeLRw6", 
        "twitter_bot"
    )