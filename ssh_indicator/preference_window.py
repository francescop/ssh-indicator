try:
   from gi.repository import AppIndicator3 as appindicator
except:
   from gi.repository import AppIndicator as appindicator

from gi.repository import Gtk as gtk

import os
import json
import modules

class PreferenceWindow(gtk.Window):

    def __init__(self):
        gtk.Window.__init__(self)
        self.set_title("Preferences")
        self.set_position(gtk.WindowPosition.CENTER)

        self.add_host = gtk.Button(label="Add Host")
        self.remove_host = gtk.Button(label="Remove Host")
        self.close_btn = gtk.Button(label="Close")
        self.host_field = gtk.Entry()
        self.ip_field = gtk.Entry()
        self.user_field = gtk.Entry()
        self.port_field = gtk.Entry()

        self.host_label = gtk.Label("Host")
        self.ip_label = gtk.Label("Ip")
        self.user_label = gtk.Label("User")
        self.port_label = gtk.Label("Port")

        vbox = gtk.VBox(False, 5)
        vbox.props.valign = gtk.Align.CENTER

        hbox3 = gtk.HBox(True, 4)
        hbox2 = gtk.HBox(True, 4)
        hbox = gtk.HBox(True, 4)

        hbox3.pack_start(self.host_label, True, True, 10)
        hbox3.pack_start(self.ip_label, True, True, 10)
        hbox3.pack_start(self.user_label, True, True, 10)
        hbox3.pack_start(self.port_label, True, True, 10)

        hbox2.pack_start(self.host_field, True, True, 10)
        hbox2.pack_start(self.ip_field, True, True, 10)
        hbox2.pack_start(self.user_field, True, True, 10)
        hbox2.pack_start(self.port_field, True, True, 10)

        hbox.pack_start(self.add_host, True, True, 10)
        hbox.pack_start(self.remove_host, True, True, 10)
        hbox.pack_start(self.close_btn, True, True, 10)

#		halign3.props.valign = gtk.Align.CENTER
#	        halign3.add(hbox3)

#		halign2.props.valign = gtk.Align.CENTER
#	        halign2.add(hbox2)

#		halign.props.valign = gtk.Align.CENTER
#	        halign.add(hbox)

        self.liststore = gtk.ListStore(str, str, str, str)

        # Get the preference saved previously
        self.configs = self.parse_config()

        self.treeview = gtk.TreeView(self.liststore)

        column1 = gtk.TreeViewColumn("Host")
        column2 = gtk.TreeViewColumn("Ip")
        column3 = gtk.TreeViewColumn("User")
        column4 = gtk.TreeViewColumn("Port")

        self.treeview.append_column(column1)
        self.treeview.append_column(column2)
        self.treeview.append_column(column3)
        self.treeview.append_column(column4)

        cell = gtk.CellRendererText()

        column1.pack_start(cell, True)
        column1.add_attribute(cell, "text", 0)

        column2.pack_start(cell, True)
        column2.add_attribute(cell, "text", 1)
        column3.pack_start(cell, True)
        column3.add_attribute(cell, "text", 2)
        column4.pack_start(cell, True)
        column4.add_attribute(cell, "text", 3)

        self.add_host.connect("clicked", self.on_add_item)
        self.remove_host.connect("clicked", self.on_remove_item)
        self.close_btn.connect("clicked", self.on_close)

        self.add(vbox)

        vbox.pack_start(self.treeview, True, True, 10)
        vbox.pack_start(hbox3, False, False, 3)
        vbox.pack_start(hbox2, False, False, 3)
        vbox.pack_start(hbox, False, False, 3)

    def on_close(self, widget):
        self.destroy()

    def on_add_item(self, widget):
        host = self.host_field.get_text()
        ip = self.ip_field.get_text()
        user = self.user_field.get_text()
        port = self.port_field.get_text()
        self.liststore.append([host, ip, user, port])
        arr = ()
        for row in self.liststore:
            dic = dict(host=row[0], ip=row[1], user=row[2], port=row[3])
            arr += (dic,)
        json.dump(arr, open(modules.config_file, "wb"))
        return True


    def on_remove_item(self, widget):
        selection = self.treeview.get_selection()
        model, treeiter = selection.get_selected()
        if treeiter is not None:
            model.remove(treeiter)
        arr = ()
        for row in self.liststore:
            dic = dict(host=row[0], ip=row[1], user=row[2], port=row[3])
            arr += (dic,)
        json.dump(arr, open(modules.config_file, "wb"))
        return True


    def parse_config(self):
        if os.path.isfile(modules.config_file):
            self.configs = json.load(open(modules.config_file))
            for h in self.configs:
                item = gtk.MenuItem(h['host'])
                self.liststore.append(
                    [h['host'], h['ip'], h['user'], h['port']])
