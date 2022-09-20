# Protocol Constants

CMD_FIELD_LENGTH = 16	# Exact length of cmd field (in bytes)
LENGTH_FIELD_LENGTH = 4   # Exact length of length field (in bytes)
MAX_DATA_LENGTH = 10**LENGTH_FIELD_LENGTH-1  # Max size of data field according to protocol
MSG_HEADER_LENGTH = CMD_FIELD_LENGTH + 1 + LENGTH_FIELD_LENGTH + 1  # Exact size of header (CMD+LENGTH fields)
MAX_MSG_LENGTH = MSG_HEADER_LENGTH + MAX_DATA_LENGTH  # Max size of total message
DELIMITER = "|"  # Delimiter character in protocol
DATA_DELIMITER = "#"  # Delimiter in the data part of the message

# Protocol Messages 
# In this dictionary we will have all the client and server command names

PROTOCOL_CLIENT = {
"login_msg" : "LOGIN",
"logout_msg" : "LOGOUT",
"GET_SCORE" : "MY_SCORE",
"HIGHSCORE" : "HIGHSCORE",
"GET_QUESTION" : "GET_QUESTION",
"SEND_ANSWER" : "SEND_ANSWER",
"LOGGED" : "LOGGED"
} # .. Add more commands if needed


PROTOCOL_SERVER = {
"login_ok_msg" : "LOGIN_OK",
"login_failed_msg" : "ERROR",
"NO_QUESTIONS" : "NO MORE QUESTIONS",
"CORRECT_ANSWER" : "CORRECT_ANSWER",
"WRONG_ANSWER" : "WRONG_ANSWER",
"ERROR" : "ERROR",
"HIGHSCORE" : "ALL_SCORE",
"MY_SCORE" : "YOUR_SCORE",
"LOGGED" : "LOGGED_ANSWER",
"YOUR_QUESTION" : "YOUR_QUESTION"
} # ..  Add more commands if needed


# Other constants

ERROR_RETURN = None  # What is returned in case of an error


def build_message(cmd, data):
	"""
	Gets command name (str) and data field (str) and creates a valid protocol message
	Returns: str, or None if error occured
	"""
	# Implement code ...
	length = len(data)
	lengthcmd = len(cmd)
	spaces = (16-lengthcmd) * " "
	if length == 0:
		full_msg = f"{cmd}{spaces}|0000|"
		return full_msg
	elif length < 10 and length > 0:
		full_msg = f"{cmd}{spaces}|000{str(length)}|{data}"
		return full_msg
	elif length > 9 and length < 100:
		full_msg = f"{cmd}{spaces}|00{str(length)}|{data}"
		return full_msg
	elif length > 99 and length < 1000:
		full_msg = f"{cmd}{spaces}|0{str(length)}|{data}"
		return full_msg
	elif length > 999 and length < 10000:
		full_msg = f"{cmd}{spaces}|{str(length)}|{data}"
		return full_msg
	else:
		return ERROR_RETURN



def parse_message(data):
	"""
	Parses protocol message and returns command name and data field
	Returns: cmd (str), data (str). If some error occured, returns None, None
	"""
	if len(data) < 22 or len(data) > 10000:
		return ERROR_RETURN
	stringcheck = data.count("|")
	if stringcheck != 2:
		return ERROR_RETURN
	try:
		logincheck = data.split("|")[0]
		numbers = data.split("|")[1]
		data =	data.split("|")[2]
		login = logincheck.replace(" ", "")
		if numbers.isdigit and len(data) == int(numbers):
			return str(login), str(data)
		else:
			return ERROR_RETURN
	except ValueError:
		return ERROR_RETURN


	# The function should return 2 values
	#return cmd, msg

	
def split_data(msg, expected_fields):
	"""
	Helper method. gets a string and number of expected fields in it. Splits the string
	using protocol's data field delimiter (|#) and validates that there are correct number of fields.
	Returns: list of fields if all ok. If some error occured, returns None
	"""
	# Implement code ...
	count = msg.count("#")
	if count == expected_fields:
		list_msg = msg.split('#')
		return list_msg
	return ERROR_RETURN


def join_data(msg_fields):
	"""
	Helper method. Gets a list, joins all of it's fields to one string divided by the data delimiter.
	Returns: string that looks like cell1#cell2#cell3
	"""
	length_list = len(msg_fields)
	message = ""
	count = 0
	for item in msg_fields:
		count += 1
		if count == length_list:
			message += str(item)
			break
		message += str(item) + "#"
	return message



