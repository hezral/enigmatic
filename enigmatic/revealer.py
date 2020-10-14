#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gi.repository import Gtk

def reveal_child(button):
    if revealer.get_child_revealed():
        revealer.set_reveal_child(False)
        label.set_visible(False) # need to set_visible to false on anyy widget that took the space 
        window.resize(207, 24)
    else:
        label.set_visible(True)
        revealer.set_reveal_child(True)

    print(window.get_size())




window = Gtk.Window()
window.connect("destroy", Gtk.main_quit)

print(window.get_size())

grid = Gtk.Grid()
window.add(grid)

revealer = Gtk.Revealer()

grid.attach(revealer, 0, 1, 1, 1)

label = Gtk.Label("Label contained in a Revealer widget")
revealer.add(label)

button = Gtk.Button("Reveal")
button.props.hexpand = True
button.connect("clicked", reveal_child)
grid.attach(button, 0, 0, 1, 1)

window.show_all()

Gtk.main()