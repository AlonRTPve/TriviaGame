import sqlite3, bcrypt


def connect_to_database():
    conn = sqlite3.connect('trivia_database.db')
    c = conn.cursor()
    return c, conn



#c.execute("""CREATE TABLE users (
#            username text,
#            password text,
#            score integer
#            )""")
#conn.commit()
#conn.close()


def check_if_user_exists(username):
    c, conn = connect_to_database()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    if c.fetchall():
        return True #returns false if user doesnt exists
    return False


def register(username, password):
    c, conn = connect_to_database()
    if not check_if_user_exists(username):
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        c.execute("INSERT INTO users VALUES(?, ?, ?) ", (username, hashed_password, 0))
        conn.commit()
        conn.close()
        return True
    else:
        print("user already exists")
        return False


def login(username, password):
    c, conn = connect_to_database()
    c.execute("SELECT password FROM users WHERE username=?", (username,))
    data = c.fetchone()[0]
    conn.close()
    print(bcrypt.checkpw(password.encode("utf-8"), data))
    return bcrypt.checkpw(password.encode("utf-8"), data)

def update_score(username):
    c, conn = connect_to_database()
    c.execute("SELECT score FROM users WHERE username=?", (username,))
    score = c.fetchone()[0]
    score +=5
    c.execute("UPDATE users SET score = ? WHERE username = ?", (score, username))
    conn.commit()

def get_score(username):
    c, conn = connect_to_database()
    c.execute("SELECT score FROM users WHERE username=?", (username,))
    score = c.fetchone()[0]
    return score



def get_high_score():
    c, conn = connect_to_database()
    c.execute("SELECT username,score FROM users")
    d = c.fetchall()
    return d


