import socket
import chatlib  # To use chatlib functions or consts, use chatlib.****

SERVER_IP = "127.0.0.1"  # Our server will run on same computer as client
SERVER_PORT = 5678

# HELPER SOCKET METHODS

def build_and_send_message(conn, code, data):
    """
    Builds a new message using chatlib, wanted code and message.
    Prints debug info, then sends it to the given socket.
    Paramaters: conn (socket object), code (str), data (str)
    Returns: Nothing
    """
    # Implement Code
    datanew = chatlib.join_data(data)
    full_msg = chatlib.build_message(code, datanew)
    try:
        conn.send(full_msg.encode())
    except ConnectionAbortedError:
        message = "Server has closed the connection"
        exit(message)


def recv_message_and_parse(conn):
    """
    Recieves a new message from given socket,
    then parses the message using chatlib.
    Paramaters: conn (socket object)
    Returns: cmd (str) and data (str) of the received message.
    If error occured, will return None, None
    """
    # ..
    try:
        full_msg = conn.recv(1024).decode()
        cmd, data = chatlib.parse_message(full_msg)
        return cmd, data
    except Exception:
        return None, None

def connect():
    # Implement Code
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((SERVER_IP,SERVER_PORT))
        return client_socket
    except ConnectionRefusedError:
        message = "Server is not up yet."
        exit(message)


def error_and_exit(error_msg):
    print(error_msg)
    exit()


def build_send_recv_parse(conn, cmd, data):
    build_and_send_message(conn, cmd, data)
    return recv_message_and_parse(conn)


def get_score(conn): #ADD COMMANDS IN CHATLIB -
    cmd,data = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["GET_SCORE"], "")
    data = data.replace("#", "")
    return cmd, data

def get_highscore(conn):
    cmd, data = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["HIGHSCORE"], "")
    if data != None:
        message = data.replace("#", "")
        return cmd, message
    return cmd, data


def login(conn):
    while True:
        username = input("Please enter username: \n")
        password = input("Please enter password: \n")
        data = [username,password]
        build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["login_msg"],data)
        message = recv_message_and_parse(conn)
        if message == ('LOGIN_OK', ''):
            print("Logged in")
            return
        else:
            print("Wrong username or password")


def logout(conn):
    build_and_send_message(conn, chatlib.PROTOCOL_CLIENT["logout_msg"], "")
    print("Goodbye!")
    exit()


def play_question(conn):
    cmd, msg = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["GET_QUESTION"], "")
    if cmd == "YOUR_QUESTION":
        msg = chatlib.split_data(msg, 5)
        question_number, question, answer1, answer2, answer3, answer4 = msg[0], msg[1], msg[2], msg[3], msg[4], msg[5]
        print(f"Question number: {question_number} \n Question is: {question} \n ")
        print(f" Answer 1. {answer1} \n Answer 2. {answer2} \n Answer 3. {answer3} \n Answer 4. {answer4} \n")
        answer = input("What is your answer? ")  # all good till here
        cmd, msg = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["SEND_ANSWER"], [question_number, answer])
        if cmd == "CORRECT_ANSWER":
            msg = get_score(conn)
            print(f"Thats Correct! Your score is {msg[1]}")
        elif cmd == "WRONG_ANSWER":
            print("you got it wrong, try again next time.")
            print(f"The right answer was {msg}")
        else:
            print("no more questions")
            exit("no more questions")



def get_logged_users(conn):
    cmd, ANSWER = build_send_recv_parse(conn, chatlib.PROTOCOL_CLIENT["LOGGED"], "")
    return ANSWER



def main():
    client_socket = connect()
    login(client_socket)
    while True:
        user_input = input("What would you like to do?\n s   Get my score \n h   Get high score\n p   Play Question \n q   Quit\n l   get logged users\n" )
        if user_input == "s":
            cmd, data = get_score(client_socket)
            print(f"your score is: {data}")
            if cmd != "YOUR_SCORE":
                exit("Error")
        elif user_input == "h":
            cmd, data = get_highscore(client_socket)
            print(f"High-Score table:\n {data}")
        elif user_input == "q":
            logout(client_socket)
            print("Goodbye")
            break
        elif user_input == "p":
            play_question(client_socket)
        elif user_input == "l":
            answer = get_logged_users(client_socket)
            print(f"Logged users are:\n{answer}")
        else:
            print("Wrong choice")




if __name__ == '__main__':
    main()


