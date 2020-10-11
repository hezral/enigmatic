import gi 
# Since a system can have multiple versions 
# of GTK + installed, we want to make  
# sure that we are importing GTK + 3. 
gi.require_version("Gtk", "3.0") 
from gi.repository import Gtk 
  
  
class MyWindow(Gtk.Window): 
    def __init__(self): 
        Gtk.Window.__init__(self, title ="Geeks for Geeks") 
        self.set_border_width(0) 
        self.get_style_context().add_class("rounded")
  
        # Create Notebook 
        self.notebook = Gtk.Notebook()
        # self.notebook.get_style_context().add_class("flat")
        self.notebook.props.tab_pos = Gtk.PositionType.BOTTOM

        self.add(self.notebook) 

        image1=Gtk.Image().new_from_icon_name("com.github.hezral.inspektor", Gtk.IconSize.DND)
        image2=Gtk.Image().new_from_icon_name("com.github.hezral.inspektor", Gtk.IconSize.DND)

   
        # Create Boxes 
        self.page1 = Gtk.Box() 
        self.page1.set_border_width(50) 
        self.page1.add(Gtk.Label("Page 1: Welcome to Geeks for Geeks")) 
        self.notebook.append_page(self.page1, Gtk.Label("Page 1")) 
  
        self.page2 = Gtk.Box() 
        self.page2.set_border_width(50) 
        self.page2.add(Gtk.Label("Page 2: A computer science portal for geeks")) 
        self.notebook.append_page(self.page2, Gtk.Label("Page 2")) 

        self.notebook.child_set_property(self.page1, "tab-expand", True)
        self.notebook.child_set_property(self.page2, "tab-expand", True)

        self.notebook.set_tab_label(self.page1, image1)
        self.notebook.set_tab_label(self.page2, image2)


        HeaderBar = Gtk.HeaderBar()
        HeaderBar.props.show_close_button = True
        HeaderBar.props.decoration_layout = "close:maximize"
        HeaderBar.get_style_context().add_class("default-decoration")
        HeaderBar.get_style_context().add_class(Gtk.STYLE_CLASS_FLAT)
        self.set_titlebar(HeaderBar)
  
  
win = MyWindow() 
win.connect("destroy", Gtk.main_quit) 
# Display the window. 
win.show_all() 
# Start the GTK + processing loop 
Gtk.main() 