#!/usr/bin/python3
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
#   System Information Viewer
#   Copyright (C) 2020 Vishwas K singh <vishwasks32@gmail.com>
#
#   This program is free software: you can redistribute it and/or modify it
#   under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful, but
#   WITHOUT ANY WARRANTY; without even the implied warranties of
#   MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR
#   PURPOSE.  See the GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License along
#   with this program.  If not, see <http://www.gnu.org/licenses/>.

# Script to gather system information 
import os
import sys

import socket
import subprocess

__license__ = 'GPL-3+'
__version__='1.0'
# We don't know how much info we get but we will restrict it to some using keys
# It would be helpful to order also
SYSINFOKEYS = ["Operating System", "Distribution","System Type", "Branch","Kernel Release","Kernel Version","Computer Name", "Domain Name"]
PROINFOKEYS = ["Vendor ID","Model name", "Model", "CPU family","CPU(s)","CPU MHz","CPU op-mode(s)","Virtualization","Byte Order", "L1i cache", "L1d cache", "L2 cache", "L3 cache"]

def get_version():
    """Return the program version."""
    return __version__

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
	op_lst = op.split('\n')
	pro_data = dict()
	for item in op_lst:
		pro_data[item.split(':')[0].strip()] = item.split(':')[1].strip()
	
	return pro_data
	
def get_data():
	''' Function to generate System Information '''
	# Software Information
	# Check for Slackware file in /etc/slackware-version
	sys_info_values = list()
	slack_file = '/etc/slackware-version'
	if  os.path.isfile(slack_file):
		f = open(slack_file,'r')
		slack_dist = f.read().strip()
		sys_info_values.append(['Distribution',slack_dist])
		if slack_dist.endswith('+'):
			sys_info_values.append(['Branch','Current'])
		else:
			sys_info_values.append(['Branch','Stable'])
			
	sys_info_values.append(['Operating System', uname('-o')])
	sys_info_values.append(['System Type',uname('-m')])
	sys_info_values.append(['Kernel Release',uname('-r')])
	sys_info_values.append(['Kernel Version',uname('-v')])
	sys_info_values.append(['Domain Name',socket.gethostname()])
	sys_info_values.append(['Computer Name',socket.gethostname().split('.')[0]])
	
	# Processor Information
	pro_data = lscpu()
	pro_data_copy = pro_data.copy()
	pro_data_lst = list()

	for item in PROINFOKEYS:
		pro_data_lst.append([item, pro_data[item]])
		
	return (sys_info_values,pro_data_lst,SYSINFOKEYS,PROINFOKEYS)
	
if __name__=='__main__':
	'''Main function to execute the script'''
	get_data()
