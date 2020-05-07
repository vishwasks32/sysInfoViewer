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

import gi
gi.require_version('Gtk','3.0')

from gi.repository import Gtk
from . import sysInfo
import os

IMAGEDIR = os.path.join(os.path.dirname(__file__), 'images')
OS_IMAGE = os.path.join(IMAGEDIR, 'Slackware.png')
PRO_IMAGE = os.path.join(IMAGEDIR, 'Processor.png')
SYSINFOICON = os.path.join(IMAGEDIR, 'sysInfoViewIcon.png')

class SysInfoGtkView(Gtk.Window):
	''' System Information Gtk View Window'''
	def __init__(self):
		Gtk.Window.__init__(self, title="System Information")
		self.set_border_width(10)
		self.set_default_size(480,480)
		self.set_default_icon_from_file(SYSINFOICON)
		self.set_icon_name('System Information')
		
		self.sys_data,self.pro_data,self.sys_info_keys,self.pro_info_keys = sysInfo.get_data()
		
		box_outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
		self.add(box_outer)
		
		nb = Gtk.Notebook()
		box_outer.pack_start(nb, False,False,0)
		
		lb1 = self.inside_view(self.sys_data,OS_IMAGE)
		pg1_label = Gtk.Label()
		pg1_label.set_label('Software') 
		nb.append_page(lb1,pg1_label)
		
		lb2 = self.inside_view(self.pro_data,PRO_IMAGE)
		pg2_label = Gtk.Label()
		pg2_label.set_label('Hardware')
		nb.append_page(lb2,pg2_label)
		
	def inside_view(self,data_lst,icon_img):
		'''Function to place the relevent data on the window'''
		# Software Section
		listbox = Gtk.ListBox()
		listbox.set_selection_mode(Gtk.SelectionMode.NONE)
		
		row = Gtk.ListBoxRow()
		
		vbox1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		image = Gtk.Image()
		image.set_from_file(icon_img)
		vbox1.pack_start(image, True,True, 0)	
		row.add(vbox1)
		listbox.add(row)
		
		row = Gtk.ListBoxRow()
		vbox2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		
		# Creating the ListStore model
		self.software_liststore = Gtk.ListStore(str, str)
		for item in data_lst:
			self.software_liststore.append(list(item))

		# creating the treeview, making it use the filter as a model, and adding the columns
		self.treeview = Gtk.TreeView.new_with_model(self.software_liststore)
		for i, column_title in enumerate(
			["Property", "Value"]
		):
			renderer = Gtk.CellRendererText()
			column = Gtk.TreeViewColumn(column_title, renderer, text=i)
			self.treeview.append_column(column)

		# setting up the layout, putting the treeview in a scrollwindow, and the buttons in a row
		self.scrollable_treelist = Gtk.ScrolledWindow()
		self.scrollable_treelist.set_policy(Gtk.PolicyType.AUTOMATIC,Gtk.PolicyType.AUTOMATIC)
		
		self.scrollable_treelist.set_min_content_height(380)
		
		self.scrollable_treelist.add(self.treeview)
		
		row.add(self.scrollable_treelist)
		vbox2.pack_start(row, True, True, 0)
		listbox.add(vbox2)
		
		return listbox
				
if __name__ == '__main__':
	'''This is executed when script is callled directly'''
	win = SysInfoGtkView()
	win.connect("destroy", Gtk.main_quit)
	win.show_all()
	Gtk.main()
