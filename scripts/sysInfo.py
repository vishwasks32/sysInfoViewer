#!/usr/bin/env python2
# Script to gather system information 
import os
import sys
import json
import socket
import subprocess

# We don't know how much info we get but we will restrict it to some using keys
# It would be helpful to order also
SYSINFOKEYS = ["Operating System", "Distribution","System Type", "Branch","Kernel Release","Kernel Version","Computer Name", "Domain Name"]
PROINFOKEYS = ["Vendor ID","Model name", "Model", "CPU family","CPU(s)","CPU MHz","CPU op-mode(s)","Virtualization","Byte Order", "L1i cache", "L1d cache", "L2 cache", "L3 cache"]

def uname(option):
	'''Function to based on System uname command'''
	command = subprocess.Popen(['uname', option],stdout=subprocess.PIPE).stdout.read().strip()
	command = command.decode('utf-8')
	if command == '':
		#logger.debug('Command "%s" could not be found.' % command)
		pass
	
	return command
	
def lscpu():
	''' Function based on lscpu'''
	command = subprocess.Popen(['lscpu'],stdout=subprocess.PIPE).stdout.read().strip()
	op = command.decode('utf-8')
	op_lst = command.split('\n')
	pro_data = dict()
	for item in op_lst:
		pro_data[item.split(':')[0].strip()] = item.split(':')[1].strip()
	
	return pro_data
	
def get_data():
	# Check for Slackware file in /etc/slackware-version
	sys_info_values = dict()
	slack_file = '/etc/slackware-version'
	if  os.path.isfile(slack_file):
		f = open(slack_file)
		sys_info_values['Distribution'] = f.read().strip()
		if sys_info_values['Distribution'].endswith('+'):
			sys_info_values['Branch'] = 'Current'
		else:
			sys_info_values['Branch'] = 'Stable'
	
	
	sys_info_values['Operating System'] = uname('-o')
	sys_info_values['System Type'] = uname('-m')
	sys_info_values['Kernel Release'] = uname('-r')
	sys_info_values['Kernel Version'] = uname('-v')
	sys_info_values['Domain Name'] = socket.gethostname()
	sys_info_values['Computer Name'] = socket.gethostname().split('.')[0]
	pro_data = lscpu()
	for item in pro_data.keys():
		if item not in PROINFOKEYS:
			pro_data.pop(item,None)
			
	return (sys_info_values,pro_data)
	
if __name__=='__main__':
	get_data()
