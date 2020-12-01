#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gi.repository import Gtk

def reveal_child(entry, event):
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
window.get_style_context().add_class(Gtk.STYLE_CLASS_FLAT)


grid = Gtk.Grid()
window.add(grid)



button = Gtk.Button("Reveal")
button.props.hexpand = True
button.connect("clicked", reveal_child)



search = Gtk.SearchEntry()
search.connect("focus-in-event", reveal_child)
search.connect("focus-out-event", reveal_child)

label = Gtk.Label("Label contained in a Revealer widget")
revealer = Gtk.Revealer()
revealer.add(label)


grid.attach(search, 0, 0, 1, 1)
grid.attach(revealer, 0, 1, 1, 1)


header = Gtk.HeaderBar()
header.props.show_close_button = True
header.props.decoration_layout = "close:maximize"
header.get_style_context().add_class(Gtk.STYLE_CLASS_FLAT)

window.set_titlebar(header)
window.show_all()

Gtk.main()
