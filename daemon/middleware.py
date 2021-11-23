#!/usr/bin/env python3

import socket
import sys
import time
import traceback

from lib.auxiliary import *

# Polling interval in seconds.
INTERVAL = 1

# Positional arguments.
P_ARGUMENTS = {
	("<IP>",)      : "IP address the API resides on (default=\"127.0.0.1\")",
	("<PORT>",)    : "Port on the <IP> the API resides on (default=8080)",
	("<API>",)     : "API endpoint to POST to (default=\"/api/report\")",
	("<SOCKET>",)  : "IPC socket path (default=\"/tmp/ctrace.sock\")",
}

# Optional help arguments.
H_ARGUMENTS = {
	("-h", "--help"): "Display the help menu and exit.",
}

# Optional arguments.
O_ARGUMENTS = {
	("-v", "--verbose"): "Enable verbose output.",
}

def print_help(path: str="main.py", alignmentWidth: int=16) -> None:
	"""
	Output help menu to stdout upon request. LHS args are aligned to a fixed
	width of alignmentWidth columns.
	"""

	# Shorthand alignment function for aligning to the ALIGNMENT_WIDTH.
	align = lambda s: s + ' '*(alignmentWidth-len(s))

	print(f"Usage: {path} [ARGUMENTS] <IP> <PORT> <API> <SOCKET>")
	print("Start the CyberTrace middleware that connects the daemon to the API.")
	print()

	print("Help:")
	for key in H_ARGUMENTS:
		print(align(", ".join([*key])) + H_ARGUMENTS[key])

	print("Positional arguments:")
	for key in P_ARGUMENTS:
		print(align(", ".join([*key])) + P_ARGUMENTS[key])

	print("Optional arguments:")
	for key in O_ARGUMENTS:
		print(align(", ".join([*key])) + O_ARGUMENTS[key])

def forward(db: str, sock: socket.socket, ip: str, port: int, api: str) -> None:
	"""
	Receive some data from the socket and forward it to the API endpoint
	in the form of JSON data.
	"""

	pass

def main(args: list=["./main.py"]):

	# Parse CLI arguments.
	path = args[0]
	args = args[1::]

	settings = {
		"verbose"   : False,
		"ip"        : "127.0.0.1",
		"port"      : 8080,
		"api"       : "/api/report",
		"socket"    : "/tmp/ctrace.sock",
	}

	# Parsing help arguments.
	if any([arg in list(*H_ARGUMENTS.keys()) for arg in args]):
		print_help(path)
		return 0

	# Parsing verbose arguments.
	if any([arg in ("-v", "--verbose") for arg in args]):
		try:
			settings["verbose"] = True
			args.remove("-v")
			args.remove("--verbose")
		except:
			pass

	# Parsing positional arguments.
	try:
		settings["ip"]      = args.pop(0)
		settings["port"]    = args.pop(0)
		settings["api"]     = args.pop(0)
		settings["socket"]  = args.pop(0)
	except:
		pass

	log(NORMAL, "Initializing CyberTrace middleware...")
	log(NORMAL, "Options:")
	log(NORMAL, "| Verbose  : %s" % colored(settings["verbose"], "yellow"))
	log(NORMAL, "| Endpoint : %s" % colored(
		f"{settings['ip']}:{settings['port']}{settings['api']}", "yellow"))
	log(NORMAL, "| Socket   : %s" % colored(settings["socket"], "yellow"))

	# Create the socket.
	s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

	log(NORMAL, "Connecting to the socket...")

	# Connect to the socket.
	while True:
		try:
			s.connect(settings["socket"])
			log(NORMAL, "Connected.")
			break
		except:
			time.sleep(1)

	# Get the attack/alert database location.
	n = int.from_bytes(s.recv(4), "big")
	db = s.recv(n).decode()

	# Forward the data from the daemon to the API indefinitely.
	while True:

		try:
			log(VERBOSE, "Starting interval...")
			start = time.time()

			forward(db, s, settings["ip"], settings["port"], settings["api"])

			if ((e:=time.time() - start) < INTERVAL):
				time.sleep(INTERVAL - (e-start))

			log(VERBOSE, "Interval complete.")

		# Upon keyboard interrupt, kill the loop.
		except KeyboardInterrupt:
			log(EMERGENCY, "Keyboard interrupt detected. Killing middleware.", start="\r")
			break

		# Output but otherwise ignore other exception cases.
		except:
			log(EMERGENCY, "Other exception occurred:")
			traceback.print_exc()

if __name__ == "__main__":
	main(sys.argv[0::])
