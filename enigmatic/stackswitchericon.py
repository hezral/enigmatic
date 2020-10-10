import sys
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Granite', '1.0')
from gi.repository import Gtk, Gdk, Gio, Granite, GObject, Pango
from constants import AppAttributes


win  = Gtk.Window () 
grid = Gtk.Grid ()
win.add (grid)

stack = Gtk.Stack ()
childstack = Gtk.Entry ()
stack.add_titled (childstack, "_Namestack", "LabelInTheSwitcher")
grid.attach (stack, 0, 1, 1, 1)

switcher = Gtk.StackSwitcher ()
switcher.set_stack (stack)
switcher.props.icon_size = Gtk.IconSize.DIALOG
grid.attach (switcher, 0, 0, 1, 1)

""" Use icon instead for your switcher """
stack.child_set_property (childstack, "icon-name", "com.github.hezral.inspektor")


win.show_all ()
win.connect ("destroy", Gtk.main_quit)

Gtk.main ()