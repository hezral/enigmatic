import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Tab(Gtk.HBox):
    def __init__(self,label='Page'):
        Gtk.HBox.__init__(self)     
        self.tab_label = Gtk.Label(label)
        self.image = Gtk.Image()
        self.image.set_from_stock(Gtk.STOCK_CLOSE, Gtk.IconSize.MENU)
        self.image.new_from_icon_name("window-close-symbolic", Gtk.IconSize.MENU)
        self.close_button = Gtk.Button()
        self.close_button.set_image(self.image)
        self.close_button.set_relief(Gtk.ReliefStyle.NONE)
        #self.connect(self.close_button, 'clicked', self.close_cb)
        self.pack_start(self.tab_label, expand=True, fill=True, padding=0)
        self.pack_end(self.close_button, expand=False, fill=False, padding=0)
        self.show_all()

settings = Gtk.Settings.get_default()
settings.set_property("gtk-application-prefer-dark-theme", True)
win = Gtk.Window()
notebook = Gtk.Notebook()
header1 = Tab('page 1')
header2 = Tab('page 2')
page1 = Gtk.Label('This is the first page')
page2 = Gtk.Label('This is the second page')

def on_page_switch(self, w, data):
    print(notebook.get_nth_page(notebook.get_current_page()).get_text())

notebook.append_page(page1, header1)
notebook.append_page(page2, header2)
notebook.props.border_width = 0



print(notebook.n_tabs)

win.add(notebook)
win.connect('delete-event', Gtk.main_quit)
win.show_all()
Gtk.main()