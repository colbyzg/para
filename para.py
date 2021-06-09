#! /usr/bin/python

import paramiko
import time

username = "your_username"
password = "your_password"
enable_pw = "enable_password"

devices = {
	"192.168.14.2": "ASA", 
	"192.168.14.1": "IOS"
	}

commands = ["sh ver", "sh int ip br", "sh vlan br"]

def main():
	ssh_conn(devices)

def enable(conn, enable_pw):
	conn.send("enable\r")
	time.sleep(1)
	conn.send(enable_pw + "\r")
	time.sleep(1)

def ssh_conn(devices):
	for device, type in devices.iteritems():
		output = []
		conn_pre = paramiko.SSHClient()
		conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		conn_pre.connect(device, username=username, password=password)
		time.sleep(1)
		conn = conn_pre.invoke_shell()
		time.sleep(1)
		if ">" in conn.recv(100000):
			enable(conn, enable_pw)
			time.sleep(1)
		if type.lower() == "asa":
			conn.send("term page 0\r")
			time.sleep(1)
		if type.lower() == "ios" or type.lower() == "nxos":
			conn.send("term len 0\r")
			time.sleep(1)
	
		for command in commands:
			conn.send(command + "\r")
			time.sleep(1)
			output.append(conn.recv(100000))

		with open(device + ".out", "w+") as out_file:
			out_file.writelines(output)
			print("{}.out created".format(device))

if __name__ == "__main__":
	main()
