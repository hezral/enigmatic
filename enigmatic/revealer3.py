#!/usr/bin/python*
from gi.repository import Gtk, GObject

class TestWindow(Gtk.Window):
     def animateImage(self, *args):
        GObject.timeout_add(150,self.slideImage)

     def slideImage(self):
        self.positionX += 50;
        if(self.positionX > 800):
          self.fixedWidget.move(self.logo,self.positionX,200)
          return True        
        else:
          return False 

     def __init__(self):
        Gtk.Window.__init__(self, title='Registration')

        self.positionX = 500
        self.fixedWidget = Gtk.Fixed()
        self.fixedWidget.set_size_request(1920,1080)
        self.fixedWidget.show()

        self.logo = Gtk.Image.new_from_file('/home/adi/Pictures/Avatars/image.jpg')
        self.logo.show()
        self.fixedWidget.put(self.logo,self.positionX,200)

        self.button1 = Gtk.Button('Click me to slide image!')
        self.button1.show()
        self.button1.connect('clicked', self.animateImage)
        self.button1.set_size_request(75,30)
        self.fixedWidget.put(self.button1,750,750)
        self.add(self.fixedWidget)

testWindow = TestWindow()
testWindow.set_size_request(1920,1080)
testWindow.set_name('testWindow')
testWindow.show()

Gtk.main()