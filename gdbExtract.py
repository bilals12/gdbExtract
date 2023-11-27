import os
import sys
import json
import subprocess
import logging
from typing import List, Dict


# configure basic logging to display errors and info
logging.basicConfig(level=logging.INFO)

# constants for file paths and binary to be analyzed
BINARY_PATH = "/path/to/binary"
DATA_FILE = "path/to/file.json"
riskyFunctions = ['strcpy', 'strncpy', 'memcpy', 'memset', 'send', 'recv']

# GDB command to list all functions in binary
# returns output from GDB as string
def run_gdb_command(binary_path: str) -> str:
	try:
		return subprocess.check_output(["gdb", "-batch", "-ex", "info functions", binary_path])
	except subprocess.CalledProcessError as e:
		logging.error(f"GDB command failed: {e}")
		sys.exit(1)

# parse output from GDB to extract function info
# returns list of dicts, each containing details of single function
def parse_gdb_output(gdb_output: str) -> List[Dict]:
	json_data = []
	for line in gdb_output.splitlines():
		if not line.startswith("0x"): continue
		address, name, signature = line.strip().split()
		json_data.append({"address": address, "name": name, "signature": signature})
	return json_data

# reads json file and returns content
def read_json_file(file_path: str) -> List[Dict]:
	try:
		with open(file_path, "r") as file:
			return json.load(file)
	except IOError as e:
		logging.error(f"error reading file {file_path}: {e}")
		return []
	except json.JSONDecodeError as e:
		logging.error(f"error decoding JSON from file {file_path}: {e}")

# writes list of dicts to json file
def write_json_file(file_path: str, data: List[Dict]):
	try:
		with open(file_path, "w") as file:
			json.dump(data, file, indent=4) # indentation for readability
	except IOError as e:
		logging.error(f"error writing to file {file_path}: {e}")

# main function that extracts function info from binary via GDB
def main_search_code():
	gdb_output = run_gdb_command(BINARY_PATH)
	json_data = parse_gdb_output(gdb_output)
	write_json_file(DATA_FILE, json_data)

# filters out functions deemed "safe" and writes the rest to new json file
def remove_safe_functions():
	json_data = read_json_file(DATA_FILE)
	filtered_json_data = [func for func in json_data if func['name'] not in riskyFunctions]
	write_json_file("filtered_file.json", filtered_json_data)

# combines multiple entries of the same function into a single record
# tracks number of occurrences of each function
def combine_data_for_same_function():
	json_data = read_json_file("filtered_file.json")
	combined_json_data = {}
	for func in json_data:
		if func["name"] not in combined_json_data:
			combined_json_data[func["name"]] = {
			"addresses": [func["address"]],
			"signature": func["signature"],
			"count": 1,
			}
		else:
			combined_json_data[func["name"]]["addresses"].append(func["address"])
			combined_json_data[func["name"]]["count"] += 1

	write_json_file("combined_file.json", combined_json_data)

# lists all functions in json data file
def list_functions():
	json_data = read_json_file(DATA_FILE)
	for func in json_data:
		print(f"{func['address']}: {func['name']}")

# searches for specific function in json data file by address or name
def search_function():
	json_data = read_json_file(DATA_FILE)
	func_addr_name = input("enter a function address or name: ")
	found = False
	for func in json_data:
		if func["address"] == func_addr_name or func["name"] == func_addr_name:
			print(f"found {func['address']}: {func['name']}")
			found = True
			break
	if not found:
		print(f"could not find function with address or name '{func_addr_name}'.")

# main entry point
# handles cli args and calls corresponding functions
def main():
	# check if correct number of args are passed
	if len(sys.argv) == 2:
		command = sys.argv[1]
		# execute function based on arg
		if command == "search":
			main_search_code()
		elif command == "remove-safe":
			remove_safe_functions()
		elif command == "combine":
			combine_data_for_same_function()
		elif command == "list":
			list_functions()
		else:
			logging.error("unknown command. please enter a valid option.")
			sys.exit(1)
	else:
		logging.error("incorrect number of args.")
		sys.exit(1)

# run script only if script is executed as main program
if __name__ == "__main__":
	main()