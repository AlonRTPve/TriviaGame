##############################################################################
# server.py
##############################################################################

import socket
import chatlib
import select
import random


# GLOBALS
users = {
			"test"		:	{"password":"test","score":0,"questions_asked":[]},
			"yossi"		:	{"password":"123","score":50,"questions_asked":[]},
			"master"	:	{"password":"master","score":200,"questions_asked":[]}
			}

questions = {
				2313 : {"question":"How much is 2+2","answers":["3","4","2","1"],"correct":2},
				4122 : {"question":"What is the capital of France?","answers":["Lion","Marseille","Paris","Montpellier"],"correct":3}

				}
logged_users = {} # a dictionary of client hostnames to usernames - will be used later
messages_to_send = []
client_sockets = []

ERROR_MSG = "Error! "
SERVER_PORT = 5678
SERVER_IP = "127.0.0.1"
MAX_MSG_LENGTH = 1024


# HELPER SOCKET METHODS



def build_and_send_message(conn, code, msg):
	global messages_to_send

	## copy from client
	# Implement Code
	datanew = chatlib.join_data(msg)
	full_msg = chatlib.build_message(code, datanew)
	messages_to_send += [conn, full_msg]
	#print(f"[SERVER] {full_msg}")
	#try:
		#conn.send(full_msg.encode())
	#except Exception:
	#	print("client has closed the connection")

def recv_message_and_parse(conn):
	## copy from client
	try:
		full_msg = conn.recv(1024).decode()
		print(f"[CLIENT] {full_msg}")
		cmd, data = chatlib.parse_message(full_msg)
		return cmd, data
	except Exception:
		print("hey")

	


# Data Loaders #

def load_questions():
	"""
	Loads questions bank from file	## FILE SUPPORT TO BE ADDED LATER
	Recieves: -
	Returns: questions dictionary
	"""
	questions = {
				2313 : {"question":"How much is 2+2","answers":["3","4","2","1"],"correct":2},
				4122 : {"question":"What is the capital of France?","answers":["Lion","Marseille","Paris","Montpellier"],"correct":3} 
				}
	
	return questions

def load_user_database():
	"""
	Loads users list from file	## FILE SUPPORT TO BE ADDED LATER
	Recieves: -
	Returns: user dictionary
	"""
	users = {
			"test"		:	{"password":"test","score":0,"questions_asked":[]},
			"yossi"		:	{"password":"123","score":50,"questions_asked":[]},
			"master"	:	{"password":"master","score":200,"questions_asked":[]}
			}
	return users

	
# SOCKET CREATOR

def setup_socket():
	"""
	Creates new listening socket and returns it
	Recieves: -
	Returns: the socket object
	"""
	# Implement code ...
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.bind((SERVER_IP, SERVER_PORT))
	server_socket.listen()

	return server_socket

def create_random_question():
	choice = random.choice(list(questions))
	for key, value in questions.items():
		if key == choice:
			question_number = key
			question = value["question"]
			answers = value["answers"]
			hey = chatlib.join_data(answers)
			list_question = chatlib.join_data([question_number, question]) + "#" + hey
			return list_question


def handle_question_message(conn):
	question = create_random_question()
	full_msg = chatlib.build_message("YOUR_QUESTION", question)
	print(f"[SERVER] {full_msg} ")
	conn.send(full_msg.encode())

def handle_answer_message(conn, username, data):
	data = chatlib.split_data(data, 1)
	question_number, answer = int(data[0]), int(data[1])
	for k, v in questions.items():
		print(type(v["correct"]), f"answer is {type(answer)}")
		if k == question_number:
			if v["correct"] == answer:
				for key, value in users.items():
					if key == username:
						build_and_send_message(conn, "CORRECT_ANSWER", "")
						value["score"] += 5
						return
			else:
				build_and_send_message(conn, chatlib.PROTOCOL_SERVER("WRONG_ANSWER"), "")
				return



def get_peer_name(conn):
	for k, v in logged_users.items():
		if v == conn:
			username = k
			return username




def send_error(conn, error_msg):
	"""
	Send error message with given message
	Recieves: socket, message error string from called function
	Returns: None
	"""
	# Implement code ...
	conn.send(error_msg.encode())

	

def print_client_sockets(list_of_sockets):
	for socket_name in list_of_sockets:
		print(socket_name)

	
##### MESSAGE HANDLING


def handle_getscore_message(conn, username):
	global users
	for key, value in logged_users.items():
		if value == conn:
			username = key

	for key, value in users.items():
		if username == key:
			score = value['score']
			build_and_send_message(conn, chatlib.PROTOCOL_SERVER["MY_SCORE"], str(score))
			return


def handle_highscore_message(conn):
	user_list = []
	message = ""
	for key, value in users.items():
		score = (value['score'])
		user_list += [[key, score]]

	user_list.sort(key=lambda s: s[1], reverse=True)
	for name, score in user_list:
		message += name + "-" + str(score) + "\n"

	build_and_send_message(conn, chatlib.PROTOCOL_SERVER["HIGHSCORE"], message)



def handle_logged_message(conn):
	build_and_send_message(conn, chatlib.PROTOCOL_SERVER["LOGGED"], logged_users)


def handle_logout_message(conn):
	"""
	Closes the given socket (in laster chapters, also remove user from logged_users dictioary)
	Recieves: socket
	Returns: None
	"""
	global logged_users
	for k, v in logged_users.items():
		if v == conn:
			logged_users.pop(k, None)
			logged_users.pop(v, None)
			return



	# Implement code ...


def handle_login_message(conn, data):
	"""
	Gets socket and message data of login message. Checks  user and pass exists and match.
	If not - sends error and finished. If all ok, sends OK message and adds user and address to logged_users
	Recieves: socket, message code and data
	Returns: None (sends answer to client)
	"""
	global users  # This is needed to access the same users dictionary from all functions
	global logged_users	 # To be used later
	list_user = chatlib.split_data(data, 1)
	user, password = list_user[0], list_user[1]
	for key, value in users.items():
		if key == user:
			if value['password'] == password:
				print("Client Logged in")
				build_and_send_message(conn, chatlib.PROTOCOL_SERVER["login_ok_msg"], "")
				logged_users[user] = conn
				return
			else:
				build_and_send_message(conn, chatlib.PROTOCOL_SERVER["login_failed_msg"], "")
				return
	build_and_send_message(conn, chatlib.PROTOCOL_SERVER["login_failed_msg"], "")
	return



# Implement code ...


def handle_client_message(conn, cmd, data):
	"""
	Gets message code and data and calls the right function to handle command
	Recieves: socket, message code and data
	Returns: None
	"""
	global logged_users	 # To be used later
	if cmd == "LOGIN":
		handle_login_message(conn, data)
	elif cmd == "MY_SCORE":
		handle_getscore_message(conn, data)
	elif cmd == "HIGHSCORE":
		handle_highscore_message(conn)
	elif cmd == "LOGGED":
		handle_logged_message(conn)
	elif cmd == "GET_QUESTION":
		handle_question_message(conn)
	elif cmd == "SEND_ANSWER":
		username = get_peer_name(conn)
		handle_answer_message(conn, username, data)


	else:
		#build_and_send_message(conn, chatlib.PROTOCOL_SERVER["ERROR"], "")
		print("hey")
	# Implement code ...
	


def main():
	# Initializes global users and questions dicionaries using load functions, will be used later
	global users
	global questions
	global client_sockets
	print("Welcome to Trivia Server!")
	server_socket = setup_socket()
	print("Listening for clients...")
	while True:
		ready_to_read, ready_to_write, in_error = select.select([server_socket] + client_sockets, [], [])
		for current_socket in ready_to_read:
			if current_socket is server_socket:
				(client_socket, client_address) = server_socket.accept()
				print("New client joined!", client_address)
				client_sockets.append(client_socket)
			else:
				print("New data from client")
				try:
					cmd, data = recv_message_and_parse(current_socket)
				except TypeError:
					cmd, data = "", ""
				if cmd == "" or cmd == "LOGOUT":
					print("Client, logged out")
					handle_logout_message(current_socket)
					client_sockets.remove(current_socket)
					current_socket.close()
				else:
					handle_client_message(current_socket, cmd, data)
		while messages_to_send != []:
			socket1, message = messages_to_send[0], messages_to_send[1]
			socket1.send(message.encode())
			messages_to_send.pop(0)
			messages_to_send.pop(0)
			print(socket1, message)






# Implement code ...



if __name__ == '__main__':
	main()

