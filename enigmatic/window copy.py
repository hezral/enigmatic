#!/usr/bin/env python3

'''
   Copyright 2020 Adi Hezral (hezral@gmail.com) (https://github.com/hezral)

   This file is part of enigmatic.

    enigmatic is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    enigmatic is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with enigmatic.  If not, see <http://www.gnu.org/licenses/>.
'''

import sys
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Granite', '1.0')
from gi.repository import Gtk, Gdk, Gio, Granite, GObject, Pango
from constants import AppAttributes

#------------------CLASS-SEPARATOR------------------#

class EnigmaticWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #---- window -----#

        # self.props.border_width = 24
        self.set_resizable(False)
        #self.get_style_context().add_class("rounded")
        #self.get_style_context().add_class(Gtk.STYLE_CLASS_FLAT)

        #---- header widgets -----#
        TitleLabel = Gtk.Button(label="ENIGMATIC")
        TitleLabel.get_style_context().add_class("title-button")


        #---- header -----#
        HeaderBar = Gtk.HeaderBar()
        HeaderBar.props.show_close_button = True
        HeaderBar.props.decoration_layout = "close:maximize"

        HeaderBar.pack_end(TitleLabel)
        HeaderBar.get_style_context().add_class("default-decoration")
        HeaderBar.get_style_context().add_class(Gtk.STYLE_CLASS_FLAT)
    
 
        #---- window -----#
        self.set_titlebar(HeaderBar)
        
        self.show_all()


#------------------CLASS-SEPARATOR------------------#




#------------------CLASS-SEPARATOR------------------#


#------------------CLASS-SEPARATOR------------------#

#------------------CLASS-SEPARATOR------------------#


class EnigmaticApp(Gtk.Application):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # set application properties
        self.props.application_id = AppAttributes.application_id

        # set theme and css provider
        # initialize any objects
        self.window = None

    def do_startup(self):
        Gtk.Application.do_startup(self)

    def do_activate(self):
        # We only allow a single window and raise any existing ones
        if self.window is None:
            # Windows are associated with the application 
            # when the last one is closed the application shuts down
            self.window = EnigmaticWindow(application=self)
            self.add_window(self.window)
            # self.window.show_all()


#------------------CLASS-SEPARATOR------------------#


app = EnigmaticApp()
app.run(sys.argv)