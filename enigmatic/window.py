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
        width = 720
        height = 576
        self.set_size_request(width, height)
        self.set_default_size(width, height)
        # geometry = Gdk.Geometry()
        # setattr(geometry, 'min_height', height)
        # setattr(geometry, 'min_width', width)
        # self.set_geometry_hints(None, geometry, Gdk.WindowHints.MIN_SIZE)
        self.props.title = AppAttributes.application_name
        # self.props.border_width = 24
        self.props.resizable = False
        self.get_style_context().add_class("rounded")
        #self.get_style_context().add_class(Gtk.STYLE_CLASS_FLAT)

        #---- header widgets -----#
        TitleLabel = Gtk.Button(label="ENIGMATIC")
        TitleLabel.get_style_context().add_class("title-button")

        gtk_settings = Gtk.Settings.get_default()
        ModeSwitch = Granite.ModeSwitch.from_icon_name("display-brightness-symbolic", "weather-clear-night-symbolic")
        ModeSwitch.props.primary_icon_tooltip_text = "Light mode"
        ModeSwitch.props.secondary_icon_tooltip_text = "Dark mode"
        ModeSwitch.props.valign = Gtk.Align.CENTER
        ModeSwitch.bind_property("active", gtk_settings, "gtk-application-prefer-dark-theme", GObject.BindingFlags.BIDIRECTIONAL)
        settings = Gio.Settings(schema_id="com.github.hezral.movens")
        settings.bind ("prefer-dark-style", ModeSwitch, "active", Gio.SettingsBindFlags.DEFAULT)

        #---- header -----#
        HeaderBar = Gtk.HeaderBar()
        HeaderBar.props.show_close_button = True
        HeaderBar.props.decoration_layout = "close:maximize"
        HeaderBar.pack_end(ModeSwitch)
        HeaderBar.pack_end(TitleLabel)
        HeaderBar.get_style_context().add_class("default-decoration")
        HeaderBar.get_style_context().add_class(Gtk.STYLE_CLASS_FLAT)
    
        #---- views -----#
        main = MainView()
        share = ShareView()
        recover = RecoverView()

        #---- notebook -----#
        notebook = Gtk.Notebook()
        notebook.props.tab_pos = Gtk.PositionType.BOTTOM
        notebook.append_page(share, Gtk.Label("SHARE"))
        notebook.append_page(recover, Gtk.Label("RECOVER"))
        notebook.child_set_property(share, "tab-expand", True)
        notebook.child_set_property(recover, "tab-expand", True)

        #---- stack -----#
        self.stack = Gtk.Stack()
        self.stack.props.transition_type = Gtk.StackTransitionType.CROSSFADE
        self.stack.add_named(main, "main")
        self.stack.add_named(notebook, "notebook")
        # self.stack.add_named(share, "share")
        # self.stack.add_named(recover, "recover")
        self.stack.set_visible_child(main)
        self.stack.set_visible_child(notebook)
        # self.stack.set_visible_child(share)
        # self.stack.set_visible_child(recover)

        #---- layout -----#
        layout = Gtk.Grid()
        layout.props.row_spacing = 12
        layout.attach(self.stack, 0, 3, 2, 1)
        layout.props.expand = True

        #---- window -----#
        self.set_titlebar(HeaderBar)
        self.add(layout)
        self.show_all()

#------------------CLASS-SEPARATOR------------------#

class MainView(Gtk.Grid):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #---- get started -----#
        GetStartedImage = Gtk.Image().new_from_icon_name("text-x-readme", Gtk.IconSize.LARGE_TOOLBAR)
        GetStartedButton = Gtk.Button(label="Quick Start Guide", image=GetStartedImage)
        GetStartedButton.props.hexpand = True
        GetStartedButton.props.always_show_image = True
        
        #---- stack buttons -----#
        ShareStackImage = Gtk.Image().new_from_icon_name("com.github.hezral.inspektor", Gtk.IconSize.DIALOG)
        ShareStackImage.set_pixel_size(96)
        self.ShareStackButton = Gtk.Button(label="SHARE", image=ShareStackImage)
        self.ShareStackButton.props.always_show_image = True
        self.ShareStackButton.props.image_position = Gtk.PositionType.TOP
        self.ShareStackButton.props.expand = True
        self.ShareStackButton.connect("clicked", self.toggle_stack)
        self.ShareStackButton.get_style_context().add_class("stack-button")

        RecoverStackImage = Gtk.Image().new_from_icon_name("internet-chat", Gtk.IconSize.DIALOG)
        RecoverStackImage.set_pixel_size(96)
        self.RecoverStackButton = Gtk.Button(label="RECOVER", image=RecoverStackImage)
        self.RecoverStackButton.props.always_show_image = True
        self.RecoverStackButton.props.image_position = Gtk.PositionType.TOP
        self.RecoverStackButton.props.expand = True
        self.RecoverStackButton.connect("clicked", self.toggle_stack)
        self.RecoverStackButton.get_style_context().add_class("stack-button")

        #---- grid -----#
        self.props.expand = True
        self.attach(self.ShareStackButton, 0, 1, 1, 1)
        self.attach_next_to(self.RecoverStackButton, self.ShareStackButton, 1, 1, 1)
        self.attach(GetStartedButton, 0, 2, 2, 1)

    def toggle_stack(self, widget):
        stack = self.get_parent()
        stack_children = stack.get_child_by_name("notebook")
        stack.set_visible_child_full("notebook",Gtk.StackTransitionType.CROSSFADE)
        if widget.get_label() == "SHARE":
            # stack.set_visible_child_full("share",Gtk.StackTransitionType.CROSSFADE)
            stack_children.set_current_page(0)
        else:
            # stack.set_visible_child_full("recover",Gtk.StackTransitionType.CROSSFADE)
            stack_children.set_current_page(1)

#------------------CLASS-SEPARATOR------------------#

class ShareView(Gtk.Grid):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #---- stack header -----#
        ShareStackImage = Gtk.Image().new_from_icon_name("com.github.hezral.inspektor", Gtk.IconSize.DIALOG)
        ShareStackLabel = Gtk.Label("SHARE")
        ShareStackSubtitle = Gtk.Label("Divide and share your secrets for safekeeping")
        ShareStackHeader = Gtk.Grid()
        ShareStackHeader.attach(ShareStackImage, 0, 1, 1, 2)
        ShareStackHeader.attach(ShareStackLabel, 1, 1, 1, 1)
        ShareStackHeader.attach(ShareStackSubtitle, 1, 2, 1, 1)

        BackButton = Gtk.Button(image=Gtk.Image().new_from_icon_name(icon_name='go-previous-symbolic', size=Gtk.IconSize.LARGE_TOOLBAR))
        BackButton.props.expand = False
        BackButton.props.valign = Gtk.Align.START
        BackButton.props.halign = Gtk.Align.START
        BackButton.set_size_request(40, 40)
        BackButton.get_style_context().add_class("back-to-main-button")
        BackButton.connect("clicked", self.on_backbutton_clicked)

        SecretHeader = Gtk.Label("Secrets or Passphrase to share")
        SecretHeader.get_style_context().add_class("h3")
        SecretHeader.props.hexpand = True

        SecretEntry = Gtk.Entry()
        SecretEntry.connect("focus_out_event", self.on_secretentry_changed)

        ShareSplitHeader = Gtk.Label("Split into")
        ShareSplit = Gtk.SpinButton().new_with_range(min=3, max=25, step=1)
        ShareSplit.connect("value-changed", self.on_sharesplit_changed)
        
        RecoverSplitHeader = Gtk.Label("Recover using")
        RecoverSplit = Gtk.SpinButton().new_with_range(min=2, max=25, step=1)
        RecoverSplit.props.expand = False
        RecoverSplit.connect("value-changed", self.on_recoversplit_changed)

        ResultsTextBuffer = Gtk.TextBuffer()
        ResultsTextBuffer.set_text("")
        textview = Gtk.TextView(buffer=ResultsTextBuffer)
        textview.props.margin = 4
        textview.props.wrap_mode = Gtk.WrapMode.WORD_CHAR

        scrolledview = Gtk.ScrolledWindow()
        scrolledview.add(textview)
        scrolledview.props.shadow_type = Gtk.ShadowType(3)
        scrolledview.props.vscrollbar_policy = Gtk.PolicyType(1)
        scrolledview.props.expand = True

        GoButton = Gtk.Button(image=Gtk.Image().new_from_icon_name(icon_name='emblem-default', size=Gtk.IconSize.DIALOG))
        GoButton.connect("clicked", self.on_gobutton_clicked)

        self.attach(SecretHeader, 0, 1, 4, 1)
        self.attach(SecretEntry, 0, 2, 4, 1)
        self.attach(ShareSplitHeader, 0, 3, 2, 1)
        self.attach_next_to(ShareSplit, ShareSplitHeader, 1, 1, 1)
        self.attach(RecoverSplitHeader, 0, 4, 2, 1)
        self.attach_next_to(RecoverSplit, RecoverSplitHeader, 1, 1, 1)
        self.attach_next_to(GoButton, ShareSplit, 1, 1, 2)
        self.attach(BackButton, 0, 5, 1, 1)
        self.attach(ShareStackHeader, 0, 6, 4, 1)


    def on_secretentry_changed(self, widget, event):
        print('entry')
        print(widget.get_text())

    def on_sharesplit_changed(self, widget):
        print(widget.get_value_as_int())

    def on_recoversplit_changed(self, widget):
        print(widget.get_value_as_int())

    def on_gobutton_clicked(self, widget):
        print(locals())

    def on_backbutton_clicked(self, widget):
        notebook = self.get_parent()
        stack = notebook.get_parent()
        # print(parent)
        # stack = self.get_parent()
        stack.set_visible_child_full("main",Gtk.StackTransitionType.CROSSFADE)


#------------------CLASS-SEPARATOR------------------#

class RecoverView(Gtk.Grid):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        

        ShareSplitHeader = Gtk.Label("How many did you split into")
        ShareSplit = Gtk.SpinButton().new_with_range(min=3, max=25, step=1)
        ShareSplit.connect("value-changed", self.on_sharesplit_changed)
        
        RecoverSplitHeader = Gtk.Label("How many do you have?")
        RecoverSplit = Gtk.SpinButton().new_with_range(min=1, max=25, step=1)
        RecoverSplit.connect("value-changed", self.on_recoversplit_changed)

        GoButton = Gtk.Button(image=Gtk.Image().new_from_icon_name(icon_name='emblem-default', size=Gtk.IconSize.DIALOG))
        GoButton.connect("clicked", self.on_gobutton_clicked)

        self.add(ShareSplitHeader)
        self.add(ShareSplit)
        self.add(RecoverSplitHeader)
        self.add(RecoverSplit)
        self.add(GoButton)

    def on_secretentry_changed(self, widget, event):
        print('entry')
        print(widget.get_text())

    def on_sharesplit_changed(self, widget):
        print(widget.get_value_as_int())

    def on_recoversplit_changed(self, widget):
        print(widget.get_value_as_int())

    def on_gobutton_clicked(self, widget):
        print(locals())
        print(widget.get_parent().get_parent().get_visible_child())

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
        #Gtk.Settings.get_default().set_property("gtk-application-prefer-dark-theme", False)
        provider = Gtk.CssProvider()
        provider.load_from_path("/home/adi/Work/enigmatic/data/application.css")
        # provider.load_from_resource ("com/github/hezral/enigmatic/application.css")
        Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        
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