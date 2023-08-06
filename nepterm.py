import os

ERROR = "ERROR"
CD = "CD"

COMMAND_ID = {
	"ls": 0,
	"touch": 1,
	"cat": 2,
	"mkdir": 3,
	"cd": 4,
	"pwd": 5,
	"exit": 6,
	"help": 7,
	"rm": 8,
	"echo": 9,
	"clear": 10,
	"$": 11,
	ERROR: 12,
}


def handle_ls(cwd: str, stream: str):
	try:
		file_path = stream.split()[1]
	except:
		file_path = cwd
	files = [file for file in os.listdir(file_path)]
	return ".\n..\n"+"\n".join(files)

def check_for_command_id(stream: str):
	try:
		type = stream.split()[0]
		if type in COMMAND_ID:
			return COMMAND_ID[type]
		return COMMAND_ID[ERROR]
	except:
		return COMMAND_ID[ERROR]

def handle_command_by_id(cwd: str, stream: str, id: int):
	if (id == COMMAND_ID["ls"]):
		return handle_ls(cwd, stream)
	pass

def exec(cwd: str, stream: str):
	id = check_for_command_id(stream)
	if id == COMMAND_ID[ERROR]:
		return ERROR
	return handle_command_by_id(cwd, stream, id)

if __name__ == "main":
	print(exec(r"C:\Lakshay\Projects\Neptune", "ls"))