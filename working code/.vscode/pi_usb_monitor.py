# standard library
import subprocess
import re
from copy import deepcopy
import platform

# 3rd party packages

# local resources

def pull_usb_device_log():
	if platform.system() == "Linux":
		raw_msg = subprocess.getoutput("dmesg --decode | grep tty | grep now")
	elif platform.system() == "Windows":
		raw_msg = subprocess.getoutput("powershell -Command \"Get-PnpDevice -PresentOnly | Where-Object { $_.FriendlyName -match 'CH340' }\"")
	lines = raw_msg.split("\n")
	return lines

def parse_usb_device_log_line(device_log_line: str = ""):
	"""
	parse one line of the usb_device_log to get
	"""
	# pattern_connection_status = r"\: \[.*\] (.*)\: (.*) now ([a-zA-Z]+) [a-zA-z]+ (tty.*)"
	pattern_connection_status = r"(\S+)\s{2,}(\S+)\s{2,}(.+?)\s{2,}(\S+)"
	connection_info = re.findall(pattern_connection_status, device_log_line)
	if connection_info:
		status, clas, friendly_name, instance_id = connection_info[0]
		parsed_log_msg =  {
			"status": status,
			"class": clas,
			"device": friendly_name,
			"instance_id": instance_id
		}
		return parsed_log_msg
	else:
		return None

def attach_device_to_tree(tree: dict, parsed_log_msg: dict) -> dict:
	device_address = parsed_log_msg["device"]
	device_port_match = re.search(r"\((COM\d+)\)", device_address)
	device_port = None
	if device_port_match:
		device_port = device_port_match.group(1)

	hub_address = device_port

	branch = tree.setdefault(hub_address, {})
	device = branch.setdefault(hub_address, {})
	
	device["name"] = parsed_log_msg["device"].split(" (")[0]
	device["port"] = device_port
	device["info"] = parsed_log_msg["instance_id"].split("\\")[1]
	return tree

def disconnect_device_from_tree(tree: dict, parsed_log_msg: dict) -> dict:
	serial_port = parsed_log_msg["serial_port"]
	for branch in tree:
		for device in tree[branch]:
			if tree[branch][device]["info"] == serial_port:
				tree[branch].pop(device)
				break
	return tree

def update_usb_device_tree(tree: dict= None) -> dict:
	"""
	read usb ports and return a  dictionary of serial ports
	"""
	if tree is None:
		tree = {}

	lines = pull_usb_device_log()
	for line in lines:
		parsed = parse_usb_device_log_line(line)
		if parsed and parsed.get("status") == "OK":
			attach_device_to_tree(tree, parsed)
	return tree

def extract_info(tree: dict= None) -> list:
	info_list = []
	for usb_port, devices in tree.items():
		for device_name, device_info in devices.items():
			info = device_info.get('info')
			if info:
				info_list.append(info)
	return info_list

if __name__ == "__main__":
	from copy import deepcopy

	old_tree = {}
	while True:
		try:
			lines = pull_usb_device_log()
			tree = {}
			for line in lines:
				parsed = parse_usb_device_log_line(line)
				if parsed and parsed.get("status") == "OK":
					attach_device_to_tree(tree, parsed)
			if tree != old_tree:
				old_tree = deepcopy(tree)
				print(tree)
		except KeyboardInterrupt:
			print("Keyboard interrupted, exiting program...")
			break

	print("=" * 50)
	print(update_usb_device_tree())
