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
    
        #---- icons -----#
        icons16 = ModuleIcon(16)
        icons24 = ModuleIcon(24)
        icons32 = ModuleIcon(32)
        icons48 = ModuleIcon(48)
        icons96 = ModuleIcon(96)

        #---- views -----#
        main = MainView(icons=icons96)
        share = ShareView()
        recover = RecoverView()
        notebook = NotebookView(pages=(share, recover), icons=icons32)

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


        self.props.title = AppAttributes.application_name
        # self.props.border_width = 24
        self.props.resizable = False
        self.get_style_context().add_class("rounded")
        #self.get_style_context().add_class(Gtk.STYLE_CLASS_FLAT)
        width = 800
        height = 600
        self.set_size_request(width, height)
        #self.set_default_size(width, height)
        # geometry = Gdk.Geometry()
        # setattr(geometry, 'max_height', height)
        # setattr(geometry, 'max_width', width)
        # self.set_geometry_hints(None, geometry, Gdk.WindowHints.MAX_SIZE)

        self.set_titlebar(HeaderBar)
        self.add(layout)
        self.show_all()

    def on_notebook_select_page(self, notebook, page, page_index):
        print(locals())

#------------------CLASS-SEPARATOR------------------#

class ModuleIcon():
    def __init__(self, size, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ShareIcon = Gtk.Image().new_from_icon_name("com.github.hezral.inspektor", Gtk.IconSize.DIALOG)
        self.RecoverIcon = Gtk.Image().new_from_icon_name("internet-chat", Gtk.IconSize.DIALOG)
        self.ShareIcon.set_pixel_size(size)
        self.RecoverIcon.set_pixel_size(size)

    def resize(self, size):
        self.ShareIcon.set_pixel_size(size)
        self.RecoverIcon.set_pixel_size(size)



#------------------CLASS-SEPARATOR------------------#

class MainView(Gtk.Grid):
    def __init__(self, icons, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #---- get started -----#
        GetStartedImage = Gtk.Image().new_from_icon_name("text-x-readme", Gtk.IconSize.LARGE_TOOLBAR)
        GetStartedButton = Gtk.Button(label="Quick Start Guide", image=GetStartedImage)
        GetStartedButton.props.hexpand = True
        GetStartedButton.props.always_show_image = True
        GetStartedButton.props.relief = Gtk.ReliefStyle.NONE
        
        #---- stack buttons -----#
        # ShareStackImage = Gtk.Image().new_from_icon_name("com.github.hezral.inspektor", Gtk.IconSize.DIALOG)
        # ShareStackImage.set_pixel_size(96)
        self.ShareStackButton = Gtk.Button(label="SHARE", image=icons.ShareIcon)
        self.ShareStackButton.props.always_show_image = True
        self.ShareStackButton.props.image_position = Gtk.PositionType.TOP
        self.ShareStackButton.props.expand = True
        self.ShareStackButton.connect("clicked", self.toggle_stack)
        self.ShareStackButton.get_style_context().add_class("stack-button")

        # RecoverStackImage = Gtk.Image().new_from_icon_name("internet-chat", Gtk.IconSize.DIALOG)
        # RecoverStackImage.set_pixel_size(96)
        self.RecoverStackButton = Gtk.Button(label="RECOVER", image=icons.RecoverIcon)
        self.RecoverStackButton.props.always_show_image = True
        self.RecoverStackButton.props.image_position = Gtk.PositionType.TOP
        self.RecoverStackButton.props.expand = True
        self.RecoverStackButton.connect("clicked", self.toggle_stack)
        self.RecoverStackButton.get_style_context().add_class("stack-button")

        #---- grid -----#
        self.props.expand = True
        self.get_style_context().add_class("mainview")
        self.attach(self.ShareStackButton, 0, 1, 1, 1)
        self.attach_next_to(self.RecoverStackButton, self.ShareStackButton, 1, 1, 1)
        self.attach(GetStartedButton, 0, 2, 2, 1)

    def toggle_stack(self, widget):
        stack = self.get_parent()
        stack_children = stack.get_child_by_name("notebook")
        stack.set_visible_child_full("notebook",Gtk.StackTransitionType.CROSSFADE)
        if widget.get_label() == "SHARE":
            stack_children.set_current_page(0)
        else:
            stack_children.set_current_page(1)

#------------------CLASS-SEPARATOR------------------#

class NotebookView(Gtk.Notebook):
    def __init__(self, pages, icons, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.props.tab_pos = Gtk.PositionType.BOTTOM
        self.append_page(pages[0], Gtk.Label(pages[0].get_name()))
        self.append_page(pages[1], Gtk.Label(pages[1].get_name()))
        self.child_set_property(pages[0], "tab-expand", True)
        self.child_set_property(pages[1], "tab-expand", True)



        page0label = self.generate_page_label(pages[0].get_name(), icons.ShareIcon)
        page0label.connect("clicked", self.on_page0)
        page1label = self.generate_page_label(pages[1].get_name(), icons.RecoverIcon)
        page1label.connect("clicked", self.on_page1)

        

        self.set_tab_label(pages[0], page0label)        
        self.set_tab_label(pages[1], page1label)
        # self.connect("switch_page", self.on_notebook_select_page)

    def generate_page_label(self, text, icon):
        button = Gtk.Button(label=text, image=icon)
        button.props.relief = Gtk.ReliefStyle.NONE
        button.props.always_show_image = True
        button.set_focus_on_click(False)
        button.get_style_context().add_class("notebook-tab-label")

        # Gtk.Button consists of Gtk.Alignment > Gtk.Box > Gtk.Image + Gtk.Label
        # use get_child and get_children to access the inner widgets
        button_label = button.get_child().get_children()[0].get_children()[1]
        button_label.props.valign = Gtk.Align.CENTER

        return button

    def on_page0(self, button):
        self.set_current_page(0)

    def on_page1(self, button):
        self.set_current_page(1)

    def on_notebook_select_page(self, notebook, page, page_index):
        print(locals())

#------------------CLASS-SEPARATOR------------------#


class ShareView(Gtk.Grid):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.props.name = "SHARE"

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

        self.get_style_context().add_class("shareview")
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

        self.props.name = "RECOVER"
        

        ShareSplitHeader = Gtk.Label("How many did you split into")
        ShareSplit = Gtk.SpinButton().new_with_range(min=3, max=25, step=1)
        ShareSplit.connect("value-changed", self.on_sharesplit_changed)
        
        RecoverSplitHeader = Gtk.Label("How many do you have?")
        RecoverSplit = Gtk.SpinButton().new_with_range(min=1, max=25, step=1)
        RecoverSplit.connect("value-changed", self.on_recoversplit_changed)

        GoButton = Gtk.Button(image=Gtk.Image().new_from_icon_name(icon_name='emblem-default', size=Gtk.IconSize.DIALOG))
        GoButton.connect("clicked", self.on_gobutton_clicked)

        self.get_style_context().add_class("recoverview")
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