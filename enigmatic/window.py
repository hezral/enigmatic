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

        #---- icons -----#
        resource_16 = InternalResource(16)
        resrouce_24 = InternalResource(24)
        resource_32 = InternalResource(32)
        resrouce_48 = InternalResource(48)
        resource_96 = InternalResource(96)

        #---- views -----#
        header = CustomHeaderBar(AppAttributes.application_name)
        main = MainView(resource=resource_96)
        share = ShareView(resource=resource_32)
        recover = RecoverView(resource=resource_32)
        notebook = NotebookView(pages=(share, recover), resource=resource_32)

        #---- stack -----#
        self.stack = Gtk.Stack()
        self.stack.props.transition_type = Gtk.StackTransitionType.CROSSFADE
        self.stack.add_named(main, "main")
        self.stack.add_named(notebook, "notebook")
        #self.stack.set_visible_child(main)
        #self.stack.set_visible_child(notebook)

        #---- layout -----#
        layout = Gtk.Grid()
        layout.props.row_spacing = 12
        layout.attach(self.stack, 0, 3, 2, 1)
        layout.props.expand = True

        #---- window -----#
        self.props.title = AppAttributes.application_name
        self.props.resizable = False
        self.get_style_context().add_class("rounded")
        width = 800
        height = 600
        self.set_size_request(width, height)
        #self.set_default_size(width, height)
        # geometry = Gdk.Geometry()
        # setattr(geometry, 'max_height', height)
        # setattr(geometry, 'max_width', width)
        # self.set_geometry_hints(None, geometry, Gdk.WindowHints.MAX_SIZE)

        self.set_titlebar(header)
        self.add(layout)
        self.show_all()

        print('abc')


#------------------CLASS-SEPARATOR------------------#

class CustomHeaderBar(Gtk.HeaderBar):
    def __init__(self, application_name, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #---- mode switch -----#
        gtk_settings = Gtk.Settings.get_default()
        mode_switch = Granite.ModeSwitch.from_icon_name("display-brightness-symbolic", "weather-clear-night-symbolic")
        mode_switch.props.primary_icon_tooltip_text = "Light mode"
        mode_switch.props.secondary_icon_tooltip_text = "Dark mode"
        mode_switch.props.valign = Gtk.Align.CENTER
        mode_switch.bind_property("active", gtk_settings, "gtk-application-prefer-dark-theme", GObject.BindingFlags.BIDIRECTIONAL)
        gio_settings = Gio.Settings(schema_id="com.github.hezral.movens")
        gio_settings.bind ("prefer-dark-style", mode_switch, "active", Gio.SettingsBindFlags.DEFAULT)

        #---- title -----#
        title_btn = Gtk.Button(label=application_name.upper())
        title_btn.get_style_context().add_class("title-button")
        title_btn.connect("clicked", self.on_title_clicked)

        #---- header -----#
        self.props.show_close_button = True
        self.props.decoration_layout = "close:maximize"
        self.pack_end(mode_switch)
        self.pack_end(title_btn)
        self.get_style_context().add_class("default-decoration")
        self.get_style_context().add_class(Gtk.STYLE_CLASS_FLAT)

    def on_title_clicked(self, button):
        about = AboutDialog(window=self.get_parent())
        about.show_all()

class AboutDialog(Gtk.AboutDialog):
    def __init__(self, window, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #---- self props -----#
        self.props.title ="About " + AppAttributes.about_program_name
        self.set_transient_for(window)
        self.set_destroy_with_parent(True)
        self.set_program_name(AppAttributes.about_program_name)
        self.set_version(AppAttributes.about_version)
        self.set_comments(AppAttributes.about_comments)
        self.set_website(AppAttributes.about_website)
        self.set_website_label(AppAttributes.about_website_label)
        self.set_authors(AppAttributes.about_authors)
        # self.set_license(AppAttributes.about_license)
        # self.set_license_type(AppAttributes.about_license_type)
        # self.set_logo_icon_name(AppAttributes.about_logo_icon_name)
        self.connect("response", self.on_response)
 
    def on_response(self, dialog, response):
        self.destroy()

#------------------CLASS-SEPARATOR------------------#

class InternalResource():
    def __init__(self, size, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.share_icn = Gtk.Image().new_from_icon_name("com.github.hezral.inspektor", Gtk.IconSize.DIALOG)
        self.share_icn.set_pixel_size(size)

        self.recover_icn = Gtk.Image().new_from_icon_name("internet-chat", Gtk.IconSize.DIALOG)
        self.recover_icn.set_pixel_size(size)

        self.share_name = "share"
        self.recover_name = "recover"

    def resize(self, size):
        self.share_icn.set_pixel_size(size)
        self.recover_icn.set_pixel_size(size)

#------------------CLASS-SEPARATOR------------------#

class MainView(Gtk.Grid):
    def __init__(self, resource, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #---- get started -----#
        getstarted_img = Gtk.Image().new_from_icon_name("text-x-readme", Gtk.IconSize.LARGE_TOOLBAR)
        getstarted_btn = Gtk.Button(label="Quick Start Guide", image=getstarted_img)
        getstarted_btn.props.hexpand = True
        getstarted_btn.props.always_show_image = True
        getstarted_btn.props.relief = Gtk.ReliefStyle.NONE
        
        #---- stack buttons -----#
        sharestack_btn = Gtk.Button(label=resource.share_name.upper(), image=resource.share_icn)
        sharestack_btn.props.always_show_image = True
        sharestack_btn.props.image_position = Gtk.PositionType.TOP
        sharestack_btn.props.expand = True
        sharestack_btn.props.name = resource.share_name.upper()
        sharestack_btn.connect("clicked", self.toggle_stack)
        sharestack_btn.get_style_context().add_class("stack-button")

        recoverstack_btn = Gtk.Button(label=resource.recover_name.upper(), image=resource.recover_icn)
        recoverstack_btn.props.always_show_image = True
        recoverstack_btn.props.image_position = Gtk.PositionType.TOP
        recoverstack_btn.props.expand = True
        recoverstack_btn.props.name = resource.recover_name.upper()
        recoverstack_btn.connect("clicked", self.toggle_stack)
        recoverstack_btn.get_style_context().add_class("stack-button")

        #---- grid -----#
        self.props.expand = True
        self.get_style_context().add_class("mainview")
        self.attach(sharestack_btn, 0, 1, 1, 1)
        self.attach_next_to(recoverstack_btn, sharestack_btn, 1, 1, 1)
        self.attach(getstarted_btn, 0, 2, 2, 1)

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
    def __init__(self, pages, resource, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.props.tab_pos = Gtk.PositionType.BOTTOM
        self.props.expand = True
        self.append_page(pages[0], Gtk.Label(pages[0].get_name()))
        self.append_page(pages[1], Gtk.Label(pages[1].get_name()))
        self.child_set_property(pages[0], "tab-expand", True)
        self.child_set_property(pages[1], "tab-expand", True)

        page0label = self.generate_page_label(pages[0].get_name(), resource.share_icn)
        page0label.connect("clicked", self.on_page0)
        page1label = self.generate_page_label(pages[1].get_name(), resource.recover_icn)
        page1label.connect("clicked", self.on_page1)

        self.set_tab_label(pages[0], page0label)        
        self.set_tab_label(pages[1], page1label)
        # self.connect("switch_page", self.on_notebook_select_page)

    def generate_page_label(self, text, icon):
        button = Gtk.Button(label=text, image=icon)
        button.props.relief = Gtk.ReliefStyle.NONE
        button.props.always_show_image = True
        button.set_focus_on_click(False)

        # Gtk.Button consists of Gtk.Alignment > Gtk.Box > Gtk.Image + Gtk.Label
        # use get_child and get_children to access the inner widgets
        button_label = button.get_child().get_children()[0].get_children()[1]
        button_label.props.valign = Gtk.Align.CENTER
        # button_label.get_style_context().add_class("notebook-tab-label")

        return button

    def on_page0(self, button):
        self.set_current_page(0)

    def on_page1(self, button):
        self.set_current_page(1)

    def on_notebook_select_page(self, notebook, page, page_index):
        print(locals())

#------------------CLASS-SEPARATOR------------------#


class ShareView(Gtk.Grid):
    def __init__(self, resource, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #---- self props -----#
        self.props.name = resource.share_name.upper()
        self.props.margin_left = 20
        self.props.margin_right = 20
        self.props.margin_bottom = 20
        self.props.row_spacing = 10
        self.get_style_context().add_class("shareview")

        #---- header -----#

        home_btn = Gtk.Button(label="Home", image=Gtk.Image().new_from_icon_name(icon_name='edit-undo', size=Gtk.IconSize.LARGE_TOOLBAR))
        home_btn.props.expand = False
        home_btn.props.valign = Gtk.Align.START
        home_btn.props.halign = Gtk.Align.START
        home_btn.props.always_show_image = True
        home_btn.props.relief = Gtk.ReliefStyle.NONE
        home_btn.set_focus_on_click(False)
        # home_btn.set_size_request(40, 40)
        home_btn_label = home_btn.get_child().get_children()[0].get_children()[1]
        home_btn_label.props.valign = Gtk.Align.CENTER
        #home_btn.get_style_context().add_class("back-to-main-button")
        home_btn.connect("clicked", self.on_home_btn_clicked)

        secret_headerlabel = Gtk.Label("Secrets or Passphrase to share")
        secret_headerlabel.get_style_context().add_class("entry")
        secret_headerlabel.props.hexpand = True

        secret_entry = Gtk.Entry()
        secret_entry.set_size_request(-1, 32)
        secret_entry.connect("focus_out_event", self.on_secret_entry_changed)

        sharesplit_headerlabel = Gtk.Label("Split into")
        sharesplit = Gtk.SpinButton().new_with_range(min=3, max=25, step=1)
        sharesplit.connect("value-changed", self.on_sharesplit_changed)
        
        recoversplit_headerlabel = Gtk.Label("Recover using")
        recoversplit = Gtk.SpinButton().new_with_range(min=2, max=25, step=1)
        recoversplit.props.expand = False
        recoversplit.connect("value-changed", self.on_recoversplit_changed)

        results_textbuffer = Gtk.TextBuffer()
        results_textbuffer.set_text("")
        textview = Gtk.TextView(buffer=results_textbuffer)
        textview.props.margin = 4
        textview.props.wrap_mode = Gtk.WrapMode.WORD_CHAR

        scrolledview = Gtk.ScrolledWindow()
        scrolledview.add(textview)
        scrolledview.props.shadow_type = Gtk.ShadowType(3)
        scrolledview.props.vscrollbar_policy = Gtk.PolicyType(1)
        scrolledview.props.expand = True

        go_button = Gtk.Button(image=Gtk.Image().new_from_icon_name(icon_name='emblem-default', size=Gtk.IconSize.DIALOG))
        go_button.connect("clicked", self.on_go_button_clicked)

        run_button = Gtk.Button(label="Run", image=Gtk.Image().new_from_icon_name(icon_name='emblem-default', size=Gtk.IconSize.DIALOG))
        run_button.props.always_show_image = True
        run_button.connect("clicked", self.on_go_button_clicked)

        #---- self layout -----#
        self.attach(home_btn, 0, 1, 1, 1,)
        self.attach(secret_headerlabel, 0, 1, 4, 1)
        self.attach(secret_entry, 0, 2, 4, 1)
        self.attach(sharesplit_headerlabel, 0, 3, 2, 1)
        self.attach_next_to(sharesplit, sharesplit_headerlabel, 1, 1, 1)
        self.attach(recoversplit_headerlabel, 0, 4, 2, 1)
        self.attach_next_to(recoversplit, recoversplit_headerlabel, 1, 1, 1)
        self.attach(run_button, 0, 5, 4, 1,)



    def on_secret_entry_changed(self, widget, event):
        print('entry')
        print(widget.get_text())

    def on_sharesplit_changed(self, widget):
        print(widget.get_value_as_int())

    def on_recoversplit_changed(self, widget):
        print(widget.get_value_as_int())

    def on_go_button_clicked(self, widget):
        print(locals())

    def on_home_btn_clicked(self, widget):
        notebook = self.get_parent()
        stack = notebook.get_parent()
        # print(parent)
        # stack = self.get_parent()
        stack.set_visible_child_full("main",Gtk.StackTransitionType.CROSSFADE)


#------------------CLASS-SEPARATOR------------------#

class RecoverView(Gtk.Grid):
    def __init__(self, resource, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #---- grid props -----#
        self.props.name = resource.recover_name.upper()
        self.get_style_context().add_class("recoverview")

        sharesplit_headerlabel = Gtk.Label("How many did you split into")
        sharesplit = Gtk.SpinButton().new_with_range(min=3, max=25, step=1)
        sharesplit.connect("value-changed", self.on_sharesplit_changed)
        
        recoversplit_headerlabel = Gtk.Label("How many do you have?")
        recoversplit = Gtk.SpinButton().new_with_range(min=1, max=25, step=1)
        recoversplit.connect("value-changed", self.on_recoversplit_changed)

        go_button = Gtk.Button(image=Gtk.Image().new_from_icon_name(icon_name='emblem-default', size=Gtk.IconSize.DIALOG))
        go_button.connect("clicked", self.on_go_button_clicked)

        
        self.add(sharesplit_headerlabel)
        self.add(sharesplit)
        self.add(recoversplit_headerlabel)
        self.add(recoversplit)
        self.add(go_button)

    def on_secret_entry_changed(self, widget, event):
        print('entry')
        print(widget.get_text())

    def on_sharesplit_changed(self, widget):
        print(widget.get_value_as_int())

    def on_recoversplit_changed(self, widget):
        print(widget.get_value_as_int())

    def on_go_button_clicked(self, widget):
        print(locals())
        print(widget.get_parent().get_parent().get_visible_child())

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