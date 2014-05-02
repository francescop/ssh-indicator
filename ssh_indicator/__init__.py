try:  
   from gi.repository import AppIndicator3 as appindicator  
except:  
   from gi.repository import AppIndicator as appindicator

#import pygtk
#pygtk.require('2.0')

from gi.repository import Gtk as gtk
#import appindicator

import sys
import os
import json
import urllib2

config_file = "%s/.sshappindicator.json" % os.getenv('HOME')

class PreferenceWindow(gtk.Window):
	def __init__(self):
		gtk.Window.__init__(self)
		
	        self.set_title("Preferences")
	        self.set_position(gtk.WindowPosition.CENTER)

	        self.add_host = gtk.Button(label="Add Host")
	        self.remove_host = gtk.Button(label="Remove Host")
	        self.save_config = gtk.Button(label="Save")
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
		hbox.pack_start(self.save_config, True, True, 10)

#		halign3.props.valign = gtk.Align.CENTER
#	        halign3.add(hbox3)

#		halign2.props.valign = gtk.Align.CENTER
#	        halign2.add(hbox2)
		
#		halign.props.valign = gtk.Align.CENTER
#	        halign.add(hbox)



		
        	self.liststore = gtk.ListStore(str,str,str,str)

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

	        self.add_host.connect("clicked", self.add_item)
	        self.remove_host.connect("clicked", self.remove_item)
	        self.save_config.connect("clicked", self.save_configs)
	        
		self.add(vbox)
		
		vbox.pack_start(self.treeview, True, True, 10)
		vbox.pack_start(hbox3, False, False, 3)
		vbox.pack_start(hbox2, False, False, 3)
		vbox.pack_start(hbox, False, False, 3)

	def add_item(self, widget):
	        host = self.host_field.get_text()
	        ip = self.ip_field.get_text()
	        user = self.user_field.get_text()
	        port = self.port_field.get_text()
		self.liststore.append([host,ip,user,port])	        
	
	def remove_item(self, widget):
		selection = self.treeview.get_selection()
		model, treeiter = selection.get_selected()
		if treeiter is not None:
        		model.remove(treeiter)

	def save_configs(self, widget):
		arr = ()
		for row in self.liststore:
			dic = dict(host=row[0],ip=row[1],user=row[2],port=row[3])
			arr += (dic,)
	        json.dump(arr, open(config_file, "wb"))
	        return True
		gtk.quit()

	def parse_config(self):
		if os.path.isfile(config_file):
		       	self.configs = json.load(open(config_file))
			for h in self.configs:
				item = gtk.MenuItem(h['host'])
				self.liststore.append([h['host'],h['ip'],h['user'],h['port']])	        
					
def connect_to_droplet(w, ip, port=22):
	os.system("gnome-terminal --tab -e '%s%s -p%s'" % ("ssh root@", ip, port) )	

class SshIndicator:
	def populate_list(self):
		if self.menu:
			for i in self.menu.get_children():
			    self.menu.remove(i)
		if os.path.isfile(config_file):
			hosts = json.load(open(config_file))
			for h in hosts:
				item = gtk.MenuItem(h['host'])
				self.menu.append(item)
			 	item.connect("activate", connect_to_droplet, h['ip'])  
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

	def show_prefs_window(self,widget,data=None):
		win = PreferenceWindow()
		win.connect("delete-event", gtk.main_quit)
		win.show_all()
		gtk.main()
		self.populate_list()

	def __init__(self):
		def menuitem_response(w, optionName):
			print optionName
	
		self.ind = appindicator.Indicator.new("example-simple-client", "indicator-messages", appindicator.IndicatorCategory.APPLICATION_STATUS)
	        self.ind.set_status (appindicator.IndicatorStatus.ACTIVE)
	        self.ind.set_attention_icon ("indicator-messages-new")
	        self.ind.set_icon("gnome-terminal")

#		url = "https://api.digitalocean.com/droplets/?client_id=[client_id]&api_key=[api_key]"
#		data = json.load(urllib2.urlopen(url))
		
		# create some drop down options
#		for droplet in data['droplets']:
#			optionName = droplet['name']
#			droplet_ip = droplet['ip_address']
#			img = gtk.Image()
#			img.set_from_file("item.png")
#			menu_items = gtk.ImageMenuItem(optionName)
#			menu_items.set_image(img)
#			self.menu.append(menu_items)
#		 	menu_items.connect("activate", connect_to_droplet, droplet_ip)  
#			menu_items.show()

		# create a menu
		self.menu = gtk.Menu()

		self.populate_list()
		  
		self.ind.set_menu(self.menu)

def main():
	gtk.main()
	return 0

if __name__ == "__main__":
    indicator = SshIndicator()
    main()
