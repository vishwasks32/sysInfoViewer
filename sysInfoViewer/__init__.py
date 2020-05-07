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

import signal

from locale import gettext as _

import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk  

from sysInfoViewer import sysInfoView
from sysInfoViewer import sysInfo


def main():
	'constructor for sysInfoViewer class instances'

	# Run the application.
	window = sysInfoView.SysInfoGtkView()

	window.connect("destroy", Gtk.main_quit)
	window.show_all()
	Gtk.main()
