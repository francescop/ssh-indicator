try:
   from gi.repository import AppIndicator3 as appindicator
except:
   from gi.repository import AppIndicator as appindicator

from gi.repository import Gtk as gtk

import os
import json
import modules

from preference_window import PreferenceWindow

def connect_to_server(w, ip, port=22):
    os.system("gnome-terminal --tab -e '%s%s -p%s'" % ("ssh root@", ip, port))


class SshIndicator:

    def populate_list(self):
        if self.menu:
            for i in self.menu.get_children():
                self.menu.remove(i)
        if os.path.isfile(modules.config_file):
            hosts = json.load(open(modules.config_file))
            for h in hosts:
                item = gtk.MenuItem(h['host'])
                self.menu.append(item)
                item.connect("activate", connect_to_server, h['ip'])
                item.show()

        # A separator
        separator = gtk.SeparatorMenuItem()
        separator.show()
        self.menu.append(separator)

        item = gtk.MenuItem('Preferences')
        item.connect("activate", self.show_prefs_window)
        item.show()
        self.menu.append(item)

        item = gtk.MenuItem('Quit')
        item.connect("activate", self.quit)
        item.show()
        self.menu.append(item)

    def quit(self, widget):
        gtk.main_quit()

    def show_prefs_window(self, widget, data=None):
        win = PreferenceWindow()
        win.connect("delete-event", gtk.main_quit)
        win.show_all()
        gtk.main()
        self.populate_list()

    def __init__(self):
        def menuitem_response(w, optionName):
            print optionName

        self.ind = appindicator.Indicator.new(
            "example-simple-client",
            "indicator-messages",
            appindicator.IndicatorCategory.APPLICATION_STATUS)
        self.ind.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.ind.set_attention_icon("indicator-messages-new")
        self.ind.set_icon("gnome-terminal")

        # create a menu
        self.menu = gtk.Menu()

        self.populate_list()

        self.ind.set_menu(self.menu)
