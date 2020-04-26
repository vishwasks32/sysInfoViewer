#!/usr/bin/env python2
import pygtk
pygtk.require('2.0')
import gtk
import sysInfo
import os
import sys

IMAGEDIR = os.path.join(os.path.dirname(__file__), '../images')
OS_IMAGE = os.path.join(IMAGEDIR, 'Slackware.png')
PRO_IMAGE = os.path.join(IMAGEDIR, 'Processor.png')
SYSINFOICON = os.path.join(IMAGEDIR, 'sysInfoViewIcon.png')

def load_data_to_view(data_dict,data_key_list):
	frame=gtk.Frame()
	frame.set_shadow_type(gtk.SHADOW_IN)
	if len(data_dict) != 0:	
		table = gtk.Table(len(data_dict), 2,False)
		table.set_row_spacings(10)
		table.set_col_spacings(10)
	
		for row_count in range(len(data_key_list)):				
			for val_count in range(2):
				if val_count == 0:
					lbl_k = gtk.Label(data_key_list[row_count])
					lbl_k.set_justify(gtk.JUSTIFY_LEFT)
					
					table.attach(lbl_k,val_count,val_count+1,row_count,row_count+1,gtk.EXPAND,gtk.EXPAND,0,0)
				else:
					lbl_v = gtk.Label(data_dict[data_key_list[row_count]])
					lbl_v.set_justify(gtk.JUSTIFY_LEFT)
					table.attach(lbl_v,val_count,val_count+1,row_count,row_count+1,gtk.EXPAND,gtk.EXPAND,0,0)

		frame.add(table)

	else:
		label = gtk.Label("No Data Available")
		frame.add(label)
			
	return frame
	
def load_image(img):
	image = gtk.Image()
	image.set_from_file(img)
	image.set_size_request(100, 100)
	return image	
		
class SysInfoGtkView(gtk.Window):
	def __init__(self, parent=None):
		gtk.Window.__init__(self)
		try:
			self.set_screen(parent.get_screen())
		except AttributeError:
			self.connect('destroy', lambda *w: gtk.main_quit())
			
		self.set_title(self.__class__.__name__)
		self.set_border_width(8)
		self.set_default_size(640, 480)
		
		windowIcon = gtk.gdk.pixbuf_new_from_file(SYSINFOICON)
		self.set_icon(windowIcon)
				
		nb = gtk.Notebook()
		nb.set_tab_pos(gtk.POS_TOP)
		vbox1 = gtk.VBox()
		
		image = load_image(OS_IMAGE)
		vbox1.pack_start(image, True, True, 0)
		
		sys_data,pro_data = sysInfo.get_data()
		frame = load_data_to_view(sys_data,sysInfo.SYSINFOKEYS)
		vbox1.add(frame)
		
		nb.append_page(vbox1)
		nb.set_tab_label_text(vbox1, "Software")
		vbox3 = gtk.VBox()
		
		# Hardware Section
		image1 = load_image(PRO_IMAGE)
		vbox3.pack_start(image1, True, True, 0)
		
		frame1 = load_data_to_view(pro_data,sysInfo.PROINFOKEYS)
		vbox3.add(frame1)
			
		nb.append_page(vbox3)
		nb.set_tab_label_text(vbox3, "Hardware")
		
		self.add(nb)
		self.show_all()
		
def main():
	SysInfoGtkView()
	gtk.main()

if __name__ == '__main__':
	main()
